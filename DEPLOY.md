# Buddio — Live Deployment Guide

Stack (all free tiers, no credit card required):

| Piece | Provider | What runs |
|-------|----------|-----------|
| Frontend | [Vercel](https://vercel.com) | Next.js app in `apps/web` |
| API | [Render](https://render.com) | FastAPI backend in `services/api` |
| Database | [Neon](https://neon.tech) | Postgres 16 (free, always-on) |
| AI | Google Gemini | Live via `GEMINI_API_KEY` |

> Note: Render's free web service sleeps after ~15 min idle and takes ~30s to
> wake on the first request. Visit the API once before the demo so it is warm.

---

## 1. Create the database (Neon)

1. Sign up / log in at https://neon.tech (free plan).
2. **Create a project** (region close to you), name it `buddio`.
3. In the dashboard copy the **connection string** from the **Connection
   details** panel. It looks like:
   `postgresql://neondb_owner:xxxx@ep-xxx.region.aws.neon.tech/buddio`
4. Rewrite it for the app by changing the scheme to `postgresql+psycopg://`
   and adding `sslmode=require&connect_timeout=3`. Keep it for step 2:
   ```
   postgresql+psycopg://neondb_owner:xxxx@ep-xxx.region.aws.neon.tech/buddio?sslmode=require&connect_timeout=3
   ```

## 2. Deploy the API (Render)

1. Sign up / log in at https://render.com (free).
2. **Dashboard → New → Web Service** → pick the GitHub repo `Reinerbroww/Buddio`.
3. Fill the form:
   - **Name:** `buddio-api`
   - **Root Directory:** `services/api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
4. **Advanced → Environment Variables:**
   | Key | Value |
   |-----|-------|
   | `APP_ENV` | `production` |
   | `SECRET_KEY` | random 64-char string (`openssl rand -hex 32`) |
   | `DATABASE_URL` | the rewritten Neon string from step 1 |
   | `GEMINI_API_KEY` | your (new) Gemini API key |
   | `CORS_ORIGINS` | `https://<your-app>.vercel.app` (fill after step 3) |
   | `GEMINI_MODEL` | `gemini-flash-latest` |
5. **Create Web Service** and wait for the first deploy to go **Live**.
6. Sanity check: open `https://buddio-api.onrender.com/api/health` →
   expect `{"status":"healthy","database":"connected",...}`.

> Tables are created automatically on first start (lifespan hook), so no
> migration step is needed.

## 3. Deploy the frontend (Vercel)

1. Sign up / log in at https://vercel.com (free).
2. **Add New → Project** → import `Reinerbroww/Buddio`.
3. Project settings:
   - **Framework Preset:** `Next.js` (auto-detected)
   - **Root Directory:** `apps/web`
4. **Environment Variables** (add as `Production`):
   | Key | Value |
   |-----|-------|
   | `NEXT_PUBLIC_API_URL` | `https://buddio-api.onrender.com/api` |
5. **Deploy.** You get a URL like `https://buddio-xyz.vercel.app`.

## 4. Link the two

1. Back in Render, edit the `buddio-api` service env vars and set
   `CORS_ORIGINS` to your Vercel URL: `https://buddio-xyz.vercel.app`
   (add a comma + `http://localhost:3000` if you still test locally).
2. Render auto-redeploys on env change.

## 5. Verify the live app

1. Open the Vercel URL. Landing page loads.
2. **Register** a demo account → you land on onboarding.
3. Generate a **roadmap** and ask the **mentor** a question — both should
   return `mode: "gemini"` responses.
4. (Optional) Wake the API by hitting `https://buddio-api.onrender.com/api/health`
   a minute before the mentor opens the app.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| API 503 / first load slow | Free Render is cold-starting; wait ~30s and refresh. |
| Frontend calls localhost | `NEXT_PUBLIC_API_URL` missing or wrong in Vercel; redeploy. |
| CORS errors in browser | `CORS_ORIGINS` on Render must be the exact Vercel origin (no trailing `/`). |
| `mode: "mock"` responses | `GEMINI_API_KEY` missing/invalid on Render, or `FORCE_MOCK_AI=true`. |
| DB connection error on startup | `DATABASE_URL` scheme must be `postgresql+psycopg://` and include `sslmode=require`. |

## Environment variables reference

| Variable | Where | Purpose |
|----------|-------|---------|
| `NEXT_PUBLIC_API_URL` | Vercel | Base URL of the API for the browser |
| `DATABASE_URL` | Render | Postgres connection string (psycopg scheme) |
| `GEMINI_API_KEY` | Render | Gemini model access |
| `GEMINI_MODEL` | Render (optional) | Model name, default `gemini-flash-latest` |
| `CORS_ORIGINS` | Render | Comma-separated allowed browser origins |
| `SECRET_KEY` | Render | JWT signing secret, random in production |
| `APP_ENV` | Render | `production` |
