# Chatbot-Driven IT Change Management Application

A conversational interface for creating and managing ServiceNow change requests, integrated with Jira and GitHub. This application replaces traditional webhook-driven workflows with an interactive user-driven approach.

## Features

- **Conversational UI** for creating/updating ServiceNow change requests
- **Intent Detection** (rule-based initially, AI-powered in later phases)
- **Multi-Platform Integration** with ServiceNow, Jira, and GitHub APIs
- **Progressive Complexity** approach: Start simple, expand to AI/NLU, then real-time features

## Technology Stack

### Backend
- **Django 5.x** + Django REST Framework
- **Python 3.11+** with `uv` package manager
- **PostgreSQL** (production) / SQLite (development)

### Frontend
- **React 18+** with TypeScript
- **Vite** for fast development
- **Tailwind CSS** + shadcn/ui components
- **Zustand** for state management

### Integrations
- ServiceNow REST API
- Jira Python library
- PyGithub

## Project Structure

This is a **monorepo** containing both frontend and backend:

```
chatbot-app/
├── backend/          # Django API
├── frontend/         # React UI
├── CLAUDE.md         # Developer instructions
└── MONOREPO_STRUCTURE.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- uv (Python package manager)

### Initial Setup

```bash
# Clone repository
git clone <your-repo-url>
cd charm

# Backend setup
cd backend
curl -LsSf https://astral.sh/uv/install.sh | sh  # Install uv if needed
uv sync
cp .env.example .env
# Edit .env with your credentials
uv run python manage.py migrate
uv run python manage.py createsuperuser

# Frontend setup
cd ../frontend
npm install
cp .env.example .env.local
```

### Development

Run both services in separate terminals:

```bash
# Terminal 1 - Backend
cd backend
uv run python manage.py runserver
# Runs on http://localhost:8000

# Terminal 2 - Frontend
cd frontend
npm run dev
# Runs on http://localhost:5173
```

### Access Points

- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:8000/api/
- **Django Admin:** http://localhost:8000/admin/

## Implementation Phases

### Phase 1: Simple Rule-Based Chatbot *(Current Target)*
- Basic React chat UI
- REST API for message exchange
- Rule-based intent detection (keyword matching)
- Form-filling conversation flow
- ServiceNow integration for creating change requests

### Phase 2: AI/NLU Integration
- Natural language intent detection using OpenAI/LangChain
- Context-aware conversations
- Entity extraction from user messages
- Multi-turn dialogue support

### Phase 3: Real-Time Features
- WebSocket connections via Django Channels
- Real-time message delivery
- Typing indicators
- Live status updates

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Comprehensive developer guide and architecture documentation
- **[MONOREPO_STRUCTURE.md](MONOREPO_STRUCTURE.md)** - Detailed monorepo setup and deployment guide

## Testing

```bash
# Backend tests
cd backend
uv run python manage.py test

# Frontend tests
cd frontend
npm test
```

## Deployment

See [MONOREPO_STRUCTURE.md](MONOREPO_STRUCTURE.md) for deployment options:
- Single server with Nginx
- Docker Compose
- Separate hosting (Vercel + Railway)

## License

*Add your license here*

## Contributing

*Add contribution guidelines here*
