-- PostgreSQL schema for Physical AI Chatbot
-- Run this on your Neon PostgreSQL database

-- Conversations table: stores all chat interactions
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    sources JSONB,
    confidence FLOAT,
    response_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Indexes for analytics
    INDEX idx_created_at (created_at DESC),
    INDEX idx_confidence (confidence)
);

-- Feedback table: stores user ratings and comments
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Indexes
    INDEX idx_rating (rating),
    INDEX idx_created_at (created_at DESC)
);

-- Optional: Create a view for analytics
CREATE OR REPLACE VIEW conversation_analytics AS
SELECT
    DATE(created_at) as date,
    COUNT(*) as total_questions,
    AVG(confidence) as avg_confidence,
    AVG(response_time_ms) as avg_response_time_ms,
    MIN(response_time_ms) as min_response_time_ms,
    MAX(response_time_ms) as max_response_time_ms
FROM conversations
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Optional: Create a view for feedback analytics
CREATE OR REPLACE VIEW feedback_analytics AS
SELECT
    DATE(created_at) as date,
    COUNT(*) as total_feedback,
    AVG(rating) as avg_rating,
    COUNT(CASE WHEN rating >= 4 THEN 1 END) as positive_feedback,
    COUNT(CASE WHEN rating <= 2 THEN 1 END) as negative_feedback
FROM feedback
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Comments
COMMENT ON TABLE conversations IS 'Stores all chatbot conversations with questions, answers, sources, and performance metrics';
COMMENT ON TABLE feedback IS 'Stores user feedback ratings and comments for continuous improvement';
COMMENT ON VIEW conversation_analytics IS 'Daily aggregated metrics for conversation performance';
COMMENT ON VIEW feedback_analytics IS 'Daily aggregated metrics for user feedback';

-- Example queries:

-- Get recent conversations with high confidence
-- SELECT question, answer, confidence, created_at
-- FROM conversations
-- WHERE confidence > 0.8
-- ORDER BY created_at DESC
-- LIMIT 10;

-- Get average rating by day
-- SELECT * FROM feedback_analytics WHERE date > CURRENT_DATE - INTERVAL '7 days';

-- Find common questions
-- SELECT question, COUNT(*) as frequency
-- FROM conversations
-- WHERE created_at > CURRENT_DATE - INTERVAL '30 days'
-- GROUP BY question
-- ORDER BY frequency DESC
-- LIMIT 20;

-- Performance over time
-- SELECT * FROM conversation_analytics WHERE date > CURRENT_DATE - INTERVAL '30 days';
