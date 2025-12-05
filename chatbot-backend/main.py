"""
FastAPI backend for Physical AI & Humanoid Robotics RAG chatbot
Integrates OpenAI + Qdrant + Neon PostgreSQL
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# OpenAI and Qdrant imports
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

# PostgreSQL imports
import asyncpg
import json

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Configuration
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_course")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))

# Database connection pool
db_pool = None

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Chatbot API",
    description="RAG-powered chatbot for Physical AI & Humanoid Robotics course",
    version="1.0.0"
)

# Configure CORS for Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    conversation_history: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    week_filter: Optional[str] = None  # e.g., "week-01-02"

class Source(BaseModel):
    title: str
    url: str
    excerpt: str
    similarity: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
    confidence: float
    response_time_ms: int

class HealthResponse(BaseModel):
    status: str
    components: Dict[str, str]

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize database connection pool on startup"""
    global db_pool
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        try:
            db_pool = await asyncpg.create_pool(
                database_url,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            print("✓ Database connection pool created")
        except Exception as e:
            print(f"⚠ Warning: Could not connect to database: {e}")
    else:
        print("⚠ Warning: DATABASE_URL not set, skipping database features")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection pool on shutdown"""
    global db_pool
    if db_pool:
        await db_pool.close()
        print("✓ Database connection pool closed")


def generate_embedding(text: str) -> List[float]:
    """Generate embedding vector for text using OpenAI"""
    try:
        response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embedding: {str(e)}")


def search_similar_documents(query_vector: List[float], week_filter: Optional[str] = None, limit: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
    """Search Qdrant for similar documents"""
    try:
        # Build filter if week specified
        search_filter = None
        if week_filter:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="week",
                        match=MatchValue(value=week_filter)
                    )
                ]
            )

        # Search in Qdrant
        search_results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            score_threshold=SIMILARITY_THRESHOLD,
            query_filter=search_filter
        ).points

        # Format results
        documents = []
        for result in search_results:
            documents.append({
                "content": result.payload.get("content", ""),
                "title": result.payload.get("title", ""),
                "url": result.payload.get("url", ""),
                "week": result.payload.get("week", ""),
                "similarity": result.score
            })

        return documents

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search documents: {str(e)}")


def generate_response(question: str, context_docs: List[Dict[str, Any]], conversation_history: List[Dict[str, str]]) -> tuple[str, float]:
    """Generate response using OpenAI with RAG context"""
    try:
        # Build context from retrieved documents
        context = "\n\n".join([
            f"[Source: {doc['title']}]\n{doc['content']}"
            for doc in context_docs
        ])

        # Build conversation history
        messages = [
            {
                "role": "system",
                "content": """You are an expert teaching assistant for a Physical AI & Humanoid Robotics course.

Your role is to:
- Answer questions clearly and accurately using the provided course content
- Cite sources when referencing specific information
- Explain complex concepts in accessible terms
- Encourage critical thinking
- Admit when you don't know something rather than speculating

If the provided context doesn't contain enough information to answer the question, say so clearly."""
            }
        ]

        # Add conversation history (last 5 turns)
        for msg in conversation_history[-5:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        # Add current query with context
        user_message = f"""Context from course materials:

{context}

---

Question: {question}

Please answer based on the context provided above. If you reference specific information, mention which source it comes from."""

        messages.append({
            "role": "user",
            "content": user_message
        })

        # Generate response
        response = openai_client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        answer = response.choices[0].message.content

        # Calculate confidence based on context relevance
        avg_similarity = sum(doc["similarity"] for doc in context_docs) / len(context_docs) if context_docs else 0.0
        confidence = min(avg_similarity * 1.2, 1.0)  # Scale up slightly, cap at 1.0

        return answer, confidence

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")


async def log_conversation(question: str, answer: str, sources: List[Dict], confidence: float, response_time_ms: int):
    """Log conversation to PostgreSQL"""
    if not db_pool:
        return  # Skip if database not configured

    try:
        async with db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO conversations (question, answer, sources, confidence, response_time_ms, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, question, answer, json.dumps(sources), confidence, response_time_ms, datetime.utcnow())
    except Exception as e:
        print(f"Warning: Failed to log conversation: {e}")


@app.get("/", response_model=dict)
async def root():
    """API root endpoint"""
    return {
        "message": "Physical AI Chatbot API",
        "status": "active",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "feedback": "/feedback",
            "stats": "/stats"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring
    Checks connectivity to Qdrant, OpenAI, and Neon PostgreSQL
    """
    components = {}

    # Check Qdrant
    try:
        collections = qdrant_client.get_collections()
        collection_exists = any(c.name == COLLECTION_NAME for c in collections.collections)
        components["vector_store"] = "healthy" if collection_exists else "collection_missing"
    except Exception as e:
        components["vector_store"] = f"error: {str(e)[:50]}"

    # Check OpenAI
    try:
        # Simple test to verify API key works
        openai_client.models.list()
        components["llm"] = "healthy"
    except Exception as e:
        components["llm"] = f"error: {str(e)[:50]}"

    # Check PostgreSQL
    if db_pool:
        try:
            async with db_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            components["database"] = "healthy"
        except Exception as e:
            components["database"] = f"error: {str(e)[:50]}"
    else:
        components["database"] = "not_configured"

    all_healthy = all(status == "healthy" for status in components.values())

    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        components=components
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    """
    Main chat endpoint for RAG-powered responses

    Process:
    1. Embed user question using OpenAI embeddings
    2. Search Qdrant vector store for relevant content
    3. Retrieve top-k most similar document chunks
    4. Construct prompt with context + question
    5. Generate response using OpenAI GPT-4
    6. Log conversation to Neon PostgreSQL
    7. Return response with sources
    """
    start_time = time.time()

    try:
        # Step 1: Generate embedding for the question
        query_vector = generate_embedding(request.question)

        # Step 2: Search for similar documents
        similar_docs = search_similar_documents(
            query_vector=query_vector,
            week_filter=request.week_filter,
            limit=TOP_K_RESULTS
        )

        if not similar_docs:
            return ChatResponse(
                answer="I couldn't find relevant information in the course materials to answer your question. Could you rephrase it or ask something more specific about the Physical AI course content?",
                sources=[],
                confidence=0.0,
                response_time_ms=int((time.time() - start_time) * 1000)
            )

        # Step 3: Generate response using RAG
        answer, confidence = generate_response(
            question=request.question,
            context_docs=similar_docs,
            conversation_history=request.conversation_history
        )

        # Step 4: Format sources
        sources = [
            Source(
                title=doc["title"],
                url=doc["url"],
                excerpt=doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"],
                similarity=round(doc["similarity"], 3)
            )
            for doc in similar_docs[:3]  # Return top 3 sources
        ]

        response_time_ms = int((time.time() - start_time) * 1000)

        # Step 5: Log conversation (async in background)
        background_tasks.add_task(
            log_conversation,
            request.question,
            answer,
            [s.dict() for s in sources],
            confidence,
            response_time_ms
        )

        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=round(confidence, 3),
            response_time_ms=response_time_ms
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit user feedback for response quality
    Stores in Neon PostgreSQL for analytics
    """
    if not db_pool:
        return {"status": "success", "message": "Feedback recorded (database not configured)"}

    try:
        async with db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO feedback (question, answer, rating, comment, created_at)
                VALUES ($1, $2, $3, $4, $5)
            """, feedback.question, feedback.answer, feedback.rating, feedback.comment, datetime.utcnow())

        return {"status": "success", "message": "Feedback recorded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record feedback: {str(e)}")


@app.get("/stats")
async def get_stats():
    """
    Get chatbot usage statistics
    Returns aggregated metrics from PostgreSQL
    """
    if not db_pool:
        return {
            "total_questions": 0,
            "avg_response_time_ms": 0,
            "avg_confidence": 0.0,
            "top_topics": [],
            "database_status": "not_configured"
        }

    try:
        async with db_pool.acquire() as conn:
            # Get total questions
            total = await conn.fetchval("SELECT COUNT(*) FROM conversations")

            # Get average response time
            avg_time = await conn.fetchval("SELECT AVG(response_time_ms) FROM conversations") or 0

            # Get average confidence
            avg_conf = await conn.fetchval("SELECT AVG(confidence) FROM conversations") or 0

            # Get recent questions (as proxy for topics)
            recent = await conn.fetch("""
                SELECT question, COUNT(*) as count
                FROM conversations
                WHERE created_at > NOW() - INTERVAL '7 days'
                GROUP BY question
                ORDER BY count DESC
                LIMIT 5
            """)

            return {
                "total_questions": total,
                "avg_response_time_ms": int(avg_time),
                "avg_confidence": round(float(avg_conf), 3),
                "top_topics": [{"question": row["question"], "count": row["count"]} for row in recent],
                "database_status": "connected"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch statistics: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
