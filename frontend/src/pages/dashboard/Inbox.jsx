import { useEffect, useState } from 'react';
import {
  Inbox as InboxIcon,
  Search,
  Filter,
  Send,
  MessageSquare,
  Sparkles,
  CheckCircle,
} from 'lucide-react';
import { FaYoutube, FaGithub, FaReddit, FaInstagram } from 'react-icons/fa6';
import { SiDevdotto } from 'react-icons/si';
import { getInboxMessages } from '../../api/inboxApi';
import './Inbox.css';

const PLATFORM_ICONS = {
  youtube: { icon: FaYoutube, color: '#FF0000', label: 'YouTube' },
  instagram: { icon: FaInstagram, color: '#E1306C', label: 'Instagram' },
  github: { icon: FaGithub, color: '#ffffff', label: 'GitHub' },
  reddit: { icon: FaReddit, color: '#FF4500', label: 'Reddit' },
  devto: { icon: SiDevdotto, color: '#0A0A0A', label: 'Dev.to' },
};

const Inbox = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPlatform, setSelectedPlatform] = useState('all');
  const [unreadOnly, setUnreadOnly] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedMessage, setSelectedMessage] = useState(null);
  const [replyText, setReplyText] = useState('');
  const [replySuccess, setReplySuccess] = useState(false);

  const loadMessages = async () => {
    setLoading(true);
    try {
      const data = await getInboxMessages(selectedPlatform, unreadOnly);
      setMessages(data);
      if (data.length > 0) {
        setSelectedMessage(data[0]);
      } else {
        setSelectedMessage(null);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMessages();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedPlatform, unreadOnly]);

  const filteredMessages = messages.filter((m) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      m.author.toLowerCase().includes(q) ||
      m.content.toLowerCase().includes(q) ||
      m.post_title.toLowerCase().includes(q)
    );
  });

  const handleSendReply = (e) => {
    e.preventDefault();
    if (!replyText.trim()) return;
    setReplySuccess(true);
    setTimeout(() => {
      setReplyText('');
      setReplySuccess(false);
    }, 2000);
  };

  return (
    <div className="dashboard-page inbox-page">
      <div className="inbox-controls">
        <div className="inbox-filters">
          <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--color-text-muted)', marginRight: 4 }}>
            Filter:
          </span>
          {['all', 'youtube', 'instagram', 'github'].map((p) => {
            const isActive = selectedPlatform === p;
            const meta = PLATFORM_ICONS[p];
            return (
              <button
                key={p}
                type="button"
                className={`filter-pill ${isActive ? 'filter-pill--active' : ''}`}
                onClick={() => setSelectedPlatform(p)}
              >
                {p === 'all' ? <Filter size={13} /> : meta?.icon && <meta.icon size={13} style={{ color: isActive ? '#fff' : meta.color }} />}
                {p === 'all' ? 'All Platforms' : meta?.label || p}
              </button>
            );
          })}
          <button
            type="button"
            className={`filter-pill ${unreadOnly ? 'filter-pill--active' : ''}`}
            onClick={() => setUnreadOnly(!unreadOnly)}
            style={{ marginLeft: 8 }}
          >
            Unread only
          </button>
        </div>

        <div className="inbox-search-box">
          <Search size={15} color="var(--color-text-muted)" />
          <input
            type="text"
            placeholder="Search messages, authors..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="inbox-layout">
        {/* Message List Panel */}
        <div className="inbox-list-panel">
          <div className="inbox-list-header">
            <span>Conversations ({filteredMessages.length})</span>
            <span style={{ fontSize: 12, color: 'var(--color-text-muted)' }}>
              {unreadOnly ? 'Unread' : 'All'}
            </span>
          </div>

          <div className="inbox-list">
            {loading ? (
              <div className="dash-state">Loading messages...</div>
            ) : filteredMessages.length === 0 ? (
              <div className="dash-state">No messages found.</div>
            ) : (
              filteredMessages.map((msg) => {
                const isSelected = selectedMessage?.id === msg.id;
                const meta = PLATFORM_ICONS[msg.platform];
                return (
                  <div
                    key={msg.id}
                    className={`inbox-item ${isSelected ? 'inbox-item--selected' : ''} ${
                      msg.unread ? 'inbox-item--unread' : ''
                    }`}
                    onClick={() => setSelectedMessage(msg)}
                  >
                    <img
                      src={msg.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80'}
                      alt={msg.author}
                      className="inbox-avatar"
                    />
                    <div className="inbox-item-content">
                      <div className="inbox-item-meta">
                        <span className="inbox-item-author">{msg.author}</span>
                        <span className="inbox-item-date">
                          {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                      <div className="inbox-item-snippet">{msg.content}</div>
                      <span className="inbox-item-badge">
                        {meta?.icon && <meta.icon size={11} color={meta.color} />}
                        {meta?.label || msg.platform} &bull; {msg.type || 'comment'}
                      </span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Message Detail Panel */}
        <div className="inbox-detail-panel">
          {selectedMessage ? (
            <>
              <div>
                <div className="detail-header-card">
                  <img
                    src={selectedMessage.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80'}
                    alt={selectedMessage.author}
                    className="detail-avatar"
                  />
                  <div className="detail-author-info">
                    <h3>{selectedMessage.author}</h3>
                    <div className="detail-context">
                      On <strong style={{ color: '#fff' }}>{selectedMessage.post_title}</strong> &bull;{' '}
                      {new Date(selectedMessage.created_at).toLocaleString()}
                    </div>
                  </div>
                </div>

                <div className="detail-body">{selectedMessage.content}</div>
              </div>

              <form className="reply-box" onSubmit={handleSendReply}>
                <textarea
                  placeholder={`Reply to ${selectedMessage.author} on ${
                    PLATFORM_ICONS[selectedMessage.platform]?.label || selectedMessage.platform
                  }...`}
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                />
                <div className="reply-actions">
                  {replySuccess && (
                    <span style={{ fontSize: 13, color: '#22c55e', display: 'flex', alignItems: 'center', gap: 4 }}>
                      <CheckCircle size={14} /> Sent reply!
                    </span>
                  )}
                  <button type="submit" className="btn btn-primary" disabled={!replyText.trim()}>
                    <Send size={14} /> Send Reply
                  </button>
                </div>
              </form>
            </>
          ) : (
            <div className="inbox-detail-empty">
              <InboxIcon size={44} opacity={0.4} />
              <p>Select a message from the list to view and reply.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Inbox;
