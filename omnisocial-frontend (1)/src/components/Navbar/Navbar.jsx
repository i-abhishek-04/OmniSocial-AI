import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, Layers, ChevronDown } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import './Navbar.css';

const NAV_LINKS = [
  { label: 'Features', href: '#features' },
  { label: 'Platforms', href: '#platforms' },
  { label: 'Pricing', href: '#pricing' },
  { label: 'Resources', href: '#resources', hasDropdown: true },
  { label: 'About Us', href: '#about' },
];

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 8);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={`navbar ${scrolled ? 'navbar--scrolled' : ''}`}>
      <div className="navbar__inner container">
        <Link to="/" className="navbar__logo">
          <span className="navbar__logo-icon">
            <Layers size={18} strokeWidth={2.5} />
          </span>
          OmniSocial <span className="navbar__logo-accent">AI</span>
        </Link>

        <nav className="navbar__links" aria-label="Primary">
          {NAV_LINKS.map((link) => (
            <a key={link.href} href={link.href} className="navbar__link">
              {link.label}
              {link.hasDropdown && <ChevronDown size={14} strokeWidth={2.2} />}
            </a>
          ))}
        </nav>

        <div className="navbar__actions">
          {isAuthenticated ? (
            <Link to="/dashboard" className="btn btn-primary">
              Go to Dashboard
            </Link>
          ) : (
            <>
              <Link to="/login" className="btn btn-secondary navbar__login">
                Log in
              </Link>
              <Link to="/register" className="btn btn-primary">
                Get Started Free
              </Link>
            </>
          )}
        </div>

        <button
          type="button"
          className="navbar__toggle"
          onClick={() => setMenuOpen((prev) => !prev)}
          aria-label={menuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={menuOpen}
        >
          {menuOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {menuOpen && (
        <div className="navbar__mobile">
          {NAV_LINKS.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="navbar__mobile-link"
              onClick={() => setMenuOpen(false)}
            >
              {link.label}
            </a>
          ))}
          <div className="navbar__mobile-actions">
            {isAuthenticated ? (
              <Link to="/dashboard" className="btn btn-primary" onClick={() => setMenuOpen(false)}>
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link to="/login" className="btn btn-secondary" onClick={() => setMenuOpen(false)}>
                  Log in
                </Link>
                <Link to="/register" className="btn btn-primary" onClick={() => setMenuOpen(false)}>
                  Get Started Free
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

export default Navbar;
