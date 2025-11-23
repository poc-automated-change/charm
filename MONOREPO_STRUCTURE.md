# Monorepo Structure for Chatbot Application

## Directory Structure

```
chatbot-app/                           # Root repository
├── README.md                          # Project overview
├── CLAUDE.md                          # Claude Code instructions
├── .gitignore                         # Git ignore (Python + Node)
├── docker-compose.yml                 # Optional: Docker setup
│
├── backend/                           # Django API
│   ├── manage.py
│   ├── pyproject.toml                # Python dependencies (uv)
│   ├── requirements.txt              # Pip format
│   ├── .env.example
│   ├── .env                          # Not in git
│   │
│   ├── config/                       # Django project
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── chatbot/                      # Chat app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── intents.py
│   │   ├── handlers.py
│   │   └── ...
│   │
│   ├── integrations/                 # External services app
│   │   ├── models.py
│   │   ├── services.py
│   │   └── ...
│   │
│   └── db.sqlite3                    # Dev database
│
├── frontend/                          # React UI
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── .env.example
│   ├── .env.local                    # Not in git
│   │
│   ├── public/
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types/
│   │
│   └── dist/                         # Build output (not in git)
│
└── docs/                             # Shared documentation (optional)
    ├── architecture.md
    ├── api-specs.md
    └── deployment.md
```

## Setup Instructions

### Initial Setup

```bash
# Clone repository
git clone <your-repo-url>
cd chatbot-app

# Backend setup
cd backend
# Install uv if not already
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
cp .env.example .env
# Edit .env with your credentials
uv run python manage.py migrate
uv run python manage.py createsuperuser

# Frontend setup
cd ../frontend
npm install
cp .env.example .env.local
# Edit .env.local if needed

# You're ready to develop!
```

### Development Workflow

```bash
# Terminal 1 - Backend
cd backend
uv run python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev

# Access application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# Django Admin: http://localhost:8000/admin
```

### Adding Dependencies

```bash
# Backend (Python)
cd backend
uv add package-name

# Frontend (Node)
cd frontend
npm install package-name
```

## Git Configuration

### .gitignore (Root)

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
backend/.env
backend/db.sqlite3
backend/staticfiles/
*.log

# Node
node_modules/
frontend/dist/
frontend/.env.local
frontend/.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
```

## Environment Variables

### backend/.env.example

```env
# Django
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=sqlite3
# For PostgreSQL:
# DB_ENGINE=postgresql
# DB_NAME=chatbot_db
# DB_USER=postgres
# DB_PASSWORD=password
# DB_HOST=localhost
# DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173

# ServiceNow
SERVICENOW_INSTANCE=your-instance
SERVICENOW_USERNAME=your-username
SERVICENOW_PASSWORD=your-password

# Jira
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token

# GitHub
GITHUB_TOKEN=your-github-token

# Phase 2: AI
# OPENAI_API_KEY=sk-...

# Phase 3: WebSockets
# REDIS_URL=redis://localhost:6379/0
```

### frontend/.env.example

```env
VITE_API_URL=http://localhost:8000
# Phase 3:
# VITE_WS_URL=ws://localhost:8000
```

## Deployment Options

### Option 1: Single Server (Simplest)

Deploy both on one server, use Nginx to route:

```nginx
# /etc/nginx/sites-available/chatbot-app
server {
    listen 80;
    server_name your-domain.com;

    # Serve React frontend
    location / {
        root /var/www/chatbot-app/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to Django
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Django admin
    location /admin {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }

    # Static files (Django)
    location /static {
        alias /var/www/chatbot-app/backend/staticfiles;
    }
}
```

**Deployment steps:**
```bash
# On server
git clone <repo>
cd chatbot-app

# Build frontend
cd frontend
npm install
npm run build

# Setup backend
cd ../backend
uv sync
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput

# Run with systemd
sudo systemctl start chatbot-backend
sudo systemctl restart nginx
```

### Option 2: Docker Compose (Recommended)

Single `docker-compose.yml` in root:

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      - db
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: chatbot_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**backend/Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml requirements.txt ./
RUN uv pip install --system -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**frontend/Dockerfile:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host"]
```

**Deploy with Docker:**
```bash
docker-compose up -d
```

### Option 3: Separate Hosting (If needed later)

- **Frontend**: Vercel, Netlify, or Cloudflare Pages (free tier)
- **Backend**: Railway, Render, or DigitalOcean (low cost)

This is easy to transition to from monorepo - just deploy each folder separately.

## CI/CD Example (GitHub Actions)

### .github/workflows/ci.yml

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        working-directory: ./backend
        run: |
          pip install uv
          uv pip install --system -r requirements.txt

      - name: Run tests
        working-directory: ./backend
        run: |
          python manage.py test

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Run tests
        working-directory: ./frontend
        run: npm test

      - name: Build
        working-directory: ./frontend
        run: npm run build
```

## Package Management

### Backend (Python with uv)

```bash
# All commands from backend/ directory
cd backend

# Add dependency
uv add django-cors-headers

# Add dev dependency
uv add --dev pytest-django

# Update all
uv sync --upgrade

# Generate requirements.txt for compatibility
uv pip freeze > requirements.txt
```

### Frontend (Node with npm)

```bash
# All commands from frontend/ directory
cd frontend

# Add dependency
npm install axios

# Add dev dependency
npm install -D @types/react

# Update all
npm update

# Audit security
npm audit fix
```

## Shared Code (Optional)

If you want to share types between frontend and backend:

### Option 1: Copy TypeScript types from Django models

```bash
# Create a script to generate types
backend/scripts/generate_types.py
```

```python
# backend/scripts/generate_types.py
# Generates TypeScript types from Django models
# Run: python manage.py shell < scripts/generate_types.py > ../frontend/src/types/api.generated.ts
```

### Option 2: Keep them separate (simpler)

Just manually keep TypeScript types in sync with Django serializers. For a small project, this is fine.

## Advantages of This Structure

1. **Single source of truth** - All code in one place
2. **Easy to navigate** - Clear separation of concerns
3. **Simple deployment** - Deploy from one repo
4. **Shared tooling** - One CI/CD, one issue tracker
5. **Better for code reviews** - See full feature (frontend + backend) in one PR
6. **Type safety** - Can generate TS types from Django models
7. **Can split later** - Easy to extract to separate repos if needed

## When to Split Into Multi-Repo

You might consider splitting if:
- Frontend and backend have different teams
- Different release schedules
- Reusing API for multiple frontends (mobile app, etc.)
- Repo becomes very large (>1GB)

For your internal tool, **start with monorepo** and split only if you hit these issues (you likely won't).
