# OmniSocial AI — Frontend (React + Vite)

## Setup
```bash
npm install
```

`.env` already points at the local backend:
```
VITE_API_BASE_URL=http://localhost:8000
```

## Run
```bash
npm run dev
```
Visit http://localhost:5173 — landing page, then Sign up / Log in to reach
the dashboard at `/dashboard`.

## Pages
- `/` — landing page (unchanged design, buttons now wired to auth)
- `/login`, `/register` — auth
- `/dashboard` — overview (stat cards, growth chart, platform grid)
- `/dashboard/platforms` — connect/disconnect any of the 7 platforms
- `/dashboard/platforms/:platform` — per-platform deep dive
- `/dashboard/revenue` — monthly revenue + breakdown
- `/dashboard/assistant` — AI chat grounded in your analytics
- `/dashboard/settings` — profile

Make sure the backend is running on port 8000 first (or update
`VITE_API_BASE_URL`).
