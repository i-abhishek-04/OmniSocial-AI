import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Lock } from 'lucide-react';
import { getPlatforms } from '../../api/analyticsApi';
import { getPlatformMeta } from '../../data/platformIcons';
import './Dashboard.css';

const formatCompact = (n) => new Intl.NumberFormat('en', { notation: 'compact', maximumFractionDigits: 2 }).format(n);

const Platforms = () => {
  const [platforms, setPlatforms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    getPlatforms()
      .then(setPlatforms)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="dash-state">Loading platforms...</div>;
  if (error) return <div className="dash-state dash-state--error">{error}</div>;

  const supported = platforms.filter((p) => p.is_supported);
  const comingSoon = platforms.filter((p) => !p.is_supported);

  return (
    <div className="dashboard-page">
      <div className="panel">
        <div className="panel__header">
          <div>
            <h3 className="panel__title">All Platforms</h3>
            <p className="panel__subtitle">
              Connect or manage your {supported.length} supported platforms
              {comingSoon.length > 0 && ` \u2014 ${comingSoon.length} more coming soon`}
            </p>
          </div>
        </div>
        <div className="platform-grid">
          {supported.map((p) => {
            const meta = getPlatformMeta(p.platform);
            const Icon = meta?.icon;
            return (
              <Link to={`/dashboard/platforms/${p.platform}`} key={p.platform} className="platform-tile">
                <div className="platform-tile__top">
                  <span className="platform-tile__icon" style={{ color: meta?.color }}>
                    {Icon && <Icon size={20} />}
                  </span>
                  <span
                    className="platform-tile__badge"
                    style={p.connected ? { color: '#4ade80', borderColor: 'rgba(74,222,128,0.3)' } : undefined}
                  >
                    {p.connected ? 'Connected' : 'Not connected'}
                  </span>
                </div>
                <span className="platform-tile__name">
                  {p.display_name}
                  {p.is_live && <span className="platform-tile__live-tag">Live</span>}
                </span>
                {p.connected ? (
                  <>
                    <span className="platform-tile__value">{formatCompact(p.followers)} followers</span>
                    <span className="platform-tile__value">${p.monthly_revenue.toFixed(0)}/mo est.</span>
                  </>
                ) : (
                  <span className="platform-tile__connect">Connect &rarr;</span>
                )}
              </Link>
            );
          })}
        </div>
      </div>

      {comingSoon.length > 0 && (
        <div className="panel">
          <div className="panel__header">
            <div>
              <h3 className="panel__title">Coming Soon</h3>
              <p className="panel__subtitle">
                These integrations are on our roadmap and already wired into our provider architecture
              </p>
            </div>
          </div>
          <div className="platform-grid">
            {comingSoon.map((p) => {
              const meta = getPlatformMeta(p.platform);
              const Icon = meta?.icon;
              return (
                <div className="platform-tile platform-tile--disabled" key={p.platform}>
                  <div className="platform-tile__top">
                    <span className="platform-tile__icon" style={{ color: meta?.color }}>
                      {Icon && <Icon size={20} />}
                    </span>
                    <span className="platform-tile__badge platform-tile__badge--soon">Coming Soon</span>
                  </div>
                  <span className="platform-tile__name">{p.display_name}</span>
                  <p className="platform-tile__coming-soon-text">{p.coming_soon_message}</p>
                  <button type="button" className="platform-tile__connect-btn" disabled>
                    <Lock size={13} /> Connect
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default Platforms;
