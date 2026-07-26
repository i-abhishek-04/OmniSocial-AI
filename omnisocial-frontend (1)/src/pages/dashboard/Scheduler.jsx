import { useEffect, useState } from 'react';
import {
  Calendar as CalendarIcon,
  List,
  Plus,
  Sparkles,
  Clock,
  Trash2,
  Edit2,
  CheckCircle,
  X,
  MessageSquare,
} from 'lucide-react';
import {
  getScheduledPosts,
  createScheduledPost,
  deleteScheduledPost,
  getBestTimeRecommendations,
} from '../../api/schedulerApi';
import './Scheduler.css';

const AVAILABLE_PLATFORMS = [
  { id: 'youtube', label: 'YouTube', color: '#FF0000' },
  { id: 'instagram', label: 'Instagram', color: '#E1306C' },
  { id: 'github', label: 'GitHub', color: '#ffffff' },
];

const Scheduler = () => {
  const [posts, setPosts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('list'); // 'list' | 'calendar'
  const [showModal, setShowModal] = useState(false);
  const [busy, setBusy] = useState(false);

  // Form State
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedPlatforms, setSelectedPlatforms] = useState(['youtube']);
  const [scheduledAt, setScheduledAt] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const [postsData, recsData] = await Promise.all([
        getScheduledPosts(),
        getBestTimeRecommendations(),
      ]);
      setPosts(postsData);
      setRecommendations(recsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    // Default scheduled time to tomorrow 10:00 AM
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(10, 0, 0, 0);
    setScheduledAt(tomorrow.toISOString().slice(0, 16));
  }, []);

  const handleTogglePlatform = (pId) => {
    if (selectedPlatforms.includes(pId)) {
      if (selectedPlatforms.length > 1) {
        setSelectedPlatforms(selectedPlatforms.filter((p) => p !== pId));
      }
    } else {
      setSelectedPlatforms([...selectedPlatforms, pId]);
    }
  };

  const handleCreatePost = async (e) => {
    e.preventDefault();
    if (!title || !content || !scheduledAt) return;
    setBusy(true);
    try {
      const newPost = await createScheduledPost({
        title,
        content,
        platforms: selectedPlatforms,
        scheduled_at: new Date(scheduledAt).toISOString(),
        status: 'scheduled',
      });
      setPosts([...posts, newPost]);
      setShowModal(false);
      setTitle('');
      setContent('');
    } catch (err) {
      console.error(err);
    } finally {
      setBusy(false);
    }
  };

  const handleDeletePost = async (id) => {
    try {
      await deleteScheduledPost(id);
      setPosts(posts.filter((p) => p.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="dashboard-page scheduler-page">
      <div className="scheduler-topbar">
        <div className="view-toggle">
          <button
            type="button"
            className={`view-btn ${viewMode === 'list' ? 'view-btn--active' : ''}`}
            onClick={() => setViewMode('list')}
          >
            <List size={15} /> Queue List
          </button>
          <button
            type="button"
            className={`view-btn ${viewMode === 'calendar' ? 'view-btn--active' : ''}`}
            onClick={() => setViewMode('calendar')}
          >
            <CalendarIcon size={15} /> Calendar View
          </button>
        </div>

        <button type="button" className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={15} /> Create Scheduled Post
        </button>
      </div>

      {/* AI Recommendations Header Banner */}
      <div className="ai-recs-bar">
        <div className="ai-recs-header">
          <Sparkles size={16} color="#ec4899" />
          AI Best-Time Posting Suggestions
        </div>
        <div className="recs-grid">
          {recommendations.map((rec, i) => (
            <div className="rec-card" key={i}>
              <div className="rec-platform" style={{ color: rec.color }}>
                {rec.display_name}
                <span style={{ fontSize: 10, padding: '1px 5px', borderRadius: 4, background: 'rgba(255,255,255,0.1)', color: '#fff' }}>
                  {rec.confidence} match
                </span>
              </div>
              <div className="rec-time">{rec.recommended_day} @ {rec.recommended_time}</div>
              <div className="rec-reason">{rec.reason}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Posts Queue View */}
      {viewMode === 'list' && (
        <div className="posts-grid">
          {loading ? (
            <div className="dash-state">Loading scheduled posts...</div>
          ) : posts.length === 0 ? (
            <div className="panel" style={{ textAlign: 'center', padding: '40px 20px' }}>
              <CalendarIcon size={40} opacity={0.3} style={{ marginBottom: 12 }} />
              <h3 className="panel__title">No Scheduled Posts</h3>
              <p className="panel__subtitle" style={{ marginBottom: 16 }}>
                Create your first post and schedule it across multiple platforms!
              </p>
              <button type="button" className="btn btn-primary" onClick={() => setShowModal(true)}>
                <Plus size={15} /> Schedule a Post
              </button>
            </div>
          ) : (
            posts.map((post) => (
              <div className="post-card" key={post.id}>
                <div className="post-main-info">
                  <div className="post-title-row">
                    <span className="post-title">{post.title}</span>
                    <span className={`status-badge status-badge--${post.status}`}>
                      {post.status}
                    </span>
                  </div>
                  <div className="post-body">{post.content}</div>
                  <div className="post-footer">
                    <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                      <Clock size={13} />
                      {new Date(post.scheduled_at).toLocaleString([], {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                    <div className="platform-chips">
                      {post.platforms?.map((p) => (
                        <span key={p} className="platform-chip">
                          {p}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="post-actions">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => handleDeletePost(post.id)}
                    style={{ padding: '6px 10px', color: '#ef4444' }}
                    title="Delete Post"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Calendar View Placeholder / Interactive Grid */}
      {viewMode === 'calendar' && (
        <div className="panel" style={{ padding: 24 }}>
          <h3 className="panel__title" style={{ marginBottom: 16 }}>Content Calendar</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 8, textAlign: 'center' }}>
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
              <div key={day} style={{ fontWeight: 600, fontSize: 12, padding: '8px 0', color: 'var(--color-text-muted)', borderBottom: '1px solid var(--color-border)' }}>
                {day}
              </div>
            ))}
            {Array.from({ length: 28 }).map((_, idx) => {
              const dayNum = idx + 1;
              const hasPost = posts.some((p) => new Date(p.scheduled_at).getDate() === dayNum);
              return (
                <div
                  key={idx}
                  style={{
                    height: 80,
                    background: 'rgba(0,0,0,0.2)',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid rgba(255,255,255,0.05)',
                    padding: 6,
                    fontSize: 12,
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                  }}
                >
                  <span style={{ color: 'var(--color-text-muted)', fontWeight: 500 }}>{dayNum}</span>
                  {hasPost && (
                    <span style={{ fontSize: 10, background: 'var(--gradient-primary)', color: '#fff', padding: '2px 4px', borderRadius: 4, textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                      Post Scheduled
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Post Creation Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Schedule New Content</h3>
              <button type="button" onClick={() => setShowModal(false)} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer' }}>
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleCreatePost} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div className="form-group">
                <label>Target Platforms</label>
                <div className="platform-select-group">
                  {AVAILABLE_PLATFORMS.map((p) => {
                    const isSel = selectedPlatforms.includes(p.id);
                    return (
                      <button
                        key={p.id}
                        type="button"
                        className={`platform-toggle-btn ${isSel ? 'platform-toggle-btn--selected' : ''}`}
                        onClick={() => handleTogglePlatform(p.id)}
                      >
                        {p.label}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="form-group">
                <label>Post Title / Topic</label>
                <input
                  type="text"
                  placeholder="e.g. 10 Tips for Better Code Performance"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Content Description / Caption</label>
                <textarea
                  rows={4}
                  placeholder="Write post content, hashtags, links..."
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Schedule Date & Time</label>
                <input
                  type="datetime-local"
                  value={scheduledAt}
                  onChange={(e) => setScheduledAt(e.target.value)}
                  required
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, marginTop: 10 }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={busy}>
                  {busy ? 'Scheduling...' : 'Schedule Post'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Scheduler;
