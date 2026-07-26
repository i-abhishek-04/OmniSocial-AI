import { features } from '../../data/features';
import './Features.css';

const Features = () => {
  return (
    <section className="features-section" id="features">
      <div className="container">
        <div className="features-section__header">
          <span className="eyebrow">Powerful Features</span>
          <h2 className="features-section__title">
            Everything You Need to Grow Faster
          </h2>
        </div>

        <div className="features-grid">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <div className="feature-card" key={feature.id}>
                <div
                  className="feature-card__icon"
                  style={{
                    background: feature.color,
                    boxShadow: `0 8px 20px -6px ${feature.color}80`,
                  }}
                >
                  <Icon size={20} strokeWidth={2} color="#ffffff" />
                </div>
                <h3 className="feature-card__title">{feature.title}</h3>
                <p className="feature-card__description">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Features;
