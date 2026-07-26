import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { updateProfile } from '../../api/authApi';
import './Dashboard.css';

const NICHES = ['Lifestyle', 'Gaming', 'Tech', 'Beauty', 'Fitness', 'Finance', 'Food', 'Travel', 'Comedy'];

const Settings = () => {
  const { user, updateUser } = useAuth();
  const [form, setForm] = useState({ full_name: user?.full_name || '', niche: user?.niche || 'Lifestyle' });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    setError('');
    try {
      const updated = await updateProfile(form);
      updateUser(updated);
      setMessage('Profile updated');
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="dashboard-page">
      <div className="panel">
        <div className="panel__header">
          <div>
            <h3 className="panel__title">Profile Settings</h3>
            <p className="panel__subtitle">{user?.email}</p>
          </div>
        </div>

        <form className="settings-form" onSubmit={handleSubmit}>
          {message && <div className="auth-error" style={{ color: '#4ade80', background: 'rgba(74,222,128,0.1)', borderColor: 'rgba(74,222,128,0.3)' }}>{message}</div>}
          {error && <div className="auth-error">{error}</div>}

          <div className="auth-field">
            <label htmlFor="full_name">Full name</label>
            <input
              id="full_name"
              value={form.full_name}
              onChange={(e) => setForm({ ...form, full_name: e.target.value })}
            />
          </div>

          <div className="auth-field">
            <label htmlFor="niche">Niche</label>
            <select
              id="niche"
              value={form.niche}
              onChange={(e) => setForm({ ...form, niche: e.target.value })}
              style={{
                background: 'var(--color-bg-elevated)',
                border: '1px solid var(--color-border)',
                borderRadius: 'var(--radius-sm)',
                padding: '12px 14px',
                color: 'var(--color-white)',
                fontSize: '14.5px',
              }}
            >
              {NICHES.map((n) => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>

          <button type="submit" className="btn btn-primary auth-submit" disabled={saving}>
            {saving ? 'Saving...' : 'Save changes'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Settings;
