import { platforms } from './platforms';

// Maps a backend platform id (e.g. "youtube") to its icon + brand color,
// reusing the same source of truth already used on the landing page.
const iconMap = Object.fromEntries(platforms.map((p) => [p.id, p]));

export const getPlatformMeta = (platformId) => iconMap[platformId] || null;
