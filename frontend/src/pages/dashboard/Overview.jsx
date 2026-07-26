import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Users, TrendingUp, Wallet, Percent, ArrowUpRight } from 'lucide-react';
import { getOverview } from '../../api/analyticsApi';
import { getPlatformMeta } from '../../data/platformIcons';
import StatCard from '../../components/StatCard/StatCard';
import LineChart from '../../components/charts/LineChart';
import './Dashboard.css';

const formatCompact = (n) => new Intl.NumberFormat('en', { notation: 'compact', maximumFractionDigits: 2 }).format(n);
const formatCurrency = (n) => `$${new Intl.NumberFormat('en', { maximumFractionDigits: 0 }).format(n)}`;

const Overview = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getOverview()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="dash-state">Loading your dashboard...</div>;
  if (error) return <div className="dash-state dash-state--error">{error}</div>;
  if (!data) return null;

  const trendPoints = data.follower_trend.map((p) => ({
    label: new Date(p.date).toLocaleDateString('en', { month: 'short', day: 'numeric' }),
    value: p.followers,
  }));

  return (
    <div className="dashboard-page">
      <div className="stat-grid">
        <StatCard icon={Users} label="Total Followers" value={formatCompact(data.total_followers)} delta={data.avg_growth_30d} deltaPositive={data.avg_growth_30d >= 0} />
        <StatCard icon={Wallet} label="Monthly Revenue" value={formatCurrency(data.total_monthly_revenue)} delta={12.4} />
        <StatCard icon={Percent} label="Avg. Engagement" value={`${data.total_engagement_rate}%`} />
        <StatCard icon={TrendingUp} label="Connected Platforms" value={`${data.connected_platforms}/${data.total_platforms}`} />
      </div>

      <div className="panel">
        <div className="panel__header">
          <div>
            <h3 className="panel__title">Follower Growth</h3>
            <p className="panel__subtitle">Combined across all connected platforms &middot; last 30 days</p>
          </div>
          {data.top_platform && <span className="panel__pill">Top: {data.top_platform}</span>}
        </div>
        <LineChart data={trendPoints} formatValue={(v) => formatCompact(v)} />
      </div>

      <div className="panel">
        <div className="panel__header">
          <div>
            <h3 className="panel__title">Platforms</h3>
            <p className="panel__subtitle">Your presence across all 7 supported platforms</p>
          </div>
          <Link to="/dashboard/platforms" className="panel__link">
            Manage all <ArrowUpRight size={14} />
          </Link>
        </div>

        <div className="platform-grid">
          {data.platforms.map((p) => {
            const meta = getPlatformMeta(p.platform);
            const Icon = meta?.icon;
            return (
              <Link to={`/dashboard/platforms/${p.platform}`} key={p.platform} className="platform-tile">
                <div className="platform-tile__top">
                  <span className="platform-tile__icon" style={{ color: meta?.color }}>
                    {Icon && <Icon size={20} />}
                  </span>
                  {!p.connected && <span className="platform-tile__badge">Not connected</span>}
                </div>
                <span className="platform-tile__name">
                  {p.display_name}
                  {p.is_live && <span className="platform-tile__live-tag">Live</span>}
                </span>
                {p.connected ? (
                  <>
                    <span className="platform-tile__value">{formatCompact(p.followers)} followers</span>
                    <span className={`platform-tile__growth ${p.growth_30d >= 0 ? 'up' : 'down'}`}>
                      {p.growth_30d >= 0 ? '+' : ''}{p.growth_30d}% (30d)
                    </span>
                  </>
                ) : (
                  <span className="platform-tile__connect">Connect &rarr;</span>
                )}
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Overview;
