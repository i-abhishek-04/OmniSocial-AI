import './StatCard.css';

const StatCard = ({ icon: Icon, label, value, delta, deltaPositive = true }) => {
  return (
    <div className="stat-card">
      <div className="stat-card__top">
        <span className="stat-card__icon">
          <Icon size={17} strokeWidth={2.2} />
        </span>
        {delta !== undefined && (
          <span className={`stat-card__delta ${deltaPositive ? 'stat-card__delta--up' : 'stat-card__delta--down'}`}>
            {deltaPositive ? '+' : ''}{delta}%
          </span>
        )}
      </div>
      <span className="stat-card__value">{value}</span>
      <span className="stat-card__label">{label}</span>
    </div>
  );
};

export default StatCard;
