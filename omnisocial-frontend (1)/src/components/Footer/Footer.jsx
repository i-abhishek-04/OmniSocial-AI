import { Layers } from 'lucide-react';
import { FaXTwitter, FaInstagram, FaLinkedin, FaYoutube } from 'react-icons/fa6';
import './Footer.css';

const FOOTER_COLUMNS = [
  {
    title: 'Company',
    links: ['About', 'Careers', 'Blog', 'Press'],
  },
  {
    title: 'Product',
    links: ['Features', 'Pricing', 'Integrations', 'Changelog'],
  },
  {
    title: 'Resources',
    links: ['Documentation', 'API Reference', 'Community', 'Guides'],
  },
  {
    title: 'Support',
    links: ['Help Center', 'Contact Us', 'Status', 'Report an Issue'],
  },
];

const SOCIAL_LINKS = [
  { id: 'x', icon: FaXTwitter, label: 'X' },
  { id: 'instagram', icon: FaInstagram, label: 'Instagram' },
  { id: 'linkedin', icon: FaLinkedin, label: 'LinkedIn' },
  { id: 'youtube', icon: FaYoutube, label: 'YouTube' },
];

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer__top">
          <div className="footer__brand">
            <a href="#top" className="footer__logo">
              <span className="footer__logo-icon">
                <Layers size={18} strokeWidth={2.5} />
              </span>
              OmniSocial <span className="footer__logo-accent">AI</span>
            </a>
            <p className="footer__tagline">
              One dashboard for every platform you create on.
            </p>
            <div className="footer__socials">
              {SOCIAL_LINKS.map((social) => {
                const Icon = social.icon;
                return (
                  <a
                    key={social.id}
                    href={`#${social.id}`}
                    className="footer__social-link"
                    aria-label={social.label}
                  >
                    <Icon size={16} />
                  </a>
                );
              })}
            </div>
          </div>

          <div className="footer__columns">
            {FOOTER_COLUMNS.map((column) => (
              <div className="footer__column" key={column.title}>
                <h4 className="footer__column-title">{column.title}</h4>
                <ul className="footer__column-list">
                  {column.links.map((link) => (
                    <li key={link}>
                      <a href="#top" className="footer__column-link">
                        {link}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        <div className="footer__bottom">
          <span className="footer__copyright">
            © {year} OmniSocial AI. All rights reserved.
          </span>
          <div className="footer__legal">
            <a href="#top" className="footer__legal-link">
              Privacy Policy
            </a>
            <a href="#top" className="footer__legal-link">
              Terms
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
