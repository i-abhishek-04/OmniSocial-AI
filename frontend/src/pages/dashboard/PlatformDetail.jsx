import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Link2, Unlink, Lock } from 'lucide-react';
import { getPlatformDetail, connectPlatform, disconnectPlatform } from '../../api/analyticsApi';
import { getPlatformMeta } from '../../data/platformIcons';
import StatCard from '../../components/StatCard/StatCard';
import LineChart from '../../components/charts/LineChart';
import { Users, Eye, Percent, Wallet } from 'lucide-react';
import './Dashboard.css';

const formatCompact = (n) => new Intl.NumberFormat('en', { notation: 'compact', maximumFractionDigits: 2 }).format(n);
const formatCurrency = (n) => `$${new Intl.NumberFormat('en', { maximumFractionDigits: 0 }).format(n)}`;

const PlatformDetail = () => {
  const { platform } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [handle, setHandle] = useState('');
  const [busy, setBusy] = useState(false);

  const load = () => {
    setLoading(true);
    getPlatformDetail(platform)
      .then((d) => {
        setData(d);
        setHandle(d.handle?.replace('@', '') || '');
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [platform]);

  const handleConnect = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      const updated = await connectPlatform(platform, `@${handle.replace('@', '')}`);
      setData(updated);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  const handleDisconnect = async () => {
    setBusy(true);
    try {
      const updated = await disconnectPlatform(platform);
      setData(updated);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  if (loading) return <div className="dash-state">Loading...</div>;
  if (error) return <div className="dash-state dash-state--error">{error}</div>;
  if (!data) return null;

  const meta = getPlatformMeta(data.platform);
  const Icon = meta?.icon;

  const trendPoints = data.timeseries.map((p) => ({
    label: new Date(p.date).toLocaleDateString('en', { month: 'short', day: 'numeric' }),
    value: p.followers,
  }));

  return (
    <div className="dashboard-page">
      <Link to="/dashboard/platforms" className="panel__link" style={{ marginBottom: 4 }}>
        <ArrowLeft size={14} /> Back to platforms
      </Link>

      <div className="detail-header">
        <span className="detail-header__icon" style={{ color: meta?.color }}>
          {Icon && <Icon size={26} />}
        </span>
        <div>
          <h2 className="detail-header__title">
            {data.display_name}
            {data.is_live && <span className="platform-tile__live-tag" style={{ marginLeft: 8 }}>Live</span>}
          </h2>
          <span className="detail-header__handle">{data.connected ? data.handle : 'Not connected'}</span>
        </div>

        <div className="detail-actions">
          {data.connected ? (
            <button type="button" className="btn btn-secondary" onClick={handleDisconnect} disabled={busy}>
              <Unlink size={15} /> Disconnect
            </button>
          ) : null}
        </div>
      </div>

      {!data.connected && data.is_supported && (
        <div className="panel">
          <h3 className="panel__title" style={{ marginBottom: 12 }}>Connect {data.display_name}</h3>
          <p className="panel__subtitle" style={{ marginBottom: 16 }}>
            {platform === 'youtube'
              ? 'Enter a real @handle or channel ID to pull live subscriber, view, and video counts from YouTube (falls back to demo data if the channel can\u2019t be found).'
              : <>Enter a real public {data.display_name} username to pull live stats. Falls back to demo
                data if the profile can&apos;t be found.</>}
          </p>
          <form className="connect-form" onSubmit={handleConnect}>
            <input
              value={handle}
              onChange={(e) => setHandle(e.target.value)}
              placeholder="your-handle"
              required
            />
            <button type="submit" className="btn btn-primary" disabled={busy}>
              <Link2 size={15} /> {busy ? 'Connecting...' : 'Connect'}
            </button>
          </form>
        </div>
      )}

      {!data.is_supported && (
        <div className="panel platform-tile--disabled">
          <div className="panel__header">
            <div>
              <h3 className="panel__title">Integration Coming Soon</h3>
              <p className="panel__subtitle">{data.coming_soon_message}</p>
            </div>
          </div>
          <button type="button" className="platform-tile__connect-btn" disabled>
            <Lock size={13} /> Connect
          </button>
        </div>
      )}

      {data.connected && (
        <>
          <div className="stat-grid">
            <StatCard icon={Users} label="Followers" value={formatCompact(data.followers)} delta={data.growth_30d} deltaPositive={data.growth_30d >= 0} />
            <StatCard icon={Eye} label="Avg. Views / Post" value={formatCompact(data.avg_views)} />
            <StatCard icon={Percent} label="Engagement Rate" value={`${data.engagement_rate}%`} />
            <StatCard icon={Wallet} label="Est. Monthly Revenue" value={formatCurrency(data.monthly_revenue)} />
          </div>

          <div className="panel">
            <div className="panel__header">
              <div>
                <h3 className="panel__title">Follower Growth</h3>
                <p className="panel__subtitle">Last 30 days on {data.display_name}</p>
              </div>
            </div>
            <LineChart data={trendPoints} color={meta?.color} formatValue={formatCompact} />
          </div>
        </>
      )}
    </div>
  );
};

export default PlatformDetail;
