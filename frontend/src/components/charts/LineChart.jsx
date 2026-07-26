/**
 * Lightweight dependency-free SVG line chart with an area fill and hover
 * tooltip. Takes an array of { label, value } points.
 */
import { useState } from 'react';
import './charts.css';

const LineChart = ({ data, height = 240, color = 'var(--color-primary)', formatValue = (v) => v }) => {
  const [hoverIndex, setHoverIndex] = useState(null);

  if (!data || data.length === 0) {
    return <div className="chart-empty">No data yet</div>;
  }

  const width = 100;
  const values = data.map((d) => d.value);
  const max = Math.max(...values, 1);
  const min = Math.min(...values, 0);
  const range = max - min || 1;

  const points = data.map((d, i) => {
    const x = (i / (data.length - 1 || 1)) * width;
    const y = 100 - ((d.value - min) / range) * 100;
    return { x, y, ...d };
  });

  const linePath = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
  const areaPath = `${linePath} L ${width} 100 L 0 100 Z`;

  const active = hoverIndex !== null ? points[hoverIndex] : null;

  return (
    <div className="line-chart" style={{ height }}>
      <svg viewBox={`0 0 ${width} 100`} preserveAspectRatio="none" className="line-chart__svg">
        <defs>
          <linearGradient id="lineChartFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity="0.35" />
            <stop offset="100%" stopColor={color} stopOpacity="0" />
          </linearGradient>
        </defs>
        <path d={areaPath} fill="url(#lineChartFill)" stroke="none" />
        <path d={linePath} fill="none" stroke={color} strokeWidth="1.5" vectorEffect="non-scaling-stroke" />
        {points.map((p, i) => (
          <rect
            key={i}
            x={p.x - width / data.length / 2}
            y={0}
            width={width / data.length}
            height={100}
            fill="transparent"
            onMouseEnter={() => setHoverIndex(i)}
            onMouseLeave={() => setHoverIndex(null)}
          />
        ))}
        {active && (
          <circle cx={active.x} cy={active.y} r="1.6" fill={color} stroke="var(--color-bg)" strokeWidth="0.6" />
        )}
      </svg>
      {active && (
        <div
          className="line-chart__tooltip"
          style={{ left: `${active.x}%`, top: `${active.y}%` }}
        >
          <span className="line-chart__tooltip-label">{active.label}</span>
          <span className="line-chart__tooltip-value">{formatValue(active.value)}</span>
        </div>
      )}
    </div>
  );
};

export default LineChart;
