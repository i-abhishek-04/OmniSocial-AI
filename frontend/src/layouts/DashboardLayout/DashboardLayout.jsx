import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import {
  LayoutGrid,
  Share2,
  Wallet,
  Bot,
  Settings,
  LogOut,
  Layers,
  Inbox as InboxIcon,
  CalendarClock,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import './DashboardLayout.css';

const NAV_ITEMS = [
  { to: '/dashboard', icon: LayoutGrid, label: 'Overview', end: true },
  { to: '/dashboard/platforms', icon: Share2, label: 'Platforms' },
  { to: '/dashboard/inbox', icon: InboxIcon, label: 'Inbox' },
  { to: '/dashboard/scheduler', icon: CalendarClock, label: 'Scheduler' },
  { to: '/dashboard/revenue', icon: Wallet, label: 'Revenue' },
  { to: '/dashboard/assistant', icon: Bot, label: 'AI Assistant' },
  { to: '/dashboard/settings', icon: Settings, label: 'Settings' },
];

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/', { replace: true });
  };

  const initials = (user?.full_name || 'U')
    .split(' ')
    .map((p) => p[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();

  return (
    <div className="dash">
      <aside className="dash__sidebar">
        <div className="dash__brand">
          <span className="dash__brand-icon">
            <Layers size={16} strokeWidth={2.5} />
          </span>
          OmniSocial <span className="text-gradient">AI</span>
        </div>

        <nav className="dash__nav">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => `dash__nav-item ${isActive ? 'dash__nav-item--active' : ''}`}
            >
              <item.icon size={17} strokeWidth={2.2} />
              {item.label}
            </NavLink>
          ))}
        </nav>

        <button type="button" className="dash__logout" onClick={handleLogout}>
          <LogOut size={16} strokeWidth={2.2} />
          Log out
        </button>
      </aside>

      <div className="dash__main">
        <header className="dash__topbar">
          <div>
            <p className="dash__topbar-greeting">Welcome back, {user?.full_name?.split(' ')[0] || 'there'} 👋</p>
            <p className="dash__topbar-sub">Here's what's happening across your platforms.</p>
          </div>
          <div className="dash__topbar-user">
            <span className="dash__avatar">{initials}</span>
          </div>
        </header>

        <main className="dash__content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
