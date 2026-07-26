# OmniSocial AI — Backend (FastAPI)

## Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`.env` is already filled in with a generated JWT secret and a SQLite
database (zero setup required). To use your own Postgres instead, edit
`DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/omnisocial
```

## Run
```bash
uvicorn app.main:app --reload --port 8000
```
API docs (Swagger): http://localhost:8000/docs

## What's real vs. demo data
- Auth, database, JWT, password hashing: **real**.
- Analytics/revenue numbers for the 7 platforms: **deterministic demo data**,
  seeded per user so it stays stable across refreshes. See the docstring at
  the top of `app/services/analytics_service.py` for exactly how to swap in
  real platform APIs (Instagram Graph API, YouTube Data API v3, etc.) later
  — each platform needs its own developer app + OAuth from you, which I
  can't create on your behalf.
- AI chat: works out of the box with a data-grounded rule-based responder.
  
