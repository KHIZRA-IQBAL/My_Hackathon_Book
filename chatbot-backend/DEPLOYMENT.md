# Chatbot Backend Deployment Guide

Deploy your Physical AI chatbot backend to production using Railway, Render, or Vercel.

## Pre-Deployment Checklist

- [ ] Backend works locally (ran `test_chat.py` successfully)
- [ ] Ingestion completed (collection created in Qdrant)
- [ ] Environment variables documented
- [ ] Qdrant Cloud account created (if using cloud)
- [ ] OpenAI API key ready
- [ ] (Optional) Neon PostgreSQL database created

## Option 1: Railway.app (Recommended)

Railway is the easiest deployment option with automatic GitHub integration.

### Step 1: Prepare Your Repository

1. Make sure all code is committed to Git:
   ```bash
   git add .
   git commit -m "Add chatbot backend"
   git push origin main
   ```

2. Add a `Procfile` (Railway will use this):
   ```bash
   echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
   ```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and install dependencies

### Step 3: Configure Environment Variables

In Railway dashboard:

1. Click on your project
2. Go to "Variables" tab
3. Add all environment variables from your `.env`:
   ```
   OPENAI_API_KEY=sk-proj-...
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   QDRANT_URL=https://your-cluster.qdrant.tech
   QDRANT_API_KEY=your-qdrant-key
   DATABASE_URL=postgresql://...
   CORS_ORIGINS=https://yourusername.github.io,https://yoursite.com
   ```

4. Click "Deploy"

### Step 4: Verify Deployment

1. Railway will provide a public URL: `https://your-app.railway.app`
2. Test the health endpoint:
   ```bash
   curl https://your-app.railway.app/health
   ```

3. Test a chat request:
   ```bash
   curl -X POST https://your-app.railway.app/chat \
     -H "Content-Type: application/json" \
     -d '{"question": "What is physical AI?"}'
   ```

**Railway Costs:**
- Free tier: $5/month credit (enough for development)
- Pro: $20/month for production use

---

## Option 2: Render.com

Render offers a generous free tier with automatic HTTPS.

### Step 1: Prepare Repository

Same as Railway Option 1, Step 1.

### Step 2: Create Web Service

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `physical-ai-chatbot`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables

In the Render dashboard, add all variables from your `.env`.

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will build and deploy (takes ~5 minutes)
3. You'll get a URL: `https://physical-ai-chatbot.onrender.com`

**Render Costs:**
- Free tier: Available with some limitations (spins down after inactivity)
- Starter: $7/month for always-on service

---

## Option 3: Vercel (Serverless)

Vercel is great for serverless deployment but requires some modifications.

### Step 1: Convert to Serverless

Create `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

Modify `main.py` to export the app:
```python
# At the bottom of main.py
app = app  # Make sure app is exported
```

### Step 2: Deploy to Vercel

```bash
npm install -g vercel
vercel --prod
```

Add environment variables through Vercel dashboard.

**Note**: Serverless has cold start issues. Use Railway or Render for better performance.

---

## Post-Deployment Steps

### 1. Update Docusaurus Frontend

In your `book/docusaurus.config.js`, add:

```javascript
customFields: {
  chatbotApiUrl: 'https://your-app.railway.app',
},
```

Then in `ChatBot/index.tsx`:
```typescript
const CHATBOT_API_URL = process.env.REACT_APP_CHATBOT_API_URL ||
                         'https://your-app.railway.app';
```

### 2. Configure CORS

Update `CORS_ORIGINS` in your deployment:
```
CORS_ORIGINS=https://yourusername.github.io,https://yourcustomdomain.com
```

### 3. Monitor Your Deployment

**Railway:**
- View logs in Railway dashboard
- Monitor metrics (CPU, memory, requests)

**Render:**
- Check logs in "Logs" tab
- Monitor health checks

### 4. Run Ingestion on Production (One-Time)

After deployment, you need to run ingestion once:

**Option A: Local Ingestion (Recommended)**

If using Qdrant Cloud:
```bash
# Set production Qdrant URL locally
export QDRANT_URL=https://your-cluster.qdrant.tech
export QDRANT_API_KEY=your-key
python ingest.py
```

**Option B: Railway Console**

1. Go to Railway dashboard
2. Click "Shell" tab
3. Run:
   ```bash
   python ingest.py
   ```

### 5. Setup Monitoring (Recommended)

**Option A: Built-in Stats**

Check `/stats` endpoint regularly:
```bash
curl https://your-app.railway.app/stats
```

**Option B: External Monitoring**

Use services like:
- [UptimeRobot](https://uptimerobot.com/) - Free uptime monitoring
- [Sentry](https://sentry.io/) - Error tracking
- [LogTail](https://logtail.com/) - Log management

---

## Database Setup (PostgreSQL)

### Using Neon (Recommended)

1. Create database at [neon.tech](https://neon.tech)
2. Copy connection string
3. Add to deployment environment variables
4. Run schema:
   ```bash
   psql "your-connection-string" -f schema.sql
   ```

### Using Railway PostgreSQL

1. In Railway dashboard, click "New" → "Database" → "Add PostgreSQL"
2. Railway will automatically add `DATABASE_URL` to your environment
3. Connect via Railway shell and run:
   ```bash
   psql $DATABASE_URL -f schema.sql
   ```

---

## Deployment Checklist

After deployment, verify:

- [ ] Health check returns `healthy`: `curl https://your-app/health`
- [ ] Chat endpoint works: Test with a question
- [ ] Response time < 5 seconds
- [ ] Sources are being returned correctly
- [ ] Feedback endpoint works
- [ ] Stats endpoint returns data (if database configured)
- [ ] CORS allows your Docusaurus domain
- [ ] Logs show no errors
- [ ] Cold starts < 10 seconds (if serverless)

---

## Troubleshooting

### 502 Bad Gateway

**Problem**: Server not responding

**Solutions**:
- Check logs for startup errors
- Verify `PORT` environment variable is used correctly
- Check if Qdrant is accessible from deployment
- Ensure all dependencies installed

### High Response Times (>5 seconds)

**Problem**: Slow responses

**Solutions**:
- Use `gpt-4o-mini` instead of `gpt-4o`
- Reduce `TOP_K_RESULTS` to 3
- Use Railway/Render (not serverless)
- Check OpenAI API status

### CORS Errors

**Problem**: Frontend can't connect to backend

**Solutions**:
- Add your Docusaurus URL to `CORS_ORIGINS`
- Include both `http://localhost:3000` (dev) and production URL
- Check browser console for exact error

### Out of Memory

**Problem**: Deployment crashes

**Solutions**:
- Upgrade to paid plan with more memory
- Reduce batch sizes in `ingest.py`
- Use streaming responses (implement chunked streaming)

### Cold Start Issues (Vercel/Serverless)

**Problem**: First request takes 10+ seconds

**Solutions**:
- Switch to Railway or Render (always-on)
- Implement connection pooling
- Cache embeddings client

---

## Security Checklist

Before going to production:

- [ ] OpenAI API key stored as environment variable (not in code)
- [ ] Qdrant API key secured
- [ ] Database connection string secured
- [ ] CORS restricted to your domains only
- [ ] Rate limiting enabled (see `MAX_REQUESTS_PER_MINUTE`)
- [ ] HTTPS enabled (automatic on Railway/Render)
- [ ] No sensitive data logged
- [ ] Input validation enabled (Pydantic models)

---

## Scaling Considerations

### For 1000+ Users

**Backend**:
- Upgrade to Railway Pro or Render Starter
- Add Redis for caching frequent questions
- Implement connection pooling for database
- Use `gpt-4o-mini` for cost efficiency

**Vector Database**:
- Upgrade to Qdrant Cloud paid plan
- Enable HNSW indexing for faster search
- Consider sharding by week

**Database**:
- Enable connection pooling
- Add indexes on frequently queried columns
- Consider read replicas

### Cost Optimization

**Current costs (100 queries/day)**:
- OpenAI: ~$10/month
- Railway: $20/month
- Qdrant Cloud: Free tier OK
- Neon: Free tier OK
- **Total**: ~$30/month

**Optimization strategies**:
1. Cache common questions (reduce OpenAI calls by 30-50%)
2. Use `gpt-4o-mini` (5x cheaper than GPT-4)
3. Batch embedding generation
4. Set `max_tokens` limit to reduce output costs

---

## Monitoring & Analytics

### Key Metrics to Track

1. **Response Time**: Should be < 3 seconds
2. **Confidence Score**: Should be > 70% on average
3. **Error Rate**: Should be < 1%
4. **Daily Active Users**: Track growth
5. **Most Asked Questions**: Identify common topics

### Setup Dashboard

Query your PostgreSQL database:

```sql
-- Daily usage
SELECT DATE(created_at), COUNT(*), AVG(confidence), AVG(response_time_ms)
FROM conversations
GROUP BY DATE(created_at)
ORDER BY DATE(created_at) DESC;

-- Popular questions
SELECT question, COUNT(*) as frequency
FROM conversations
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY question
ORDER BY frequency DESC
LIMIT 10;

-- User satisfaction
SELECT AVG(rating), COUNT(*)
FROM feedback
WHERE created_at > NOW() - INTERVAL '7 days';
```

---

## Next Steps

1. **Test Production**: Run full test suite against production URL
2. **Update Frontend**: Point Docusaurus to production API
3. **Monitor**: Set up alerts for downtime/errors
4. **Iterate**: Use feedback to improve responses
5. **Scale**: Add more weeks of content as you create them

## Support

- Railway docs: [docs.railway.app](https://docs.railway.app)
- Render docs: [render.com/docs](https://render.com/docs)
- Qdrant Cloud: [qdrant.tech/documentation](https://qdrant.tech/documentation)
- Neon docs: [neon.tech/docs](https://neon.tech/docs)
