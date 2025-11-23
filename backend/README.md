# Chatbot Backend - Testing & Understanding Guide

## 📊 Current State

Your backend has:
- ✅ 8 conversations
- ✅ 53 messages
- ✅ 4 change requests created
- ✅ Fully functional REST API
- ✅ Django admin interface

## 🚀 Quick Start

### 1. Start the Server
```bash
cd backend
uv run python manage.py runserver
```

Server will be available at: **http://localhost:8000**

### 2. Test the API (Choose One)

#### Option A: Interactive Python Client (Recommended)
```bash
python interactive_client.py
```
Then chat naturally:
```
You: create a change request
You: Deploy API v3
You: Upgrade to latest version
You: 2
You: 2025-04-01
You: 2025-04-15
```

#### Option B: Automated Test Script
```bash
./test_api.sh
```

#### Option C: Manual curl Commands
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "help"}'
```

### 3. View Data in Django Admin
```bash
# First time: create admin user
uv run python manage.py createsuperuser

# Then visit
http://localhost:8000/admin/
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | This file - overview and quick start |
| `QUICK_START.md` | 5 different testing methods explained |
| `API_TESTING_GUIDE.md` | Detailed API examples with curl commands |
| `test_api.sh` | Bash script - automated testing |
| `interactive_client.py` | Python script - interactive chat |

---

## 🎯 What Each Tool Does

### interactive_client.py
**Best for:** Natural conversation testing
```
╔════════════════════════════════════════════╗
║    IT Change Management Chatbot           ║
╚════════════════════════════════════════════╝

You: hello
Bot: Hello! I'm your IT Change Management Assistant...

You: create a change request
Bot: What's a brief summary of the change?

You: /changes
✓ Total Change Requests: 4
  - CHG0000001: Deploy API v2 [New]
  - CHG0000002: Database upgrade [New]
```

### test_api.sh
**Best for:** Quick automated testing
- Runs all test scenarios
- Shows formatted output
- Displays results with colors
- Tests full conversation flows

### Django Admin
**Best for:** Visual data inspection
- Browse conversations
- View message history
- Inspect change requests
- Search and filter
- Manually edit data

### curl Commands
**Best for:** Understanding HTTP requests
- See raw request/response
- Learn API structure
- Debugging
- Integration testing

---

## 🔍 Understanding the APIs

### Main Endpoints

#### 1. Chat Message API
```
POST /api/chat/message/
```
**Purpose:** Send messages to the chatbot

**Flow:**
```
Request → Intent Detection → Handler → Response
```

**Intents Supported:**
- `greeting` - "hello", "hi"
- `help` - "help", "what can you do"
- `create_change_request` - "create change", "new ticket"
- `check_status` - "check status", "find CHG0000001"

#### 2. Conversations API
```
GET /api/chat/conversations/          # List all
GET /api/chat/conversations/{uuid}/   # Get one
DELETE /api/chat/conversations/{uuid}/delete/  # Delete
```

#### 3. Change Requests API
```
GET /api/change-requests/       # List all
GET /api/change-requests/{id}/  # Get one
```

---

## 💡 Example Scenarios

### Scenario 1: Create a Change Request
```bash
# Step 1: Initiate
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "create a change request"}'

# Response will include conversation_id
# Use it in subsequent requests

# Step 2-6: Answer the bot's questions
# - Short description
# - Detailed description
# - Priority (1-4)
# - Start date (YYYY-MM-DD)
# - End date (YYYY-MM-DD)

# Final response will include change_request details
```

### Scenario 2: Check Status
```bash
# Step 1
curl -X POST http://localhost:8000/api/chat/message/ \
  -d '{"message": "check status"}'

# Step 2: Provide CHG number
curl -X POST http://localhost:8000/api/chat/message/ \
  -d '{"conversation_id": "from-step-1", "message": "CHG0000001"}'
```

---

## 🔧 Useful Commands

### View Database
```bash
uv run python manage.py shell
```
```python
from chatbot.models import Conversation, Message
from integrations.models import ChangeRequest

# Count records
Conversation.objects.count()
ChangeRequest.objects.count()

# View all change requests
for cr in ChangeRequest.objects.all():
    print(f"{cr.number}: {cr.short_description}")

# View a conversation
conv = Conversation.objects.first()
for msg in conv.messages.all():
    print(f"{msg.sender}: {msg.text}")
```

### Check API Health
```bash
curl http://localhost:8000/api/chat/conversations/ | python3 -m json.tool
```

### View Server Logs
```bash
tail -f /tmp/django.log
```

### Database Migrations
```bash
uv run python manage.py makemigrations  # Create migrations
uv run python manage.py migrate         # Apply migrations
```

---

## 🎨 Architecture Overview

```
User → API Endpoint → View → Intent Detection → Handler → Database
                                                      ↓
                                               Response ← Serializer
```

**Components:**
- **Models** (`models.py`) - Database structure
- **Serializers** (`serializers.py`) - JSON ↔ Python conversion
- **Views** (`views.py`) - API endpoints
- **Intents** (`intents.py`) - Keyword-based intent detection
- **Handlers** (`handlers.py`) - Business logic for each intent
- **Services** (`integrations/services.py`) - External API calls (ServiceNow, Jira, GitHub)

---

## 🐛 Troubleshooting

**Port already in use:**
```bash
pkill -f "manage.py runserver"
uv run python manage.py runserver 8001  # Use different port
```

**Module not found:**
```bash
uv sync  # Reinstall dependencies
```

**Database errors:**
```bash
rm db.sqlite3  # Warning: deletes all data!
uv run python manage.py migrate
```

**Cannot connect to API:**
```bash
# Check if server is running
ps aux | grep "manage.py runserver"

# Check server status
curl http://localhost:8000/admin/
```

---

## 📖 Next Steps

1. **Test the API** - Use one of the methods above
2. **Explore Django Admin** - Visual interface at http://localhost:8000/admin/
3. **Read the guides** - Check QUICK_START.md and API_TESTING_GUIDE.md
4. **Build the frontend** - React UI to connect to this API (see ../frontend/)
5. **Implement ServiceNow** - Real API integration in integrations/services.py
6. **Add tests** - Write unit tests for handlers and views

---

## 📝 API Response Format

All chat responses follow this structure:
```json
{
  "conversation_id": "uuid",
  "intent": "intent_name",
  "bot_message": "Bot's response text",
  "required_fields": ["field1", "field2"],
  "collected_data": {"field1": "value1"},
  "next_field": "field2",
  "is_complete": true/false,
  "change_request": {  // Only when created
    "number": "CHG0000001",
    "sys_id": "...",
    "id": 1
  }
}
```

---

## 🎓 Learning Resources

- **Django Docs:** https://docs.djangoproject.com/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **curl Tutorial:** https://curl.se/docs/manual.html
- **Postman:** https://www.postman.com/

---

Made with ❤️ using Django REST Framework
