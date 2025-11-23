# Quick Start Guide - Testing Your APIs

## 5 Ways to Test the Chatbot API

### Method 1: Bash Test Script (Automated)
```bash
cd backend
./test_api.sh
```
**What it does:** Runs all API tests automatically and shows results

---

### Method 2: Python Interactive Client (Recommended)
```bash
cd backend
uv add requests  # Install requests library
python interactive_client.py
```

**What it does:** Interactive chat interface in your terminal
```
You: create a change request
Bot: I'll help you create a change request. What's a brief summary of the change?

You: Deploy API v2
Bot: Please provide a detailed description of the change.
...
```

**Commands:**
- `/new` - Start new conversation
- `/list` - List all conversations
- `/changes` - List all change requests
- `/quit` - Exit

---

### Method 3: curl Commands (Manual)
```bash
# 1. Send a message
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# 2. List conversations
curl http://localhost:8000/api/chat/conversations/

# 3. List change requests
curl http://localhost:8000/api/change-requests/
```

See `API_TESTING_GUIDE.md` for more examples.

---

### Method 4: Django Admin Interface (Visual)
```bash
# 1. Create superuser (first time only)
cd backend
uv run python manage.py createsuperuser

# 2. Start server
uv run python manage.py runserver

# 3. Open browser
http://localhost:8000/admin/
```

**What you can do:**
- ✅ View all conversations
- ✅ See message history
- ✅ Inspect conversation contexts
- ✅ Browse change requests
- ✅ Manually create/edit records
- ✅ Search and filter data

**Screenshot of Admin:**
```
┌─────────────────────────────────────────┐
│ Django Administration                   │
├─────────────────────────────────────────┤
│ CHATBOT                                 │
│   Conversations        [View] [Add]     │
│   Messages             [View] [Add]     │
│   Conversation Contexts [View] [Add]    │
│                                         │
│ INTEGRATIONS                            │
│   Change Requests      [View] [Add]     │
└─────────────────────────────────────────┘
```

---

### Method 5: Postman / Insomnia (GUI Tool)

**Postman Setup:**
1. Download Postman: https://www.postman.com/downloads/
2. Import endpoints:
   - POST `http://localhost:8000/api/chat/message/`
   - GET `http://localhost:8000/api/chat/conversations/`
   - GET `http://localhost:8000/api/change-requests/`
3. Set Headers: `Content-Type: application/json`
4. Send requests with JSON body

---

## What Each API Does

### 1. POST /api/chat/message/
**Purpose:** Main chatbot endpoint - send messages and get responses

**Request:**
```json
{
  "message": "create a change request",
  "conversation_id": "uuid-or-null"
}
```

**Response:**
```json
{
  "conversation_id": "abc-123",
  "intent": "create_change_request",
  "bot_message": "What's a brief summary?",
  "required_fields": ["short_description", ...],
  "next_field": "short_description",
  "is_complete": false
}
```

---

### 2. GET /api/chat/conversations/
**Purpose:** List all conversations

**Response:**
```json
[
  {
    "id": "uuid",
    "status": "completed",
    "started_at": "2025-11-23T10:00:00Z",
    "messages": [...],
    "context": {...}
  }
]
```

---

### 3. GET /api/chat/conversations/{uuid}/
**Purpose:** Get specific conversation with full message history

---

### 4. DELETE /api/chat/conversations/{uuid}/delete/
**Purpose:** Delete a conversation

---

### 5. GET /api/change-requests/
**Purpose:** List all change requests created

**Response:**
```json
[
  {
    "id": 1,
    "number": "CHG0000001",
    "short_description": "Deploy API v2",
    "description": "...",
    "state": "New",
    "priority": "2",
    "created_at": "2025-11-23T10:00:00Z"
  }
]
```

---

### 6. GET /api/change-requests/{id}/
**Purpose:** Get specific change request details

---

## Understanding the Flow

### Simple Intent (Help):
```
User: "help"
  ↓
Intent Detection: "help"
  ↓
HelpHandler: Returns help text
  ↓
Bot: "I can help you with..."
  ↓
is_complete: true (done)
```

### Multi-Step Intent (Create Change Request):
```
User: "create change request"
  ↓
Intent: "create_change_request"
  ↓
Handler: Initialize context
  required_fields: [short_description, description, priority, ...]
  next_field: "short_description"
  ↓
Bot: "What's a brief summary?"
  ↓
User: "Deploy API v2"
  ↓
Handler: Save to context, move to next field
  collected_data: {"short_description": "Deploy API v2"}
  next_field: "description"
  ↓
Bot: "Please provide a detailed description"
  ↓
... (continues for each field)
  ↓
Handler: All fields collected → Create ChangeRequest in database
  ↓
Bot: "✓ Change request CHG0000001 created!"
  is_complete: true
```

---

## Troubleshooting

**Server not running?**
```bash
cd backend
uv run python manage.py runserver
```

**Check if server is up:**
```bash
curl http://localhost:8000/admin/
```

**View server logs:**
```bash
tail -f /tmp/django.log
```

**Check database:**
```bash
uv run python manage.py shell
>>> from integrations.models import ChangeRequest
>>> ChangeRequest.objects.count()
>>> ChangeRequest.objects.all()
```

**Reset database (WARNING: deletes all data):**
```bash
rm db.sqlite3
uv run python manage.py migrate
```

---

## Next Steps

1. ✅ **Test with the interactive client** - Most user-friendly
2. ✅ **Explore Django Admin** - See your data visually
3. ✅ **Read API_TESTING_GUIDE.md** - Detailed examples
4. ✅ **Try curl commands** - Understand HTTP requests
5. ✅ **Build the frontend** - React UI to connect to this API
