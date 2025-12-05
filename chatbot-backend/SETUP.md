# Chatbot Backend Setup Guide

Complete step-by-step guide to set up the Physical AI RAG chatbot backend.

## Prerequisites

- Python 3.10 or higher
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Qdrant (local or cloud)
- Neon PostgreSQL (optional, for analytics)

## Step 1: Install Dependencies

```bash
cd chatbot-backend
pip install -r requirements.txt
```

## Step 2: Setup Qdrant Vector Database

### Option A: Local Qdrant (Recommended for Development)

```bash
# Using Docker (easiest)
docker run -p 6333:6333 qdrant/qdrant

# Or download from https://qdrant.tech/documentation/quick-start/
```

### Option B: Qdrant Cloud (Recommended for Production)

1. Sign up at [cloud.qdrant.io](https://cloud.qdrant.io)
2. Create a new cluster
3. Copy the URL and API key

## Step 3: Setup OpenAI API

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with `sk-proj-...`)

## Step 4: Configure Environment Variables

```bash
# Copy the example .env file
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or use your favorite text editor
```

**Required variables:**
```env
OPENAI_API_KEY=sk-proj-your_actual_key_here
QDRANT_URL=http://localhost:6333  # or your Qdrant Cloud URL
```

**Optional variables:**
```env
QDRANT_API_KEY=your_qdrant_cloud_key  # only for Qdrant Cloud
DATABASE_URL=postgresql://...         # only if using PostgreSQL analytics
```

## Step 5: Setup PostgreSQL (Optional)

If you want conversation logging and analytics:

### Option A: Neon PostgreSQL (Recommended)

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Add to `.env`:
   ```env
   DATABASE_URL=postgresql://username:password@host/dbname?sslmode=require
   ```

### Option B: Local PostgreSQL

```bash
# Install PostgreSQL
# Then create database and run schema
psql -U postgres -d your_database -f schema.sql
```

## Step 6: Ingest Course Content

This creates embeddings for all Week 1-2 content:

```bash
python ingest.py
```

**Expected output:**
```
============================================================
STEP 1: Discovering markdown files
============================================================
✓ Found 6 markdown files

============================================================
STEP 2: Processing files into chunks
============================================================
Processing files: 100%|██████████| 6/6 [00:00<00:00, 12.34it/s]

✓ Created 45 total chunks

============================================================
STEP 3: Creating Qdrant collection
============================================================
  ✓ Created collection 'physical_ai_course' (dimension: 1536)

============================================================
STEP 4: Generating embeddings
============================================================
  Generating embeddings for 45 chunks...
  ✓ Generated 45 embeddings

============================================================
STEP 5: Uploading to Qdrant
============================================================
Uploading batches: 100%|██████████| 1/1 [00:00<00:00,  5.23it/s]

✓ Uploaded 45 points to Qdrant

============================================================
INGESTION COMPLETE!
============================================================

📊 Summary:
  - Files processed: 6
  - Chunks created: 45
  - Embeddings generated: 45
  - Collection: physical_ai_course
  - Embedding model: text-embedding-3-small
```

**Troubleshooting ingestion:**
- **Error: OPENAI_API_KEY not set**: Add your OpenAI API key to `.env`
- **Error: Connection refused**: Make sure Qdrant is running
- **Error: Directory not found**: Run from `chatbot-backend/` directory

## Step 7: Start the Backend Server

```bash
uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
✓ Database connection pool created
INFO:     Application startup complete.
```

The API is now running at http://localhost:8000

## Step 8: Test the Backend

### Option A: Web Interface

Open your browser and go to:
```
http://localhost:8000/docs
```

This opens the FastAPI Swagger UI where you can test all endpoints interactively.

### Option B: Test Script

```bash
python test_chat.py
```

**Expected output:**
```
============================================================
PHYSICAL AI CHATBOT - COMPREHENSIVE TEST SUITE
============================================================
API URL: http://localhost:8000

============================================================
TEST 1: Health Check
============================================================
✓ Status: 200
✓ Overall health: healthy

Components:
  ✓ vector_store: healthy
  ✓ llm: healthy
  ✓ database: healthy

============================================================
TEST: Chat with question
============================================================
Question: What is physical AI?

✓ Response received in 1523ms

Answer:
Physical AI refers to artificial intelligence systems that interact with the physical world through embodied forms, such as robots...

✓ Confidence: 89.2%
✓ Response time: 1523ms

✓ Sources (3):
  1. What is Physical AI
     URL: /docs/weeks/week-01-02-physical-ai/what-is-physical-ai
     Similarity: 94.5%
  2. Introduction to Physical AI
     URL: /docs/weeks/week-01-02-physical-ai/intro
     Similarity: 87.3%
  3. Embodied Intelligence
     URL: /docs/weeks/week-01-02-physical-ai/embodied-intelligence
     Similarity: 85.8%

✓ Performance: EXCELLENT (< 3 seconds)

...

============================================================
TEST SUMMARY
============================================================

Passed: 7/7 tests

Average confidence: 87.5%
Average response time: 1845ms

✓ ALL TESTS PASSED!

🎉 Your chatbot is working correctly!
```

### Option C: cURL

```bash
# Test health check
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is physical AI?",
    "conversation_history": []
  }'
```

## Step 9: Verify Qdrant Dashboard (Optional)

Open http://localhost:6333/dashboard to see your vector database.

You should see:
- Collection: `physical_ai_course`
- Points: 45 (or however many chunks were created)
- Vector size: 1536

## Troubleshooting

### Backend won't start

**Error: ModuleNotFoundError**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Error: Port 8000 already in use**
```bash
# Solution: Use a different port
uvicorn main:app --reload --port 8001
```

### Health check fails

**vector_store: error**
- Make sure Qdrant is running on port 6333
- Check `QDRANT_URL` in `.env`
- Verify you ran `python ingest.py` successfully

**llm: error**
- Check your `OPENAI_API_KEY` in `.env`
- Verify the key is valid at [platform.openai.com](https://platform.openai.com)

**database: not_configured**
- This is OK if you don't need analytics
- To enable, set `DATABASE_URL` in `.env`

### Chat responses are poor quality

**Low confidence scores (<70%)**
- Run ingestion again: `python ingest.py --recreate`
- Try increasing `TOP_K_RESULTS` in `.env`
- Lower `SIMILARITY_THRESHOLD` in `.env`

**Slow response times (>3 seconds)**
- Use `gpt-4o-mini` instead of `gpt-4o` (set in `.env`)
- Reduce `TOP_K_RESULTS` to 3
- Use `text-embedding-3-small` instead of `large`

**Irrelevant responses**
- Check that ingestion completed successfully
- Verify Week 1-2 content exists in `../book/docs/weeks/week-01-02-physical-ai/`
- Try filtering by week: `"week_filter": "week-01-02"` in request

## Next Steps

1. **Integrate with Docusaurus**: Follow `INTEGRATION.md` to add the ChatBot component
2. **Deploy to production**: Follow `DEPLOYMENT.md` for Railway/Render deployment
3. **Monitor usage**: Check `/stats` endpoint for analytics
4. **Collect feedback**: Use the feedback system to improve responses

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | LLM model for responses |
| `OPENAI_EMBEDDING_MODEL` | No | `text-embedding-3-small` | Embedding model |
| `QDRANT_URL` | No | `http://localhost:6333` | Qdrant server URL |
| `QDRANT_API_KEY` | No | - | Qdrant Cloud API key |
| `QDRANT_COLLECTION_NAME` | No | `physical_ai_course` | Collection name |
| `DATABASE_URL` | No | - | PostgreSQL connection string |
| `CHUNK_SIZE` | No | `1000` | Characters per chunk |
| `CHUNK_OVERLAP` | No | `200` | Overlap between chunks |
| `TOP_K_RESULTS` | No | `5` | Number of chunks to retrieve |
| `SIMILARITY_THRESHOLD` | No | `0.7` | Minimum similarity (0-1) |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/chat` | POST | Ask questions |
| `/feedback` | POST | Submit feedback |
| `/stats` | GET | Usage statistics |
| `/docs` | GET | Swagger UI |

## Cost Estimation

Based on Week 1-2 content (~10,000 words):

**One-time ingestion:**
- Embeddings: ~$0.02 (45 chunks × $0.00002/1K tokens)
- Total: **~$0.02**

**Per 1000 queries:**
- Query embeddings: ~$0.20
- LLM responses (gpt-4o-mini): ~$3.00
- Total: **~$3.20 per 1000 queries**

**Monthly estimate (100 queries/day):**
- ~3000 queries/month
- Cost: **~$10/month**

To reduce costs:
- Use `text-embedding-3-small` (already default)
- Use `gpt-4o-mini` instead of `gpt-4o`
- Cache frequently asked questions
- Reduce `TOP_K_RESULTS` to 3

## Support

- Backend issues: Check the FastAPI logs
- Qdrant issues: Check Qdrant dashboard at `:6333/dashboard`
- OpenAI issues: Check usage at [platform.openai.com/usage](https://platform.openai.com/usage)
- Report bugs: Create an issue in the GitHub repository
