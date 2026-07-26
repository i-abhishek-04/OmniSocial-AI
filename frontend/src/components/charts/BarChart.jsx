/**
 * Lightweight dependency-free bar chart. Takes an array of
 * { label, value, color? }.
 */
import './charts.css';

const BarChart = ({ data, height = 220, formatValue = (v) => v }) => {
  if (!data || data.length === 0) {
    return <div className="chart-empty">No data yet</div>;
  }

  const max = Math.max(...data.map((d) => d.value), 1);

  return (
    <div className="bar-chart" style={{ height }}>
      {data.map((d, i) => (
        <div className="bar-chart__col" key={i}>
          <div className="bar-chart__track">
            <div
              className="bar-chart__bar"
              style={{
                height: `${(d.value / max) * 100}%`,
                background: d.color || 'var(--gradient-primary)',
              }}
              title={`${d.label}: ${formatValue(d.value)}`}
            />
          </div>
          <span className="bar-chart__label">{d.label}</span>
        </div>
      ))}
    </div>
  );
};

export default BarChart;
