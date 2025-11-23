# API Testing Guide

## Available Endpoints

### Chat Endpoints
```
POST   /api/chat/message/                    - Send a chat message
GET    /api/chat/conversations/              - List all conversations
GET    /api/chat/conversations/{uuid}/       - Get specific conversation
DELETE /api/chat/conversations/{uuid}/delete/ - Delete a conversation
```

### Integration Endpoints
```
GET    /api/change-requests/                 - List all change requests
GET    /api/change-requests/{id}/            - Get specific change request
```

### Admin
```
GET    /admin/                               - Django admin interface
```

---

## Test Examples

### 1. Start a New Conversation (Greeting)
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

**Expected Response:**
```json
{
  "conversation_id": "uuid-here",
  "intent": "greeting",
  "bot_message": "Hello! I'm your IT Change Management Assistant...",
  "is_complete": true
}
```

---

### 2. Create a Change Request (Full Flow)

**Step 1: Initiate**
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "create a change request"}'
```

**Response:**
```json
{
  "conversation_id": "abc-123-...",
  "intent": "create_change_request",
  "bot_message": "What's a brief summary of the change?",
  "required_fields": ["short_description", "description", "priority", "planned_start_date", "planned_end_date"],
  "next_field": "short_description",
  "is_complete": false
}
```

**Step 2: Provide Short Description**
```bash
CONV_ID="abc-123-..."  # Use the conversation_id from Step 1

curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"Deploy new API version\"}"
```

**Step 3: Provide Description**
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"Deploy v2.0 of the REST API with breaking changes\"}"
```

**Step 4: Provide Priority (1-4)**
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"2\"}"
```

**Step 5: Provide Start Date**
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"2025-02-01\"}"
```

**Step 6: Provide End Date (Final)**
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"2025-02-10\"}"
```

**Final Response:**
```json
{
  "conversation_id": "abc-123-...",
  "intent": "create_change_request",
  "bot_message": "✓ Change request CHG0000004 created successfully!\n\nSummary: Deploy new API version\nPriority: 2\nStatus: New",
  "is_complete": true,
  "change_request": {
    "number": "CHG0000004",
    "sys_id": "...",
    "id": 4
  }
}
```

---

### 3. Check Status of Change Request

**Step 1: Ask to check status**
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "check status"}'
```

**Step 2: Provide CHG number**
```bash
CONV_ID="..."  # From step 1 response

curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"CHG0000004\"}"
```

**Response:**
```json
{
  "bot_message": "Change Request: CHG0000004\n\nSummary: Deploy new API version\nDescription: ...\nStatus: New\nPriority: 2\nCreated: 2025-11-23 17:30",
  "change_request": {
    "number": "CHG0000004",
    "sys_id": "...",
    "id": 4
  }
}
```

---

### 4. Get Help

```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "help"}'
```

---

### 5. List All Conversations

```bash
curl http://localhost:8000/api/chat/conversations/
```

**Response:**
```json
[
  {
    "id": "uuid-1",
    "status": "completed",
    "started_at": "2025-11-23T16:51:00Z",
    "messages": [...],
    "context": {...}
  }
]
```

---

### 6. Get Specific Conversation

```bash
CONV_ID="uuid-here"

curl http://localhost:8000/api/chat/conversations/$CONV_ID/
```

---

### 7. List All Change Requests

```bash
curl http://localhost:8000/api/change-requests/
```

---

### 8. Get Specific Change Request

```bash
curl http://localhost:8000/api/change-requests/1/
```

---

## Intent Keywords

The chatbot detects intents based on keywords:

### Create Change Request
- "create", "new", "make", "add", "start" + "change", "ticket", "request", "cr"
- Examples: "create a change request", "new change", "add a ticket"

### Check Status
- "status", "check", "show", "find", "lookup" + "change", "ticket", "CHG"
- Examples: "check status", "find CHG0000001", "status of change"

### Help
- "help", "what can you do", "commands", "how to"
- Examples: "help", "what can you do?"

### Greeting
- "hello", "hi", "hey", "good morning"
- Examples: "Hello", "Hi there"

---

## Testing Tips

1. **Use `jq` for pretty JSON:**
   ```bash
   curl ... | jq
   ```

2. **Save conversation_id for multi-step flows:**
   ```bash
   CONV_ID=$(curl -X POST ... | jq -r '.conversation_id')
   ```

3. **Check server logs:**
   ```bash
   tail -f /tmp/django.log
   ```

4. **View database records:**
   ```bash
   uv run python manage.py shell
   >>> from integrations.models import ChangeRequest
   >>> ChangeRequest.objects.all()
   ```
