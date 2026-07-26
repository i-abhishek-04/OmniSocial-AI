import { useEffect, useRef, useState } from 'react';
import { Send, Bot } from 'lucide-react';
import { getChatHistory, sendChatMessage } from '../../api/chatApi';
import './Dashboard.css';
import './Chat.css';

const SUGGESTIONS = [
  "What's my best platform?",
  'How is my revenue this month?',
  "What's my growth trend?",
  'How is my engagement?',
];

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const scrollRef = useRef(null);

  useEffect(() => {
    getChatHistory()
      .then(setMessages)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (text) => {
    const content = (text ?? input).trim();
    if (!content || sending) return;
    setInput('');
    setError('');
    setMessages((prev) => [
      ...prev,
      { id: `temp-${Date.now()}`, role: 'user', content, created_at: new Date().toISOString() },
    ]);
    setSending(true);
    try {
      const reply = await sendChatMessage(content);
      setMessages((prev) => [...prev, reply]);
    } catch (err) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSend();
  };

  return (
    <div className="dashboard-page">
      <div className="panel chat-panel">
        <div className="panel__header">
          <div>
            <h3 className="panel__title">AI Assistant</h3>
            <p className="panel__subtitle">Ask about your growth, revenue, or any connected platform</p>
          </div>
        </div>

        <div className="chat-messages" ref={scrollRef}>
          {loading && <div className="chat-empty">Loading conversation...</div>}
          {!loading && messages.length === 0 && (
            <div className="chat-empty">
              <Bot size={28} style={{ marginBottom: 10, opacity: 0.6 }} />
              <p>Ask me anything about your analytics.</p>
            </div>
          )}
          {messages.map((m) => (
            <div key={m.id} className={`chat-bubble chat-bubble--${m.role}`}>
              {m.content}
            </div>
          ))}
          {sending && <div className="chat-bubble chat-bubble--assistant">Thinking...</div>}
        </div>

        {error && <div className="auth-error" style={{ marginTop: 10 }}>{error}</div>}

        <div className="chat-suggestions">
          {SUGGESTIONS.map((s) => (
            <button type="button" key={s} className="chat-suggestion" onClick={() => handleSend(s)}>
              {s}
            </button>
          ))}
        </div>

        <form className="chat-input-row" onSubmit={handleSubmit}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about your growth, revenue, or a platform..."
          />
          <button type="submit" className="btn btn-primary" disabled={sending}>
            <Send size={16} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default Chat;
