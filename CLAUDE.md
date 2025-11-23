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
```python
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Future: for auth
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned')
    ])
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
```

**Message** - Individual chat messages
```python
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=10, choices=[
        ('user', 'User'),
        ('bot', 'Bot')
    ])
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(null=True, blank=True)  # For rich content

    class Meta:
        ordering = ['timestamp']
```

**ConversationContext** - Tracks conversation state
```python
class ConversationContext(models.Model):
    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, related_name='context')
    intent = models.CharField(max_length=50, null=True, blank=True)
    collected_data = models.JSONField(default=dict)  # Fields collected so far
    required_fields = models.JSONField(default=list)  # Fields still needed
    next_field = models.CharField(max_length=50, null=True, blank=True)
    change_request = models.ForeignKey('integrations.ChangeRequest', null=True, blank=True, on_delete=models.SET_NULL)

    def is_complete(self):
        return len(self.required_fields) == 0
```

### Integrations App Models

**ChangeRequest** - Links to ServiceNow changes
```python
class ChangeRequest(models.Model):
    # ServiceNow fields
    servicenow_sys_id = models.CharField(max_length=32, unique=True)
    number = models.CharField(max_length=40)  # CHG0030001
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    state = models.CharField(max_length=20)
    priority = models.CharField(max_length=10)

    # Integration links
    jira_issue_key = models.CharField(max_length=50, null=True, blank=True)
    github_repo = models.CharField(max_length=100, null=True, blank=True)
    github_pr_number = models.IntegerField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['servicenow_sys_id']),
            models.Index(fields=['number']),
            models.Index(fields=['jira_issue_key']),
        ]
```

## API Design

### Chat API Endpoints

**POST /api/chat/message/**
Send a message and get bot response

Request:
```json
{
  "conversation_id": "uuid-or-null",  // null for new conversation
  "message": "I want to create a change request"
}
```

Response:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "intent": "create_change_request",
  "bot_message": "I'll help you create a change request. What's the short description?",
  "required_fields": ["short_description", "description", "priority"],
  "collected_data": {},
  "next_field": "short_description",
  "is_complete": false
}
```

**GET /api/chat/conversations/**
List user's conversations

Response:
```json
{
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "active",
      "started_at": "2025-01-15T10:30:00Z",
      "last_message": "I'll help you create a change request...",
      "message_count": 5
    }
  ]
}
```

**GET /api/chat/conversations/{id}/**
Get conversation with all messages

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "active",
  "started_at": "2025-01-15T10:30:00Z",
  "messages": [
    {
      "id": 1,
      "sender": "user",
      "text": "I want to create a change request",
      "timestamp": "2025-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "sender": "bot",
      "text": "I'll help you create a change request...",
      "timestamp": "2025-01-15T10:30:01Z"
    }
  ],
  "context": {
    "intent": "create_change_request",
    "collected_data": {},
    "next_field": "short_description"
  }
}
```

### Integration API Endpoints

**GET /api/change-requests/**
List change requests

**GET /api/change-requests/{id}/**
Get change request details

**GET /api/change-requests/by_servicenow_number/?number=CHG0030001**
Find by ServiceNow number

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
```python
# chatbot/intents.py
def detect_intent(message: str) -> str:
    """Simple keyword-based intent detection"""
    message_lower = message.lower()

    # Create change request
    if any(word in message_lower for word in ['create', 'new', 'make', 'add']):
        if any(word in message_lower for word in ['change', 'ticket', 'request']):
            return 'create_change_request'

    # Check status
    if any(word in message_lower for word in ['status', 'check', 'show', 'find']):
        return 'check_status'

    # Update change
    if any(word in message_lower for word in ['update', 'modify', 'edit', 'change']):
        return 'update_change_request'

    # Help
    if any(word in message_lower for word in ['help', 'what can you do']):
        return 'help'

    return 'unknown'
```

**Intent Handler Example**:
```python
# chatbot/handlers.py
class CreateChangeRequestHandler:
    REQUIRED_FIELDS = [
        'short_description',
        'description',
        'priority',
        'planned_start_date',
        'planned_end_date'
    ]

    FIELD_PROMPTS = {
        'short_description': "What's a brief summary of the change?",
        'description': "Please provide a detailed description of the change.",
        'priority': "What's the priority? (1-Critical, 2-High, 3-Medium, 4-Low)",
        'planned_start_date': "When do you plan to start? (YYYY-MM-DD)",
        'planned_end_date': "When should this be completed? (YYYY-MM-DD)"
    }

    def handle(self, context: ConversationContext, message: str) -> dict:
        """Handle create_change_request intent"""

        # Initialize context if new intent
        if not context.intent:
            context.intent = 'create_change_request'
            context.required_fields = self.REQUIRED_FIELDS.copy()
            context.next_field = self.REQUIRED_FIELDS[0]
            context.save()

            return {
                'bot_message': self.FIELD_PROMPTS[context.next_field],
                'is_complete': False
            }

        # Collect current field value
        current_field = context.next_field
        context.collected_data[current_field] = message
        context.required_fields.remove(current_field)

        # Check if more fields needed
        if context.required_fields:
            context.next_field = context.required_fields[0]
            context.save()

            return {
                'bot_message': self.FIELD_PROMPTS[context.next_field],
                'is_complete': False
            }

        # All fields collected - create change request
        change_request = self._create_change_request(context.collected_data)
        context.change_request = change_request
        context.save()

        return {
            'bot_message': f"Change request {change_request.number} created successfully!",
            'is_complete': True,
            'change_request': {
                'number': change_request.number,
                'sys_id': change_request.servicenow_sys_id,
                'url': f"https://your-instance.service-now.com/nav_to.do?uri=change_request.do?sys_id={change_request.servicenow_sys_id}"
            }
        }

    def _create_change_request(self, data: dict) -> ChangeRequest:
        """Call ServiceNow API to create change request"""
        from integrations.services import ServiceNowService

        service = ServiceNowService()
        snow_response = service.create_change_request(
            short_description=data['short_description'],
            description=data['description'],
            priority=data['priority'],
            planned_start_date=data['planned_start_date'],
            planned_end_date=data['planned_end_date']
        )

        # Create local record
        change_request = ChangeRequest.objects.create(
            servicenow_sys_id=snow_response['sys_id'],
            number=snow_response['number'],
            short_description=data['short_description'],
            description=data['description'],
            priority=data['priority'],
            state=snow_response['state']
        )

        return change_request
```

**API View**:
```python
# chatbot/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message, ConversationContext
from .intents import detect_intent
from .handlers import CreateChangeRequestHandler, CheckStatusHandler

class ChatMessageView(APIView):
    """Handle chat messages"""

    def post(self, request):
        conversation_id = request.data.get('conversation_id')
        user_message = request.data.get('message')

        if not user_message:
            return Response(
                {'error': 'Message is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create conversation
        if conversation_id:
            conversation = Conversation.objects.get(id=conversation_id)
        else:
            conversation = Conversation.objects.create(status='active')
            ConversationContext.objects.create(conversation=conversation)

        # Save user message
        Message.objects.create(
            conversation=conversation,
            sender='user',
            text=user_message
        )

        # Get context
        context = conversation.context

        # Detect intent if not already set
        if not context.intent:
            intent = detect_intent(user_message)
            context.intent = intent
            context.save()

        # Route to appropriate handler
        handler = self._get_handler(context.intent)
        result = handler.handle(context, user_message)

        # Save bot response
        Message.objects.create(
            conversation=conversation,
            sender='bot',
            text=result['bot_message']
        )

        # Mark conversation as completed if done
        if result.get('is_complete'):
            conversation.status = 'completed'
            conversation.save()

        # Build response
        response_data = {
            'conversation_id': str(conversation.id),
            'intent': context.intent,
            'bot_message': result['bot_message'],
            'required_fields': context.required_fields,
            'collected_data': context.collected_data,
            'next_field': context.next_field,
            'is_complete': result.get('is_complete', False)
        }

        if 'change_request' in result:
            response_data['change_request'] = result['change_request']

        return Response(response_data)

    def _get_handler(self, intent: str):
        handlers = {
            'create_change_request': CreateChangeRequestHandler(),
            'check_status': CheckStatusHandler(),
            # Add more handlers as needed
        }
        return handlers.get(intent, CreateChangeRequestHandler())
```

**Frontend Chat Component**:
```typescript
// src/components/chat/ChatWindow.tsx
import React, { useState, useEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';
import { InputBox } from './InputBox';
import { chatApi } from '@/services/chatApi';
import type { Message, Conversation } from '@/types/chat.types';

export const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now(),
      sender: 'user',
      text,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);

    setIsLoading(true);

    try {
      const response = await chatApi.sendMessage({
        conversation_id: conversationId,
        message: text
      });

      // Update conversation ID if new
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add bot response
      const botMessage: Message = {
        id: Date.now() + 1,
        sender: 'bot',
        text: response.bot_message,
        timestamp: new Date().toISOString(),
        metadata: {
          intent: response.intent,
          change_request: response.change_request
        }
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      // Show error message
      const errorMessage: Message = {
        id: Date.now() + 1,
        sender: 'bot',
        text: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b px-6 py-4 shadow-sm">
        <h1 className="text-xl font-semibold text-gray-800">
          IT Change Management Assistant
        </h1>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg mb-2">Welcome! How can I help you today?</p>
            <p className="text-sm">
              Try saying: "I want to create a change request"
            </p>
          </div>
        )}

        {messages.map(message => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 text-gray-500">
            <div className="animate-pulse">●</div>
            <div className="animate-pulse animation-delay-200">●</div>
            <div className="animate-pulse animation-delay-400">●</div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <InputBox
        onSend={handleSendMessage}
        disabled={isLoading}
      />
    </div>
  );
};
```

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
```python
# chatbot/intents.py
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class IntentDetectionResult(BaseModel):
    intent: str = Field(description="The detected intent")
    confidence: float = Field(description="Confidence score 0-1")
    entities: dict = Field(description="Extracted entities")

class AIIntentDetector:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.parser = PydanticOutputParser(pydantic_object=IntentDetectionResult)

    def detect_intent(self, message: str, conversation_history: list = None) -> IntentDetectionResult:
        """Use LLM to detect intent and extract entities"""

        system_prompt = """You are an intent classifier for an IT change management chatbot.

Available intents:
- create_change_request: User wants to create a new change request
- check_status: User wants to check the status of an existing change
- update_change_request: User wants to update an existing change
- list_changes: User wants to see all changes
- help: User needs help understanding what the bot can do
- unknown: Cannot determine intent

Extract any relevant entities like:
- priority (1-4, critical, high, medium, low)
- dates (start date, end date)
- descriptions or titles
- change request numbers (CHG followed by numbers)

{format_instructions}
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{message}")
        ])

        chain = prompt | self.llm | self.parser

        result = chain.invoke({
            "message": message,
            "format_instructions": self.parser.get_format_instructions()
        })

        return result
```

**Smart Entity Extraction**:
```python
# chatbot/handlers.py
class SmartCreateChangeRequestHandler:
    """AI-enhanced handler that pre-fills data from initial message"""

    def handle(self, context: ConversationContext, message: str) -> dict:
        # Use AI to extract entities from message
        detector = AIIntentDetector()
        result = detector.detect_intent(message)

        # Pre-fill any extracted entities
        if result.entities:
            for field, value in result.entities.items():
                if field in self.REQUIRED_FIELDS:
                    context.collected_data[field] = value
                    if field in context.required_fields:
                        context.required_fields.remove(field)

        context.save()

        # Continue with normal flow
        # ...
```

**Conversational Memory**:
```python
# chatbot/context_manager.py
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

class ConversationManager:
    """Manages conversation context with LLM memory"""

    def __init__(self, conversation: Conversation):
        self.conversation = conversation
        self.memory = ConversationBufferMemory()

        # Load previous messages into memory
        for msg in conversation.messages.all():
            if msg.sender == 'user':
                self.memory.chat_memory.add_user_message(msg.text)
            else:
                self.memory.chat_memory.add_ai_message(msg.text)

    def get_response(self, user_message: str) -> str:
        """Get contextual response using conversation history"""
        llm = ChatOpenAI(model="gpt-4")
        chain = ConversationChain(llm=llm, memory=self.memory)

        response = chain.predict(input=user_message)
        return response
```

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
```python
# config/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatbot import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
```

**WebSocket Consumer**:
```python
# chatbot/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message, ConversationContext
from .intents import detect_intent
from .handlers import CreateChangeRequestHandler

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Send welcome message
        await self.send_json({
            'type': 'bot_message',
            'message': 'Welcome! How can I help you today?'
        })

    async def disconnect(self, close_code):
        pass

    async def receive_json(self, content):
        message_type = content.get('type')

        if message_type == 'user_message':
            await self.handle_user_message(content)
        elif message_type == 'typing':
            # Echo typing indicator back
            await self.send_json({
                'type': 'typing',
                'is_typing': content.get('is_typing', False)
            })

    async def handle_user_message(self, content):
        user_message = content.get('message')
        conversation_id = content.get('conversation_id')

        # Show typing indicator
        await self.send_json({
            'type': 'bot_typing',
            'is_typing': True
        })

        # Process message (use database_sync_to_async for ORM calls)
        response = await self.process_message(user_message, conversation_id)

        # Hide typing indicator
        await self.send_json({
            'type': 'bot_typing',
            'is_typing': False
        })

        # Send response
        await self.send_json({
            'type': 'bot_message',
            **response
        })

    @database_sync_to_async
    def process_message(self, user_message, conversation_id):
        # Same logic as REST API view
        # ...
        return {
            'message': bot_message,
            'conversation_id': str(conversation_id),
            # ...
        }
```

**WebSocket Routing**:
```python
# chatbot/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]
```

**Frontend WebSocket Hook**:
```typescript
// src/hooks/useWebSocket.ts
import { useEffect, useState, useRef, useCallback } from 'react';
import type { Message } from '@/types/chat.types';

export const useWebSocket = (url: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'bot_message') {
        const message: Message = {
          id: Date.now(),
          sender: 'bot',
          text: data.message,
          timestamp: new Date().toISOString(),
          metadata: data
        };
        setMessages(prev => [...prev, message]);
      } else if (data.type === 'bot_typing') {
        setIsBotTyping(data.is_typing);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  const sendMessage = useCallback((text: string, conversationId?: string) => {
    if (wsRef.current && isConnected) {
      // Add user message to UI
      const userMessage: Message = {
        id: Date.now(),
        sender: 'user',
        text,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, userMessage]);

      // Send to server
      wsRef.current.send(JSON.stringify({
        type: 'user_message',
        message: text,
        conversation_id: conversationId
      }));
    }
  }, [isConnected]);

  const sendTypingIndicator = useCallback((isTyping: boolean) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify({
        type: 'typing',
        is_typing: isTyping
      }));
    }
  }, [isConnected]);

  return {
    messages,
    isConnected,
    isBotTyping,
    sendMessage,
    sendTypingIndicator
  };
};
```

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

```bash
# Create project directory
mkdir chatbot-app
cd chatbot-app

# Initialize git
git init

# Create directory structure
mkdir backend frontend

# Create .gitignore (see below for contents)
touch .gitignore
```

### Backend Setup

```bash
cd backend

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize uv project
uv init

# Add Django dependencies
uv add django djangorestframework django-cors-headers python-decouple psycopg2-binary

# Create Django project
uv run django-admin startproject config .

# Create apps
uv run python manage.py startapp chatbot
uv run python manage.py startapp integrations

# For Phase 2 (AI)
# uv add langchain openai

# For Phase 3 (WebSockets)
# uv add channels channels-redis redis

# Create environment file
cp .env.example .env
# Edit .env with your credentials

# Run migrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser

# Test server
uv run python manage.py runserver
```

### Frontend Setup

```bash
cd ../frontend

# Create React app with Vite
npm create vite@latest . -- --template react-ts

# Install dependencies
npm install

# Install UI dependencies
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install shadcn/ui
npx shadcn-ui@latest init

# Install additional packages
npm install axios zustand

# Create environment file
cp .env.example .env.local
# Edit if needed (default VITE_API_URL=http://localhost:8000)

# Test dev server
npm run dev
```

### Running Both in Development

You'll need two terminal windows:

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

**Access:**
- Frontend UI: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/

### Environment Variables

**Backend (.env)**:
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_ENGINE=postgresql
DB_NAME=chatbot_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# For development, use SQLite instead:
# DB_ENGINE=sqlite3

# CORS (for local development)
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

# Phase 2: OpenAI (for AI features)
OPENAI_API_KEY=sk-...

# Phase 3: Redis (for Channels)
REDIS_URL=redis://localhost:6379/0
```

**Frontend (.env.local)**:
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## Testing Strategy

### Backend Tests

```python
# chatbot/tests/test_intents.py
from django.test import TestCase
from chatbot.intents import detect_intent

class IntentDetectionTestCase(TestCase):
    def test_create_change_request_intent(self):
        message = "I want to create a new change request"
        intent = detect_intent(message)
        self.assertEqual(intent, 'create_change_request')

    def test_check_status_intent(self):
        message = "What's the status of CHG0030001?"
        intent = detect_intent(message)
        self.assertEqual(intent, 'check_status')
```

```python
# chatbot/tests/test_handlers.py
from django.test import TestCase
from chatbot.models import Conversation, ConversationContext
from chatbot.handlers import CreateChangeRequestHandler

class CreateChangeRequestHandlerTestCase(TestCase):
    def setUp(self):
        self.conversation = Conversation.objects.create(status='active')
        self.context = ConversationContext.objects.create(conversation=self.conversation)
        self.handler = CreateChangeRequestHandler()

    def test_initial_prompt(self):
        result = self.handler.handle(self.context, "I want to create a change")
        self.assertIn("short description", result['bot_message'].lower())
        self.assertFalse(result['is_complete'])

    def test_field_collection(self):
        # Simulate collecting all fields
        # ...
```

### Frontend Tests

```typescript
// src/components/chat/__tests__/ChatWindow.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChatWindow } from '../ChatWindow';
import { chatApi } from '@/services/chatApi';

jest.mock('@/services/chatApi');

describe('ChatWindow', () => {
  it('renders welcome message', () => {
    render(<ChatWindow />);
    expect(screen.getByText(/welcome/i)).toBeInTheDocument();
  });

  it('sends message and displays response', async () => {
    const mockResponse = {
      conversation_id: '123',
      bot_message: 'How can I help you?',
      intent: 'unknown'
    };

    (chatApi.sendMessage as jest.Mock).mockResolvedValue(mockResponse);

    render(<ChatWindow />);

    const input = screen.getByPlaceholderText(/type a message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('How can I help you?')).toBeInTheDocument();
    });
  });
});
```

## Deployment Considerations

### Backend Deployment

**Production Settings**:
```python
# config/settings.py
import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Security
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

**Docker Setup**:
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml requirements.txt ./

# Install dependencies
RUN uv pip install --system -r requirements.txt

# Copy application
COPY . .

# Run migrations and collect static files
RUN python manage.py collectstatic --noinput

# Start server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Frontend Deployment

**Build for Production**:
```bash
npm run build
```

**Vercel/Netlify** (easiest):
- Connect GitHub repo
- Auto-deploy on push

**Nginx** (traditional):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/chatbot-frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

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
```python
# config/settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'chatbot.log',
        },
    },
    'loggers': {
        'chatbot': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

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
```python
# config/settings.py
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]
```

**WebSocket connection fails**:
- Ensure Redis is running: `redis-server`
- Check ASGI server is running, not WSGI
- Verify WebSocket URL uses `ws://` or `wss://`

**Database migrations conflict**:
```bash
# Reset migrations (development only!)
uv run python manage.py migrate chatbot zero
rm -rf chatbot/migrations/
uv run python manage.py makemigrations chatbot
uv run python manage.py migrate
```

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
