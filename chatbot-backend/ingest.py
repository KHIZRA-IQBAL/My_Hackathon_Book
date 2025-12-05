"""
Ingest Docusaurus markdown content into Qdrant vector store
Processes course content and creates embeddings for RAG retrieval
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import re
from dotenv import load_dotenv
from tqdm import tqdm
import frontmatter

# OpenAI and Qdrant imports
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_course")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Embedding dimensions for different models
EMBEDDING_DIMENSIONS = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536
}


class DocumentChunker:
    """Split markdown documents into semantically meaningful chunks"""

    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_by_headers(self, content: str, metadata: dict) -> List[Dict]:
        """
        Split content by markdown headers while preserving hierarchy
        Each chunk includes header context for better retrieval
        """
        chunks = []

        # Parse content by headers
        lines = content.split('\n')
        current_chunk = []
        current_headers = []  # Stack of current header hierarchy
        current_size = 0

        for line in lines:
            # Check if line is a header
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)

            if header_match:
                # Save current chunk if it exists
                if current_chunk and current_size > 0:
                    chunk_text = '\n'.join(current_chunk).strip()
                    if chunk_text:
                        chunks.append({
                            "content": chunk_text,
                            "metadata": {
                                **metadata,
                                "headers": list(current_headers),
                                "section": ' > '.join(current_headers) if current_headers else "Root"
                            }
                        })

                # Update header hierarchy
                header_level = len(header_match.group(1))
                header_text = header_match.group(2).strip()

                # Adjust hierarchy stack
                current_headers = current_headers[:header_level-1] + [header_text]

                # Start new chunk with header
                current_chunk = [line]
                current_size = len(line)

            else:
                # Add line to current chunk
                current_chunk.append(line)
                current_size += len(line) + 1  # +1 for newline

                # If chunk is too large, split it
                if current_size > self.chunk_size:
                    # Save current chunk
                    chunk_text = '\n'.join(current_chunk).strip()
                    if chunk_text:
                        chunks.append({
                            "content": chunk_text,
                            "metadata": {
                                **metadata,
                                "headers": list(current_headers),
                                "section": ' > '.join(current_headers) if current_headers else "Root"
                            }
                        })

                    # Start new chunk with overlap
                    overlap_lines = current_chunk[-5:] if len(current_chunk) > 5 else current_chunk
                    current_chunk = overlap_lines
                    current_size = sum(len(line) + 1 for line in overlap_lines)

        # Add final chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk).strip()
            if chunk_text:
                chunks.append({
                    "content": chunk_text,
                    "metadata": {
                        **metadata,
                        "headers": list(current_headers),
                        "section": ' > '.join(current_headers) if current_headers else "Root"
                    }
                })

        return chunks


class CourseContentIngester:
    """Ingest course content from Docusaurus markdown files"""

    def __init__(self, docs_dir: str = "../book/docs"):
        self.docs_dir = Path(docs_dir)
        self.chunker = DocumentChunker()

        # Initialize clients
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment variables")

        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

        print(f"✓ Initialized OpenAI client (model: {EMBEDDING_MODEL})")
        print(f"✓ Initialized Qdrant client (url: {QDRANT_URL})")

    def extract_frontmatter(self, file_path: Path) -> Dict:
        """Extract YAML frontmatter from markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            return {
                "title": post.get("title", file_path.stem),
                "sidebar_position": post.get("sidebar_position", 0),
                "description": post.get("description", ""),
                **post.metadata
            }
        except Exception as e:
            print(f"Warning: Could not parse frontmatter for {file_path}: {e}")
            return {
                "title": file_path.stem,
                "path": str(file_path.relative_to(self.docs_dir))
            }

    def clean_content(self, content: str) -> str:
        """Clean markdown content for better embedding"""
        # Remove frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Remove HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

        # Remove excessive newlines
        content = re.sub(r'\n{3,}', '\n\n', content)

        # Remove code block language specifiers but keep code
        # This preserves the code content while removing syntax highlighting hints
        content = re.sub(r'```(\w+)\n', '```\n', content)

        return content.strip()

    def process_markdown_file(self, file_path: Path) -> List[Dict]:
        """Process a single markdown file into chunks with metadata"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                full_content = f.read()

            # Extract frontmatter
            post = frontmatter.loads(full_content)
            metadata = post.metadata

            # Clean content
            content = self.clean_content(post.content)

            if not content.strip():
                print(f"  ⚠ Skipping {file_path.name} (empty content)")
                return []

            # Build complete metadata
            file_metadata = {
                "title": metadata.get("title", file_path.stem),
                "source_file": str(file_path.name),
                "week": self._extract_week(file_path),
                "url": self._generate_url(file_path),
                "type": "course_content"
            }

            # Chunk content
            chunks = self.chunker.chunk_by_headers(content, file_metadata)

            return chunks

        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")
            return []

    def _extract_week(self, file_path: Path) -> str:
        """Extract week identifier from file path"""
        path_str = str(file_path)
        match = re.search(r'week-(\d{2}-\d{2})', path_str)
        return match.group(0) if match else "unknown"

    def _generate_url(self, file_path: Path) -> str:
        """Generate Docusaurus URL from file path"""
        # Convert path to URL
        # E.g., docs/weeks/week-01-02-physical-ai/intro.md -> /docs/weeks/week-01-02-physical-ai/intro
        relative_path = file_path.relative_to(self.docs_dir)
        url_parts = list(relative_path.parts)

        # Remove .md extension
        if url_parts[-1].endswith('.md'):
            url_parts[-1] = url_parts[-1][:-3]

        # Build URL
        url = '/docs/' + '/'.join(url_parts)
        return url

    def generate_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate embeddings for a list of texts in batches"""
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                response = self.openai_client.embeddings.create(
                    model=EMBEDDING_MODEL,
                    input=batch
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
            except Exception as e:
                print(f"Error generating embeddings for batch {i//batch_size + 1}: {e}")
                raise

        return all_embeddings

    def create_collection(self, collection_name: str = COLLECTION_NAME, recreate: bool = False):
        """Create Qdrant collection with appropriate configuration"""
        vector_size = EMBEDDING_DIMENSIONS.get(EMBEDDING_MODEL, 1536)

        try:
            # Check if collection exists
            collections = self.qdrant_client.get_collections()
            exists = any(c.name == collection_name for c in collections.collections)

            if exists:
                if recreate:
                    print(f"  Deleting existing collection: {collection_name}")
                    self.qdrant_client.delete_collection(collection_name)
                else:
                    print(f"  ✓ Collection '{collection_name}' already exists")
                    return

            # Create collection
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

            print(f"  ✓ Created collection '{collection_name}' (dimension: {vector_size})")

        except Exception as e:
            print(f"  ✗ Error creating collection: {e}")
            raise

    def ingest_all_content(self, recreate_collection: bool = False):
        """
        Main ingestion pipeline:
        1. Discover all markdown files in docs/weeks/
        2. Process each file into chunks
        3. Generate embeddings using OpenAI
        4. Store in Qdrant vector store
        """
        print("\n" + "=" * 60)
        print("STEP 1: Discovering markdown files")
        print("=" * 60)

        # Find all markdown files in weeks directory
        weeks_dir = self.docs_dir / "weeks"
        if not weeks_dir.exists():
            print(f"✗ Error: Directory not found: {weeks_dir}")
            print(f"  Make sure you're running from the chatbot-backend/ directory")
            return

        markdown_files = list(weeks_dir.glob("**/*.md"))
        print(f"✓ Found {len(markdown_files)} markdown files")

        print("\n" + "=" * 60)
        print("STEP 2: Processing files into chunks")
        print("=" * 60)

        all_chunks = []
        for file_path in tqdm(markdown_files, desc="Processing files"):
            chunks = self.process_markdown_file(file_path)
            all_chunks.extend(chunks)

        print(f"\n✓ Created {len(all_chunks)} total chunks")

        if not all_chunks:
            print("✗ No chunks created. Exiting.")
            return

        print("\n" + "=" * 60)
        print("STEP 3: Creating Qdrant collection")
        print("=" * 60)

        self.create_collection(recreate=recreate_collection)

        print("\n" + "=" * 60)
        print("STEP 4: Generating embeddings")
        print("=" * 60)

        # Extract texts for embedding
        texts = [chunk["content"] for chunk in all_chunks]

        print(f"  Generating embeddings for {len(texts)} chunks...")
        embeddings = self.generate_embeddings(texts)
        print(f"  ✓ Generated {len(embeddings)} embeddings")

        print("\n" + "=" * 60)
        print("STEP 5: Uploading to Qdrant")
        print("=" * 60)

        # Create points for Qdrant
        points = []
        for i, (chunk, embedding) in enumerate(zip(all_chunks, embeddings)):
            point = PointStruct(
                id=i,
                vector=embedding,
                payload={
                    "content": chunk["content"],
                    **chunk["metadata"]
                }
            )
            points.append(point)

        # Upload in batches
        batch_size = 100
        for i in tqdm(range(0, len(points), batch_size), desc="Uploading batches"):
            batch = points[i:i + batch_size]
            self.qdrant_client.upsert(
                collection_name=COLLECTION_NAME,
                points=batch
            )

        print(f"\n✓ Uploaded {len(points)} points to Qdrant")

        print("\n" + "=" * 60)
        print("INGESTION COMPLETE!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"  - Files processed: {len(markdown_files)}")
        print(f"  - Chunks created: {len(all_chunks)}")
        print(f"  - Embeddings generated: {len(embeddings)}")
        print(f"  - Collection: {COLLECTION_NAME}")
        print(f"  - Embedding model: {EMBEDDING_MODEL}")
        print(f"\n🎯 Next steps:")
        print(f"  1. Test retrieval: python -c 'from main import *; print(search_similar_documents(generate_embedding(\"What is physical AI?\")))'")
        print(f"  2. Start the API: uvicorn main:app --reload")
        print(f"  3. Test chat: curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{{\"question\": \"What is embodied intelligence?\"}}'")
        print(f"  4. View Qdrant dashboard: {QDRANT_URL}/dashboard")


def main():
    """Main ingestion script"""
    print("\n" + "=" * 60)
    print("Physical AI Course Content Ingestion")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Docs directory: ../book/docs")
    print(f"  Qdrant URL: {QDRANT_URL}")
    print(f"  Collection: {COLLECTION_NAME}")
    print(f"  Embedding model: {EMBEDDING_MODEL}")
    print(f"  Chunk size: {CHUNK_SIZE}")
    print(f"  Chunk overlap: {CHUNK_OVERLAP}")

    # Check if we should recreate collection
    recreate = "--recreate" in sys.argv or "--force" in sys.argv

    if recreate:
        print("\n⚠ WARNING: --recreate flag detected. Existing collection will be deleted!")
        response = input("Continue? (yes/no): ")
        if response.lower() != "yes":
            print("Aborted.")
            return

    try:
        # Initialize ingester
        ingester = CourseContentIngester(docs_dir="../book/docs")

        # Run ingestion pipeline
        ingester.ingest_all_content(recreate_collection=recreate)

    except ValueError as e:
        print(f"\n✗ Configuration error: {e}")
        print("\nMake sure to set the following environment variables:")
        print("  - OPENAI_API_KEY")
        print("  - QDRANT_URL (optional, defaults to http://localhost:6333)")
        print("\nYou can set these in a .env file in the chatbot-backend/ directory")
        sys.exit(1)

    except Exception as e:
        print(f"\n✗ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
