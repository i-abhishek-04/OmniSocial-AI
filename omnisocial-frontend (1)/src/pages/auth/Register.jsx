import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Layers } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import './Auth.css';

const NICHES = ['Lifestyle', 'Gaming', 'Tech', 'Beauty', 'Fitness', 'Finance', 'Food', 'Travel', 'Comedy'];

const Register = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: '', email: '', password: '', niche: 'Lifestyle' });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await register(form);
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <Link to="/" className="auth-card__logo">
          <span className="auth-card__logo-icon">
            <Layers size={16} strokeWidth={2.5} />
          </span>
          OmniSocial AI
        </Link>
        <h1 className="auth-card__title">Create your account</h1>
        <p className="auth-card__subtitle">
          Connect all 7 platforms and see everything in one dashboard.
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          {error && <div className="auth-error">{error}</div>}
          <div className="auth-field">
            <label htmlFor="full_name">Full name</label>
            <input
              id="full_name"
              name="full_name"
              type="text"
              required
              value={form.full_name}
              onChange={handleChange}
              placeholder="Alex Rivera"
            />
          </div>
          <div className="auth-field">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={form.email}
              onChange={handleChange}
              placeholder="you@example.com"
            />
          </div>
          <div className="auth-field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="new-password"
              required
              minLength={8}
              value={form.password}
              onChange={handleChange}
              placeholder="At least 8 characters"
            />
          </div>
          <div className="auth-field">
            <label htmlFor="niche">Niche</label>
            <select
              id="niche"
              name="niche"
              value={form.niche}
              onChange={handleChange}
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
          <button type="submit" className="btn btn-primary auth-submit" disabled={submitting}>
            {submitting ? 'Creating account...' : 'Create free account'}
          </button>
        </form>

        <p className="auth-card__footer">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
