import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  confidence?: number;
  responseTime?: number;
}

interface Source {
  title: string;
  url: string;
  excerpt: string;
  similarity: number;
}

const CHATBOT_API_URL = process.env.REACT_APP_CHATBOT_API_URL || 'http://localhost:8000';

export default function ChatBot(): JSX.Element {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [weekFilter, setWeekFilter] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: inputValue,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Build conversation history
      const conversationHistory = messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

      const response = await fetch(`${CHATBOT_API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: inputValue,
          conversation_history: conversationHistory,
          week_filter: weekFilter || null,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        confidence: data.confidence,
        responseTime: data.response_time_ms,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);

      const errorMessage: Message = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.message}. Please make sure the chatbot backend is running at ${CHATBOT_API_URL}.`,
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedback = async (messageIndex: number, rating: number) => {
    const message = messages[messageIndex];
    if (message.role !== 'assistant') return;

    const userQuestion = messages[messageIndex - 1]?.content || '';

    try {
      await fetch(`${CHATBOT_API_URL}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: userQuestion,
          answer: message.content,
          rating,
        }),
      });

      alert('Thank you for your feedback!');
    } catch (error) {
      console.error('Feedback error:', error);
    }
  };

  const clearConversation = () => {
    setMessages([]);
    setWeekFilter('');
  };

  // Handle selected text query (bonus feature)
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const selectedText = selection?.toString().trim();

      if (selectedText && selectedText.length > 10 && selectedText.length < 500) {
        const askButton = document.getElementById('ask-about-selection');
        if (askButton) {
          askButton.style.display = 'block';
          askButton.onclick = () => {
            setInputValue(`Explain: "${selectedText}"`);
            setIsOpen(true);
            askButton.style.display = 'none';
          };
        }
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  return (
    <>
      {/* Floating chat button */}
      <button
        className={styles.chatButton}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chatbot"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>Physical AI Assistant</h3>
            <div className={styles.headerActions}>
              <select
                value={weekFilter}
                onChange={(e) => setWeekFilter(e.target.value)}
                className={styles.weekFilter}
              >
                <option value="">All Weeks</option>
                <option value="week-01-02">Week 1-2</option>
                <option value="week-03-04">Week 3-4</option>
                <option value="week-05-06">Week 5-6</option>
              </select>
              <button onClick={clearConversation} className={styles.clearButton}>
                Clear
              </button>
            </div>
          </div>

          <div className={styles.messagesContainer}>
            {messages.length === 0 && (
              <div className={styles.welcomeMessage}>
                <p>👋 Hi! I'm your Physical AI teaching assistant.</p>
                <p>Ask me anything about the course content!</p>
                <div className={styles.suggestions}>
                  <button onClick={() => setInputValue('What is physical AI?')}>
                    What is physical AI?
                  </button>
                  <button onClick={() => setInputValue('Explain embodied intelligence')}>
                    Explain embodied intelligence
                  </button>
                  <button onClick={() => setInputValue('What sensors do humanoid robots use?')}>
                    What sensors do robots use?
                  </button>
                </div>
              </div>
            )}

            {messages.map((message, index) => (
              <div key={index} className={`${styles.message} ${styles[message.role]}`}>
                <div className={styles.messageContent}>
                  {message.content}

                  {message.sources && message.sources.length > 0 && (
                    <div className={styles.sources}>
                      <h4>Sources:</h4>
                      {message.sources.map((source, idx) => (
                        <a
                          key={idx}
                          href={source.url}
                          className={styles.source}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          <strong>{source.title}</strong>
                          <span className={styles.similarity}>
                            {(source.similarity * 100).toFixed(0)}% relevant
                          </span>
                          <p>{source.excerpt}</p>
                        </a>
                      ))}
                    </div>
                  )}

                  {message.confidence !== undefined && (
                    <div className={styles.metadata}>
                      <span>Confidence: {(message.confidence * 100).toFixed(0)}%</span>
                      {message.responseTime && (
                        <span>Response time: {message.responseTime}ms</span>
                      )}
                    </div>
                  )}
                </div>

                {message.role === 'assistant' && (
                  <div className={styles.feedbackButtons}>
                    <button
                      onClick={() => handleFeedback(index, 5)}
                      title="Helpful"
                      aria-label="Thumbs up"
                    >
                      👍
                    </button>
                    <button
                      onClick={() => handleFeedback(index, 1)}
                      title="Not helpful"
                      aria-label="Thumbs down"
                    >
                      👎
                    </button>
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.loadingDots}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className={styles.inputForm}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question about Physical AI..."
              className={styles.input}
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading || !inputValue.trim()} className={styles.sendButton}>
              {isLoading ? '...' : '➤'}
            </button>
          </form>
        </div>
      )}

      {/* Hidden button for selected text queries */}
      <button id="ask-about-selection" style={{ display: 'none' }} className={styles.selectionButton}>
        Ask about this
      </button>
    </>
  );
}
