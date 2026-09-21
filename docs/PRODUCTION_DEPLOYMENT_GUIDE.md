# LearnSync AI — Production Deployment Guide

This guide provides step-by-step instructions for deploying LearnSync AI to cloud infrastructure (AWS / GCP / Vercel / Render / Docker).

---

## 1. Environment Configuration

### Backend (`backend/.env`)
Copy `backend/.env.example` to `backend/.env` on your production server:

```ini
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=8000

GEMINI_API_KEY=your_production_google_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
AI_PROVIDER_MODE=auto

CORS_ORIGINS=https://app.learnsync.ai,https://teacher.learnsync.ai
JWT_SECRET=your_secure_64_char_random_jwt_secret
MONGODB_URL=mongodb+srv://user:password@cluster.mongodb.net/learnsync?retryWrites=true&w=majority
MAX_UPLOAD_SIZE_MB=5
```

### Frontend (`teacher-dashboard/.env.production`)
Create `.env.production` in `teacher-dashboard`:

```ini
VITE_API_BASE_URL=https://api.learnsync.ai
VITE_WS_BASE_URL=wss://api.learnsync.ai
```

---

## 2. Backend Deployment (FastAPI + Gunicorn / Uvicorn)

### Docker Deployment
Build and run the production backend container:

```bash
cd backend
docker build -t learnsync-backend:latest .
docker run -d --name learnsync-backend -p 8000:8000 --env-file .env learnsync-backend:latest
```

### Systemd Service (Linux Server)
Run Gunicorn with Uvicorn workers:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 3. Frontend Deployment (React + Vite + Nginx / Vercel)

### Static Build
```bash
cd teacher-dashboard
npm run build
```

### Nginx Reverse Proxy Configuration (`/etc/nginx/sites-available/learnsync`)
```nginx
server {
    listen 80;
    server_name app.learnsync.ai;

    location / {
        root /var/www/learnsync/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/collaboration/ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## 4. Verification & Health Monitoring

Verify endpoints post-deployment:
- `GET https://api.learnsync.ai/health` $\rightarrow$ `{"status": "healthy", ...}`
- `GET https://api.learnsync.ai/api/ai/status` $\rightarrow$ `{"gemini_configured": true, ...}`
