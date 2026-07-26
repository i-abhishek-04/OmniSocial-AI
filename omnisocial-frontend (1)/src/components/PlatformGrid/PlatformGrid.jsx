import { platforms } from '../../data/platforms';
import './PlatformGrid.css';

const PlatformGrid = () => {
  return (
    <section className="platform-section" id="platforms">
      <div className="container">
        <h2 className="platform-section__title">
          All Major Platforms. One Dashboard.
        </h2>

        <div className="platform-row">
          {platforms.map((platform) => {
            const Icon = platform.icon;
            return (
              <div className="platform-pill" key={platform.id}>
                <span
                  className="platform-pill__icon"
                  style={{ color: platform.color }}
                >
                  <Icon size={18} />
                </span>
                <span className="platform-pill__name">{platform.name}</span>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default PlatformGrid;
