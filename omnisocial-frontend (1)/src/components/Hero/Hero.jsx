import {
  Play,
  ArrowUpRight,
  Users,
  Send,
  Timer,
  ShieldCheck,
  LayoutGrid,
  BarChart3,
  Inbox,
  CalendarDays,
  FileText,
  Bot,
  Wallet,
  Settings,
  ChevronDown,
} from 'lucide-react';
import { FaYoutube } from 'react-icons/fa6';
import { Link } from 'react-router-dom';
import './Hero.css';

const STATS = [
  { id: 'creators', icon: Users, value: '10K+', label: 'Creators' },
  { id: 'posts', icon: Send, value: '25M+', label: 'Posts Managed' },
  { id: 'uptime', icon: Timer, value: '99.9%', label: 'Uptime' },
  { id: 'support', icon: ShieldCheck, value: '24/7', label: 'AI Support' },
];

const SIDEBAR_NAV = [
  { id: 'overview', icon: LayoutGrid, label: 'Overview', active: true },
  { id: 'analytics', icon: BarChart3, label: 'Analytics' },
  { id: 'inbox', icon: Inbox, label: 'Inbox', badge: 12 },
  { id: 'scheduler', icon: CalendarDays, label: 'Scheduler' },
  { id: 'posts', icon: FileText, label: 'Posts' },
  { id: 'assistant', icon: Bot, label: 'AI Assistant' },
  { id: 'revenue', icon: Wallet, label: 'Revenue' },
  { id: 'settings', icon: Settings, label: 'Settings' },
];

const METRIC_CARDS = [
  {
    id: 'followers',
    label: 'Total Followers',
    value: '3.42M',
    delta: '+14.5%',
    points: '0,20 10,17 20,19 30,14 40,15 50,9 60,11 70,4',
  },
  {
    id: 'views',
    label: 'Total Views',
    value: '48.7M',
    delta: '+21.3%',
    points: '0,18 10,19 20,13 30,15 40,8 50,10 60,5 70,3',
  },
  {
    id: 'engagement',
    label: 'Engagement Rate',
    value: '5.67%',
    delta: '+8.9%',
    points: '0,15 10,16 20,12 30,13 40,10 50,11 60,7 70,6',
  },
  {
    id: 'revenue',
    label: 'Total Revenue',
    value: '$12,4K',
    delta: '+16.7%',
    points: '0,19 10,14 20,16 30,10 40,12 50,6 60,8 70,2',
  },
];

const CHART_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

const Hero = () => {
  return (
    <section className="hero" id="top">
      <div className="hero__glow" aria-hidden="true" />
      <div className="container hero__inner">
        <div className="hero__content">
          <span className="eyebrow hero__eyebrow-pill">
            AI Powered &middot; All-in-One &middot; For Creators &amp; Businesses
          </span>

          <h1 className="hero__title">
            Manage Every Social
            <br />
            Platform From One
            <br />
            <span className="text-gradient">Intelligent Dashboard</span>
          </h1>

          <p className="hero__subtitle">
            AI-powered analytics, cross-posting, smart scheduling, and revenue
            tracking &mdash; everything you need to grow faster and save hours
            every day.
          </p>

          <div className="hero__actions">
            <Link to="/register" className="btn btn-primary">
              Get Started Free
              <ArrowUpRight size={17} strokeWidth={2.5} />
            </Link>
            <button type="button" className="btn btn-secondary hero__demo-btn">
              Watch Demo
              <span className="hero__play-icon">
                <Play size={11} fill="currentColor" />
              </span>
            </button>
          </div>

          <dl className="hero__stats">
            {STATS.map((stat) => {
              const Icon = stat.icon;
              return (
                <div className="hero__stat" key={stat.id}>
                  <span className="hero__stat-icon">
                    <Icon size={16} strokeWidth={2.2} />
                  </span>
                  <div>
                    <dt className="hero__stat-value">{stat.value}</dt>
                    <dd className="hero__stat-label">{stat.label}</dd>
                  </div>
                </div>
              );
            })}
          </dl>
        </div>

        <div className="hero__preview">
          <div className="app-card">
            <div className="app-card__sidebar">
              <div className="app-card__brand">
                <span className="app-card__brand-icon">
                  <LayoutGrid size={14} strokeWidth={2.5} />
                </span>
                OmniSocial AI
              </div>
              <nav className="app-card__nav">
                {SIDEBAR_NAV.map((item) => {
                  const Icon = item.icon;
                  return (
                    <span
                      key={item.id}
                      className={`app-card__nav-item ${
                        item.active ? 'app-card__nav-item--active' : ''
                      }`}
                    >
                      <Icon size={14} strokeWidth={2.2} />
                      {item.label}
                      {item.badge && (
                        <span className="app-card__nav-badge">{item.badge}</span>
                      )}
                    </span>
                  );
                })}
              </nav>
            </div>

            <div className="app-card__main">
              <div className="app-card__topbar">
                <div>
                  <h2 className="app-card__welcome">Welcome back, Alex 👋</h2>
                  <p className="app-card__welcome-sub">
                    Here&apos;s what&apos;s happening with your channels today.
                  </p>
                </div>
                <div className="app-card__topbar-right">
                  <span className="app-card__date-pill">
                    May 12 &ndash; May 18, 2024
                    <ChevronDown size={13} />
                  </span>
                  <span className="app-card__avatar" aria-hidden="true" />
                </div>
              </div>

              <div className="app-card__metrics">
                {METRIC_CARDS.map((metric) => (
                  <div className="metric-card" key={metric.id}>
                    <span className="metric-card__label">{metric.label}</span>
                    <span className="metric-card__value">{metric.value}</span>
                    <div className="metric-card__foot">
                      <span className="metric-card__delta">{metric.delta}</span>
                      <svg
                        viewBox="0 0 70 24"
                        preserveAspectRatio="none"
                        className="metric-card__sparkline"
                        aria-hidden="true"
                      >
                        <polyline points={metric.points} fill="none" strokeWidth="2" />
                      </svg>
                    </div>
                  </div>
                ))}
              </div>

              <div className="app-card__panels">
                <div className="performance-card">
                  <div className="performance-card__header">
                    <span className="performance-card__title">
                      Performance Overview
                    </span>
                    <span className="performance-card__range">
                      Weekly
                      <ChevronDown size={12} />
                    </span>
                  </div>

                  <div className="performance-card__legend">
                    <span className="legend-dot legend-dot--followers">Followers</span>
                    <span className="legend-dot legend-dot--views">Views</span>
                    <span className="legend-dot legend-dot--engagement">Engagement</span>
                  </div>

                  <svg
                    viewBox="0 0 460 160"
                    preserveAspectRatio="none"
                    className="performance-card__chart"
                    aria-hidden="true"
                  >
                    <defs>
                      <linearGradient id="fillFollowers" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#818cf8" stopOpacity="0.32" />
                        <stop offset="100%" stopColor="#818cf8" stopOpacity="0" />
                      </linearGradient>
                    </defs>
                    <path
                      d="M0,110 L65,95 L130,105 L195,70 L260,88 L325,45 L390,60 L460,30 L460,160 L0,160 Z"
                      fill="url(#fillFollowers)"
                    />
                    <path
                      className="performance-card__line performance-card__line--followers"
                      d="M0,110 L65,95 L130,105 L195,70 L260,88 L325,45 L390,60 L460,30"
                      fill="none"
                    />
                    <path
                      className="performance-card__line performance-card__line--views"
                      d="M0,130 L65,120 L130,100 L195,108 L260,80 L325,90 L390,55 L460,62"
                      fill="none"
                    />
                    <path
                      className="performance-card__line performance-card__line--engagement"
                      d="M0,148 L65,140 L130,142 L195,130 L260,134 L325,120 L390,124 L460,110"
                      fill="none"
                    />
                  </svg>

                  <div className="performance-card__axis">
                    {CHART_DAYS.map((day) => (
                      <span key={day}>{day}</span>
                    ))}
                  </div>
                </div>

                <div className="side-panels">
                  <div className="platform-highlight">
                    <span className="platform-highlight__label">
                      Top Performing Platform
                    </span>
                    <div className="platform-highlight__body">
                      <span className="platform-highlight__icon">
                        <FaYoutube size={18} />
                      </span>
                      <div>
                        <span className="platform-highlight__name">YouTube</span>
                        <span className="platform-highlight__sub">1.2M Followers</span>
                      </div>
                      <span className="platform-highlight__delta">+18.2%</span>
                    </div>
                  </div>

                  <div className="ai-recommend">
                    <span className="ai-recommend__label">AI Recommendation</span>
                    <p className="ai-recommend__text">
                      Best time to post tomorrow on Instagram is{' '}
                      <strong>7:30 PM</strong>
                    </p>
                    <button type="button" className="ai-recommend__button">
                      Schedule Now
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
