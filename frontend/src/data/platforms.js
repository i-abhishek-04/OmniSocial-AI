import {
  FaYoutube,
  FaGithub,
  FaReddit,
  FaInstagram,
  FaFacebook,
  FaLinkedin,
  FaXTwitter,
  FaTiktok,
} from 'react-icons/fa6';
import { SiDevdotto } from 'react-icons/si';

// Order and platform set mirror the backend's single source of truth,
// app/services/platforms/registry.py: live platforms first, then the
// coming-soon placeholders. `live: false` platforms render as disabled
// cards in the dashboard (see pages/dashboard/Platforms.jsx) - they are
// intentionally kept in this list rather than removed, per the product
// spec, so they always appear in the UI.
export const platforms = [
  {
    id: 'youtube',
    name: 'YouTube',
    icon: FaYoutube,
    color: '#FF0000',
    stat: '2.1B users',
    live: true,
  },
  {
    id: 'github',
    name: 'GitHub',
    icon: FaGithub,
    color: '#ffffff',
    stat: '100M+ developers',
    live: true,
  },
  {
    id: 'reddit',
    name: 'Reddit',
    icon: FaReddit,
    color: '#FF4500',
    stat: '500M+ users',
    live: false,
  },
  {
    id: 'devto',
    name: 'Dev.to',
    icon: SiDevdotto,
    color: '#0A0A0A',
    stat: '1M+ developers',
    live: false,
  },
  {
    id: 'instagram',
    name: 'Instagram',
    icon: FaInstagram,
    color: '#E1306C',
    stat: '2B users',
    live: true,
  },
  {
    id: 'linkedin',
    name: 'LinkedIn',
    icon: FaLinkedin,
    color: '#0A66C2',
    stat: '1B users',
    live: false,
  },
  {
    id: 'tiktok',
    name: 'TikTok',
    icon: FaTiktok,
    color: '#25F4EE',
    stat: '1.5B users',
    live: false,
  },
  {
    id: 'facebook',
    name: 'Facebook',
    icon: FaFacebook,
    color: '#1877F2',
    stat: '3B users',
    live: false,
  },
  {
    id: 'x',
    name: 'X (Twitter)',
    icon: FaXTwitter,
    color: '#e2e8f0',
    stat: '550M users',
    live: false,
  },
];
