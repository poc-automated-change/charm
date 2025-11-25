# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a chatbot-driven IT change management application that helps users create and manage ServiceNow change requests through a conversational interface. The application integrates with Jira, GitHub, and ServiceNow, replacing traditional webhook-driven workflows with an interactive user-driven approach.

**Key Features:**
- Conversational UI for creating/updating ServiceNow change requests
- Intent detection (rule-based initially, AI-powered later)
- Integration with ServiceNow, Jira, and GitHub APIs
- Progressive complexity: Start simple, expand to AI/NLU, then real-time features

## Repository Structure

**IMPORTANT**: This project uses a **MONOREPO** structure with both frontend and backend in a single repository.

**Why monorepo?**
- ✅ Simpler to manage for internal tools
- ✅ Atomic commits (update API and UI together)
- ✅ Easier development (no version sync issues)
- ✅ Single CI/CD pipeline
- ✅ Better for small teams

```
chatbot-app/                           # Root repository (this is your repo)
├── README.md
├── CLAUDE.md                          # This file
├── .gitignore
├── docker-compose.yml                 # Optional
│
├── backend/                           # Django API
│   ├── manage.py
│   ├── pyproject.toml
│   ├── config/                        # Django project
│   ├── chatbot/                       # Chat app
│   └── integrations/                  # External services app
│
└── frontend/                          # React UI
    ├── package.json
    ├── vite.config.ts
    └── src/
```

## Technology Stack

### Frontend (in `frontend/` directory)
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite (fast dev experience, hot module replacement)
- **UI Library**: Tailwind CSS + shadcn/ui (modern, customizable components)
- **State Management**: Zustand or React Context (start simple)
- **HTTP Client**: Axios or fetch API
- **Real-time (Phase 3)**: WebSocket API or Socket.io client

**Why React?**
- Largest ecosystem, most trending framework
- Easy transition from Angular (component-based architecture)
- Excellent WebSocket/real-time support for Phase 3
- Rich chatbot UI component libraries available

### Backend (in `backend/` directory)
- **Framework**: Django 5.x + Django REST Framework (DRF)
- **Language**: Python 3.11+
- **Database**: PostgreSQL (production) / SQLite (development)
- **Package Manager**: uv (fast Python package management)
- **Real-time (Phase 3)**: Django Channels + Redis
- **AI/NLU (Phase 2)**: LangChain + OpenAI API or Rasa

**Why Django over Flask?**
- Built-in admin interface for debugging conversations
- Django ORM excellent for conversation/message tracking
- Django REST Framework mature and feature-rich
- Django Channels for WebSocket support
- Better structure for growing complexity (simple → AI → real-time)
- Robust authentication and permissions system

### External Integrations
- **ServiceNow**: REST API (change request management)
- **Jira**: Jira Python library (issue tracking)
- **GitHub**: PyGithub (repository/PR management)

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   React Chat    │
│   Frontend      │
│  (Vite + TS)    │
└────────┬────────┘
         │ HTTP/REST (Phase 1-2)
         │ WebSocket (Phase 3)
         ▼
┌─────────────────────────────────────┐
│      Django Backend (DRF)           │
│  ┌───────────────────────────────┐  │
│  │   Chat API Endpoints          │  │
│  │   /api/chat/message/          │  │
│  │   /api/chat/conversations/    │  │
│  └──────────┬────────────────────┘  │
│             ▼                        │
│  ┌───────────────────────────────┐  │
│  │   Intent Detection Layer      │  │
│  │   - Phase 1: Rule-based       │  │
│  │   - Phase 2: AI/LLM           │  │
│  └──────────┬────────────────────┘  │
│             ▼                        │
│  ┌───────────────────────────────┐  │
│  │   Intent Handlers             │  │
│  │   - create_change_request     │  │
│  │   - check_status              │  │
│  │   - update_change             │  │
│  └──────────┬────────────────────┘  │
│             ▼                        │
│  ┌───────────────────────────────┐  │
│  │   Service Layer               │  │
│  │   - ServiceNowService         │  │
│  │   - JiraService               │  │
│  │   - GitHubService             │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   External Systems                  │
│   - ServiceNow                      │
│   - Jira                            │
│   - GitHub                          │
└─────────────────────────────────────┘
```

### Django Project Structure

```
chatbot-backend/
├── manage.py                          # Django CLI tool
├── pyproject.toml                     # Python dependencies (uv)
├── requirements.txt                   # Pip format (compatibility)
├── .env                               # Environment variables (not in git)
├── .env.example                       # Environment template
│
├── config/                            # Django project config
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Root URL routing
│   ├── wsgi.py                        # WSGI config
│   └── asgi.py                        # ASGI config (for Channels)
│
├── chatbot/                           # NEW - Chat logic app
│   ├── __init__.py
│   ├── models.py                      # Conversation, Message, ConversationContext
│   ├── views.py                       # DRF API views
│   ├── serializers.py                 # DRF serializers
│   ├── urls.py                        # Chat endpoints
│   ├── intents.py                     # Intent detection (rule-based → AI)
│   ├── handlers.py                    # Intent handlers
│   ├── context_manager.py             # Conversation state management
│   ├── admin.py                       # Django admin config
│   ├── apps.py                        # App configuration
│   ├── tests/                         # Unit tests
│   │   ├── test_intents.py
│   │   ├── test_handlers.py
│   │   └── test_views.py
│   └── migrations/                    # Database migrations
│
├── integrations/                      # External service integrations
│   ├── __init__.py
│   ├── models.py                      # ChangeRequest model
│   ├── services.py                    # ServiceNow, Jira, GitHub clients
│   ├── views.py                       # REST API endpoints
│   ├── serializers.py                 # DRF serializers
│   ├── urls.py                        # Integration endpoints
│   ├── admin.py                       # Admin config
│   ├── apps.py
│   ├── tests/
│   └── migrations/
│
└── db.sqlite3                         # SQLite database (dev only)
```

### React Frontend Structure

```
chatbot-frontend/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── .env.example
├── .env.local
│
├── public/
│   └── favicon.ico
│
├── src/
│   ├── main.tsx                       # App entry point
│   ├── App.tsx                        # Root component
│   ├── index.css                      # Global styles (Tailwind)
│   │
│   ├── components/                    # React components
│   │   ├── chat/
│   │   │   ├── ChatWindow.tsx         # Main chat container
│   │   │   ├── MessageList.tsx        # Scrollable message list
│   │   │   ├── MessageBubble.tsx      # Individual message component
│   │   │   ├── InputBox.tsx           # User input field
│   │   │   ├── TypingIndicator.tsx    # "Bot is typing..." indicator
│   │   │   └── FormRenderer.tsx       # Dynamic form rendering
│   │   │
│   │   ├── ui/                        # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   └── ... (other shadcn components)
│   │   │
│   │   └── layout/
│   │       ├── Header.tsx
│   │       └── Sidebar.tsx
│   │
│   ├── hooks/                         # Custom React hooks
│   │   ├── useChat.ts                 # Chat state management
│   │   ├── useConversation.ts         # Conversation persistence
│   │   └── useWebSocket.ts            # WebSocket hook (Phase 3)
│   │
│   ├── services/                      # API client services
│   │   ├── api.ts                     # Axios instance config
│   │   ├── chatApi.ts                 # Chat API endpoints
│   │   └── types.ts                   # API response types
│   │
│   ├── types/                         # TypeScript type definitions
│   │   ├── chat.types.ts              # Message, Conversation types
│   │   ├── intent.types.ts            # Intent, Context types
│   │   └── api.types.ts               # API response types
│   │
│   ├── store/                         # State management (Zustand)
│   │   └── chatStore.ts               # Global chat state
│   │
│   └── utils/                         # Utility functions
│       ├── formatters.ts              # Date/time formatting
│       └── validators.ts              # Input validation
```

## Database Models

### Chatbot App Models

**Conversation** - Tracks chat sessions
- Fields: id (UUID), user (FK), status, started_at, updated_at
- Tracks active, completed, or abandoned conversations
- Ordered by most recent first

**Message** - Individual chat messages
- Fields: conversation (FK), sender (user/bot), text, timestamp, metadata
- Stores all messages in chronological order
- Metadata field for rich content (forms, buttons, etc.)

**ConversationContext** - Tracks conversation state
- Fields: conversation (OneToOne), intent, collected_data, required_fields, next_field, change_request (FK)
- Manages the state machine for form filling
- Tracks which fields have been collected and what's still needed
- Has `is_complete()` method to check if all required fields are collected

### Integrations App Models

**ChangeRequest** - Links to ServiceNow changes
- ServiceNow fields: servicenow_sys_id, number, short_description, description, state, priority
- Integration links: jira_issue_key, github_repo, github_pr_number
- Timestamps: created_at, updated_at
- Indexed on servicenow_sys_id, number, and jira_issue_key for fast lookups

## API Design

### Chat API Endpoints

**POST /api/chat/message/**
- Send a message and get bot response
- Request: conversation_id (optional, null for new), message (string)
- Response: conversation_id, intent, bot_message, required_fields, collected_data, next_field, is_complete, change_request (optional)

**GET /api/chat/conversations/**
- List user's conversations
- Returns: array of conversations with id, status, started_at, last_message, message_count

**GET /api/chat/conversations/{id}/**
- Get conversation with all messages
- Returns: conversation details, full message history, current context

### Integration API Endpoints

**GET /api/change-requests/**
- List change requests

**GET /api/change-requests/{id}/**
- Get change request details

**GET /api/change-requests/by_servicenow_number/?number=CHG0030001**
- Find by ServiceNow number

## Implementation Phases

### Phase 1: Simple Rule-Based Chatbot (Start Here)

**Goal**: Get a working chatbot with basic intent detection and form filling

**Features**:
- Simple React chat UI
- REST API for message exchange
- Rule-based intent detection (keyword matching)
- Form-filling conversation flow
- Integration with ServiceNow to create change requests

**Intent Detection (Rule-Based)**:
- Implement in `chatbot/intents.py`
- Use keyword matching to detect intents
- Supported intents: create_change_request, check_status, update_change_request, help, unknown
- Match keywords like "create", "new", "change", "status", "update", etc.

**Intent Handler Pattern**:
- Each intent has a handler class (e.g., `CreateChangeRequestHandler`)
- Handler defines REQUIRED_FIELDS and FIELD_PROMPTS
- `handle()` method manages the conversation state machine
- Collects fields one by one, validates input, creates ServiceNow request when complete
- Returns bot_message, is_complete flag, and optional change_request data

**API View Pattern**:
- `ChatMessageView` handles POST requests to /api/chat/message/
- Gets or creates conversation and context
- Saves user message
- Detects intent if not already set
- Routes to appropriate handler
- Saves bot response
- Marks conversation as completed when done
- Returns structured response with conversation state

**Frontend Chat Component**:
- `ChatWindow` component manages message list and input
- Maintains local state for messages and conversation ID
- Handles message sending with loading state
- Scrolls to bottom when new messages arrive
- Shows typing indicator while waiting for response
- Displays welcome message when empty

**Phase 1 Deliverables**:
- ✅ Working chat interface
- ✅ REST API for chat messages
- ✅ Rule-based intent detection
- ✅ Create change request flow
- ✅ Check status flow
- ✅ ServiceNow integration
- ✅ Conversation persistence

---

### Phase 2: AI/NLU Integration

**Goal**: Replace rule-based intent detection with AI for natural language understanding

**New Features**:
- Natural language intent detection using OpenAI/LangChain
- Context-aware conversations
- Entity extraction from user messages
- Multi-turn dialogue support

**AI Intent Detection**:
- Use LangChain with OpenAI GPT-4
- Create `AIIntentDetector` class in `chatbot/intents.py`
- Define system prompt with available intents and entity types
- Use Pydantic output parser for structured results
- Return intent, confidence score, and extracted entities

**Smart Entity Extraction**:
- Create `SmartCreateChangeRequestHandler` class
- Extract entities from initial message (priority, dates, descriptions)
- Pre-fill collected_data with extracted entities
- Remove pre-filled fields from required_fields
- Continue with normal form-filling flow for missing fields

**Conversational Memory**:
- Use LangChain's ConversationBufferMemory
- Create `ConversationManager` class in `chatbot/context_manager.py`
- Load previous messages into memory on initialization
- Use ConversationChain for context-aware responses
- Maintains conversation history across turns

**Phase 2 Deliverables**:
- ✅ OpenAI/LangChain integration
- ✅ Natural language intent detection
- ✅ Entity extraction from messages
- ✅ Smart pre-filling of form fields
- ✅ Context-aware conversations
- ✅ Conversation memory

---

### Phase 3: Real-Time Features

**Goal**: Add WebSocket support for real-time chat experience

**New Features**:
- WebSocket connections
- Real-time message delivery
- Typing indicators
- Live status updates
- Multiple concurrent conversations

**Django Channels Setup**:
- Configure ASGI application in `config/asgi.py`
- Use ProtocolTypeRouter to handle both HTTP and WebSocket
- Add AuthMiddlewareStack for authentication
- Route WebSocket connections to chat consumer

**WebSocket Consumer**:
- Create `ChatConsumer` in `chatbot/consumers.py`
- Extend AsyncJsonWebsocketConsumer
- Handle connect, disconnect, receive_json events
- Send typing indicators (bot_typing)
- Process messages asynchronously
- Use database_sync_to_async for ORM calls

**WebSocket Routing**:
- Create `routing.py` in chatbot app
- Define websocket_urlpatterns
- Map `/ws/chat/` to ChatConsumer

**Frontend WebSocket Hook**:
- Create `useWebSocket` custom hook in `src/hooks/useWebSocket.ts`
- Manage WebSocket connection lifecycle
- Handle message sending and receiving
- Track connection status
- Support typing indicators
- Auto-reconnect on disconnect

**Phase 3 Deliverables**:
- ✅ Django Channels + Redis setup
- ✅ WebSocket consumer
- ✅ Real-time message delivery
- ✅ Typing indicators
- ✅ Frontend WebSocket integration
- ✅ Connection status handling

---

## Development Setup

### Initial Project Setup (Monorepo)

1. Create project directory
2. Initialize git
3. Create backend/ and frontend/ directories
4. Create .gitignore file

### Backend Setup

1. Install uv package manager
2. Initialize uv project
3. Add Django dependencies: django, djangorestframework, django-cors-headers, python-decouple, psycopg2-binary
4. Create Django project with `django-admin startproject config .`
5. Create apps: chatbot and integrations
6. For Phase 2: Add langchain and openai
7. For Phase 3: Add channels, channels-redis, and redis
8. Create .env file from .env.example
9. Run migrations
10. Create superuser
11. Test server on http://localhost:8000

### Frontend Setup

1. Create React app with Vite and TypeScript template
2. Install dependencies
3. Install Tailwind CSS and configure
4. Install shadcn/ui
5. Install additional packages: axios, zustand
6. Create .env.local file
7. Test dev server on http://localhost:5173

### Running Both in Development

Run two terminal windows:
- Terminal 1 (Backend): `cd backend && uv run python manage.py runserver`
- Terminal 2 (Frontend): `cd frontend && npm run dev`

**Access:**
- Frontend UI: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/

### Environment Variables

**Backend (.env)**: Configure Django settings, database, CORS, ServiceNow, Jira, GitHub, OpenAI API, and Redis

**Frontend (.env.local)**: Configure API URL and WebSocket URL

## Testing Strategy

### Backend Tests

**Intent Detection Tests** (`chatbot/tests/test_intents.py`):
- Test create_change_request intent detection
- Test check_status intent detection
- Test update_change_request intent detection
- Test help and unknown intents

**Handler Tests** (`chatbot/tests/test_handlers.py`):
- Test initial prompt generation
- Test field collection flow
- Test field validation
- Test change request creation
- Test completion detection

### Frontend Tests

**Chat Component Tests** (`src/components/chat/__tests__/ChatWindow.test.tsx`):
- Test welcome message rendering
- Test message sending
- Test bot response display
- Test loading states
- Test error handling

## Deployment Considerations

### Backend Deployment

**Production Settings**:
- Set DEBUG=False
- Configure ALLOWED_HOSTS
- Use PostgreSQL database
- Enable security settings: SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE

**Docker Setup**:
- Use Python 3.11-slim base image
- Install uv for dependency management
- Copy dependencies and install
- Copy application code
- Collect static files
- Run with gunicorn

### Frontend Deployment

**Build for Production**: Run `npm run build`

**Deployment Options**:
- Vercel/Netlify: Connect GitHub repo for auto-deploy
- Nginx: Serve static files and proxy API requests to backend

## Best Practices

### Code Organization
- Keep intent handlers in separate files as they grow
- Use Django signals for side effects (e.g., sending notifications)
- Use serializers for all API responses
- Keep business logic in services, not views

### Performance
- Use database indexes on frequently queried fields
- Implement caching for repeated API calls to external services
- Use Django's `select_related()` and `prefetch_related()` for query optimization
- For Phase 3, use Redis for session storage

### Security
- Validate and sanitize all user inputs
- Implement rate limiting for API endpoints
- Use environment variables for all secrets
- Implement authentication (Django's built-in or JWT)
- Add CORS configuration for production

### Monitoring & Logging
- Configure Django LOGGING in settings.py
- Log to file with appropriate levels (INFO, WARNING, ERROR)
- Set up handlers for different log destinations
- Use structured logging for easier parsing

## Resources

### Documentation
- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- React: https://react.dev/
- Vite: https://vitejs.dev/
- Tailwind CSS: https://tailwindcss.com/
- shadcn/ui: https://ui.shadcn.com/
- LangChain: https://python.langchain.com/
- Django Channels: https://channels.readthedocs.io/

### Example Projects
- Build a chatbot with Django: [Search GitHub for django-chatbot examples]
- React chat UI components: [Search for react-chat-ui or similar]
- LangChain conversational agents: [LangChain documentation examples]

## Troubleshooting

### Common Issues

**CORS errors in development**:
- Add 'corsheaders' to INSTALLED_APPS
- Add 'corsheaders.middleware.CorsMiddleware' to MIDDLEWARE
- Configure CORS_ALLOWED_ORIGINS with frontend URL

**WebSocket connection fails**:
- Ensure Redis is running with `redis-server`
- Check ASGI server is running, not WSGI
- Verify WebSocket URL uses `ws://` or `wss://`

**Database migrations conflict**:
- Reset migrations in development only
- Migrate to zero, remove migrations folder, recreate and apply

## Next Steps After Setup

1. **Phase 1 Implementation**:
   - Create basic chat UI
   - Implement rule-based intent detection
   - Build create_change_request handler
   - Test end-to-end flow

2. **Add More Intents**:
   - Update change request
   - Cancel change request
   - Link Jira issue to change
   - Link GitHub PR to change

3. **Phase 2 (AI)**:
   - Integrate OpenAI API
   - Implement AI intent detection
   - Add entity extraction
   - Test with complex user inputs

4. **Phase 3 (Real-time)**:
   - Set up Django Channels
   - Implement WebSocket consumer
   - Update frontend to use WebSockets
   - Add typing indicators

5. **Production Readiness**:
   - Add authentication
   - Implement rate limiting
   - Add comprehensive error handling
   - Write full test suite
   - Set up CI/CD pipeline
   - Deploy to production
