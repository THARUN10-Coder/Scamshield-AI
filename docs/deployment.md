# ScamShield AI — Deployment Guide

## 1. Cloud & Container Deployment Options

### Option A: Render.com / Railway / Fly.io (Zero-DevOps Deployment)

#### Backend (Web Service):
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py` or `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: `backend`
- **Environment Variables**:
  - `PROJECT_NAME=ScamShield AI`
  - `DATABASE_URL=sqlite:///./scamshield.db` (or attach a managed PostgreSQL database)
  - `SECRET_KEY=<your-secret-production-key>`

#### Frontend (Static Site):
- **Build Command**: `npm run build`
- **Publish Directory**: `dist`
- **Root Directory**: `frontend`
- **Environment Variables / Config**:
  - Update `VITE_API_URL` or `API_BASE_URL` in `src/services/api.ts` to your deployed backend URL.

---

### Option B: Docker & Docker Compose (Self-Hosted VPS / AWS EC2 / DigitalOcean)

```bash
# Build and run containers in detached mode
docker compose up -d --build
```
- **Backend**: Runs on port 8000
- **Frontend**: Runs on port 80 (Nginx serving production bundle)

---

### Option C: Vercel (Frontend) + Render/Railway (Backend)
1. Push this repository to GitHub:
   ```bash
   git remote add origin https://github.com/THARUN10-Coder/<repo-name>.git
   git push -u origin main
   ```
2. In Vercel, import the repository and set the root directory to `frontend`.
3. Set build command to `npm run build` and output directory to `dist`.
