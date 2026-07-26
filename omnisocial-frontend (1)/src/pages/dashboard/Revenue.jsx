import { useEffect, useState } from 'react';
import { getRevenue } from '../../api/analyticsApi';
import BarChart from '../../components/charts/BarChart';
import './Dashboard.css';

const formatCurrency = (n) => `$${new Intl.NumberFormat('en', { maximumFractionDigits: 0 }).format(n)}`;

const Revenue = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    getRevenue()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="dash-state">Loading revenue...</div>;
  if (error) return <div className="dash-state dash-state--error">{error}</div>;
  if (!data) return null;

  const monthlyBars = data.months.map((m) => ({ label: m.month.split(' ')[0], value: m.total }));

  return (
    <div className="dashboard-page">
      <div className="panel">
        <div className="revenue-summary">
          <div className="revenue-summary__block">
            <span className="revenue-summary__value">{formatCurrency(data.total_this_month)}</span>
            <span className="revenue-summary__label">This month</span>
          </div>
          <div className="revenue-summary__block">
            <span className="revenue-summary__value">{formatCurrency(data.total_last_month)}</span>
            <span className="revenue-summary__label">Last month</span>
          </div>
          <div className="revenue-summary__block">
            <span
              className="revenue-summary__value"
              style={{ color: data.change_pct >= 0 ? '#4ade80' : '#f87171' }}
            >
              {data.change_pct >= 0 ? '+' : ''}{data.change_pct}%
            </span>
            <span className="revenue-summary__label">Month over month</span>
          </div>
        </div>
      </div>

      <div className="panel">
        <div className="panel__header">
          <div>
            <h3 className="panel__title">Revenue by Month</h3>
            <p className="panel__subtitle">Last 6 months, combined across connected platforms</p>
          </div>
        </div>
        <BarChart data={monthlyBars} formatValue={formatCurrency} />
      </div>

      <div className="panel">
        <div className="panel__header">
          <div>
            <h3 className="panel__title">This Month by Platform</h3>
            <p className="panel__subtitle">Estimated revenue breakdown</p>
          </div>
        </div>
        {data.breakdown_this_month.length === 0 ? (
          <div className="empty-state">Connect a platform to start tracking revenue.</div>
        ) : (
          <table className="revenue-table">
            <thead>
              <tr>
                <th>Platform</th>
                <th>Est. Revenue</th>
                <th>% of Total</th>
              </tr>
            </thead>
            <tbody>
              {data.breakdown_this_month
                .slice()
                .sort((a, b) => b.amount - a.amount)
                .map((row) => (
                  <tr key={row.platform}>
                    <td>
                      <span className="revenue-table__platform">
                        <span className="revenue-table__dot" style={{ background: row.color }} />
                        {row.display_name}
                      </span>
                    </td>
                    <td>{formatCurrency(row.amount)}</td>
                    <td>{data.total_this_month ? ((row.amount / data.total_this_month) * 100).toFixed(1) : 0}%</td>
                  </tr>
                ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Revenue;
