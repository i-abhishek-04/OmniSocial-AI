import { ArrowUpRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import './CTA.css';

const CTA = () => {
  return (
    <section className="cta-section" id="pricing">
      <div className="container">
        <div className="cta-card">
          <div className="cta-card__glow" aria-hidden="true" />
          <span className="eyebrow">Get started in minutes</span>
          <h2 className="cta-card__title">
            Ready to Manage All Your Social Media?
          </h2>
          <p className="cta-card__subtitle">
            Join thousands of creators and teams who stopped switching tabs and
            started growing faster with one AI-powered dashboard for every
            platform they use.
          </p>
          <Link to="/register" className="btn btn-primary cta-card__button">
            Get Started Free
            <ArrowUpRight size={17} strokeWidth={2.5} />
          </Link>
          <span className="cta-card__note">No credit card required · Cancel anytime</span>
        </div>
      </div>
    </section>
  );
};

export default CTA;
