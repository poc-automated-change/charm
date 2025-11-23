# Code Review Guide - File Reading Order

## 📚 Review Order: From Foundation to Implementation

### Phase 1: Project Configuration (Understanding the Setup)
**Goal:** Understand how the project is configured

#### 1. `.env.example` ⭐⭐⭐
**Why:** Shows what environment variables you need
**What to look for:**
- Database configuration options
- External service credentials (ServiceNow, Jira, GitHub)
- API keys for Phase 2 (OpenAI) and Phase 3 (Redis)

**Location:** `/backend/.env.example`

---

#### 2. `config/settings.py` ⭐⭐⭐⭐⭐
**Why:** Main Django configuration - controls everything
**What to look for:**
- Installed apps (lines 34-49)
- Middleware configuration (lines 51-60)
- Database setup (lines 85-104)
- CORS configuration (lines 148-153)
- REST Framework settings (lines 155-163)

**Location:** `/backend/config/settings.py`

**Key sections to review:**
```python
# Line 34-49: Installed apps
INSTALLED_APPS = [
    'chatbot',          # Our chat logic
    'integrations',     # ServiceNow integration
]

# Line 148-153: CORS (allows frontend to connect)
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5173',
)
```

---

#### 3. `config/urls.py` ⭐⭐⭐
**Why:** Maps URLs to views - the routing table
**What to look for:**
- API endpoint structure (lines 20-24)
- How URLs are organized

**Location:** `/backend/config/urls.py`

**Key lines:**
```python
# Line 22-23: Where our APIs are mounted
path('api/chat/', include('chatbot.urls')),
path('api/', include('integrations.urls')),
```

---

### Phase 2: Data Models (Understanding the Data Structure)
**Goal:** Understand what data we store and how

#### 4. `chatbot/models.py` ⭐⭐⭐⭐⭐
**Why:** Defines the database structure for conversations
**What to look for:**
- `Conversation` model (lines 8-34) - Chat sessions
- `Message` model (lines 37-60) - Individual messages
- `ConversationContext` model (lines 63-90) - Conversation state
- The `is_complete()` method (lines 88-90)

**Location:** `/backend/chatbot/models.py`

**Important concepts:**
```python
# UUIDs for conversations (secure, unique IDs)
id = models.UUIDField(primary_key=True, default=uuid.uuid4)

# JSONField for flexible data storage
collected_data = models.JSONField(default=dict)
required_fields = models.JSONField(default=list)
```

---

#### 5. `integrations/models.py` ⭐⭐⭐⭐
**Why:** Defines change request structure
**What to look for:**
- ServiceNow fields (lines 7-20)
- Integration links to Jira/GitHub (lines 22-39)
- Database indexes for performance (lines 48-52)

**Location:** `/backend/integrations/models.py`

---

### Phase 3: Business Logic (Understanding How It Works)
**Goal:** Understand the chatbot intelligence

#### 6. `chatbot/intents.py` ⭐⭐⭐⭐⭐
**Why:** Brain of the chatbot - detects what user wants
**What to look for:**
- `detect_intent()` function (lines 7-59) - Main intent detection
- Keyword matching logic (lines 15-45)
- Intent types supported

**Location:** `/backend/chatbot/intents.py`

**How it works:**
```python
# Checks for keywords to determine intent
if 'create' in message and 'change' in message:
    return 'create_change_request'
```

**Start here to understand:** How the bot knows what you want

---

#### 7. `chatbot/handlers.py` ⭐⭐⭐⭐⭐ (MOST IMPORTANT)
**Why:** Contains all the chatbot logic - how each intent is handled
**What to look for:**
- `CreateChangeRequestHandler` (lines 24-144) - Multi-step form logic
- `CheckStatusHandler` (lines 147-196) - Status lookup
- `HelpHandler` (lines 199-210) - Help text
- Handler registry (lines 253-261)

**Location:** `/backend/chatbot/handlers.py`

**Flow to understand:**
```python
1. User sends message
2. Intent detected → Handler selected
3. Handler processes message
4. Handler updates context
5. Handler returns response
```

**This is the CORE file** - spend the most time here!

---

#### 8. `chatbot/context_manager.py` ⭐⭐⭐
**Why:** Manages conversation state between messages
**What to look for:**
- `get_or_create_context()` (lines 11-23)
- `reset_context()` (lines 25-35)
- How context is managed

**Location:** `/backend/chatbot/context_manager.py`

**Simple utility file** - quick read

---

#### 9. `integrations/services.py` ⭐⭐⭐
**Why:** External API integration logic (ServiceNow, Jira, GitHub)
**What to look for:**
- ServiceNowService class (lines 8-68) - Currently placeholder
- How it will be implemented (comments)

**Location:** `/backend/integrations/services.py`

**Note:** Currently placeholders - will be implemented when you connect real ServiceNow

---

### Phase 4: API Layer (Understanding the Interface)
**Goal:** Understand how frontend communicates with backend

#### 10. `chatbot/serializers.py` ⭐⭐⭐⭐
**Why:** Converts between JSON and Python objects
**What to look for:**
- `MessageSerializer` (lines 7-13) - Message format
- `ChatMessageRequestSerializer` (lines 40-43) - What API expects
- `ChatMessageResponseSerializer` (lines 46-54) - What API returns

**Location:** `/backend/chatbot/serializers.py`

**Key concept:**
```python
# Incoming request format
conversation_id = serializers.UUIDField(required=False)
message = serializers.CharField(required=True, max_length=2000)

# Outgoing response format
bot_message = serializers.CharField()
is_complete = serializers.BooleanField()
```

---

#### 11. `chatbot/views.py` ⭐⭐⭐⭐⭐
**Why:** API endpoints - where HTTP requests are handled
**What to look for:**
- `ChatMessageView.post()` (lines 24-98) - Main chat endpoint
- Flow: Request → Validation → Intent → Handler → Response
- How conversation_id is managed

**Location:** `/backend/chatbot/views.py`

**Critical flow (lines 24-98):**
```python
1. Validate request (lines 28-33)
2. Get/create conversation (lines 35-42)
3. Save user message (lines 47-51)
4. Detect intent (lines 54-62)
5. Call handler (lines 65-66)
6. Save bot response (lines 69-74)
7. Build response (lines 84-96)
```

---

#### 12. `chatbot/urls.py` ⭐⭐⭐
**Why:** Maps URLs to view functions
**What to look for:**
- URL patterns (lines 13-18)
- How views are connected

**Location:** `/backend/chatbot/urls.py`

---

#### 13. `chatbot/admin.py` ⭐⭐
**Why:** Django admin configuration (visual interface)
**What to look for:**
- How models are displayed in admin
- Inline editing features

**Location:** `/backend/chatbot/admin.py`

**Optional:** Only review if you want to customize admin interface

---

### Phase 5: Testing & Documentation
**Goal:** Learn how to use and test the system

#### 14. `API_TESTING_GUIDE.md` ⭐⭐⭐⭐
**Why:** Complete API usage examples
**Location:** `/backend/API_TESTING_GUIDE.md`

#### 15. `QUICK_START.md` ⭐⭐⭐⭐
**Why:** 5 different ways to test
**Location:** `/backend/QUICK_START.md`

#### 16. `README.md` ⭐⭐⭐⭐
**Why:** Main documentation
**Location:** `/backend/README.md`

#### 17. `interactive_client.py` ⭐⭐⭐
**Why:** Python testing tool
**Location:** `/backend/interactive_client.py`

#### 18. `test_api.sh` ⭐⭐
**Why:** Bash testing script
**Location:** `/backend/test_api.sh`

---

## 🎯 Recommended Reading Order

### For Quick Understanding (30 minutes)
1. `README.md` - Overview
2. `chatbot/models.py` - Data structure
3. `chatbot/intents.py` - Intent detection
4. `chatbot/handlers.py` - Business logic (focus on CreateChangeRequestHandler)
5. `chatbot/views.py` - API endpoint

### For Deep Understanding (2 hours)
Follow the full order above from Phase 1 to Phase 5

### For Practical Learning (Best approach!)
1. Read `QUICK_START.md`
2. Run `python interactive_client.py`
3. As you use it, read the corresponding files:
   - Send "create change request" → Read `handlers.py` CreateChangeRequestHandler
   - Send "help" → Read `handlers.py` HelpHandler
   - Check response format → Read `serializers.py`

---

## 📊 File Importance Matrix

| File | Importance | Complexity | Time to Review |
|------|-----------|------------|----------------|
| `chatbot/handlers.py` | ⭐⭐⭐⭐⭐ | High | 30 min |
| `chatbot/views.py` | ⭐⭐⭐⭐⭐ | Medium | 20 min |
| `chatbot/models.py` | ⭐⭐⭐⭐⭐ | Low | 15 min |
| `config/settings.py` | ⭐⭐⭐⭐⭐ | Medium | 15 min |
| `chatbot/intents.py` | ⭐⭐⭐⭐ | Low | 10 min |
| `chatbot/serializers.py` | ⭐⭐⭐⭐ | Medium | 15 min |
| `integrations/models.py` | ⭐⭐⭐⭐ | Low | 10 min |
| `chatbot/context_manager.py` | ⭐⭐⭐ | Low | 5 min |
| `config/urls.py` | ⭐⭐⭐ | Low | 5 min |
| `chatbot/urls.py` | ⭐⭐⭐ | Low | 5 min |
| `integrations/services.py` | ⭐⭐⭐ | Medium | 10 min |
| `chatbot/admin.py` | ⭐⭐ | Low | 5 min |
| `.env.example` | ⭐⭐⭐ | Low | 5 min |

---

## 🔍 What to Focus On in Each File

### In `handlers.py` (Most Important!)
- **Lines 24-144:** `CreateChangeRequestHandler`
  - How fields are collected step-by-step
  - How `required_fields` list shrinks
  - How `next_field` is updated
  - The `_create_change_request()` method

**Key pattern to understand:**
```python
# First time: Initialize
if not context.intent:
    context.required_fields = ['field1', 'field2', 'field3']
    context.next_field = 'field1'

# Each message: Collect field
context.collected_data[current_field] = message
context.required_fields.remove(current_field)

# Check if done
if not context.required_fields:
    # All fields collected - create change request
```

### In `views.py`
- **Lines 24-98:** `ChatMessageView.post()`
  - The complete request/response cycle
  - How context is managed
  - How handlers are called
  - Error handling

### In `models.py`
- Field types (UUIDField, JSONField, ForeignKey)
- Relationships between models
- The `is_complete()` method

### In `intents.py`
- Keyword matching logic
- How to add new intents

---

## 🎓 Learning Path by Goal

### "I want to understand the data flow"
1. `chatbot/views.py` (lines 24-98)
2. `chatbot/intents.py` (lines 7-59)
3. `chatbot/handlers.py` (lines 24-144)
4. `chatbot/models.py`

### "I want to add a new feature"
1. `chatbot/intents.py` - Add new intent keywords
2. `chatbot/handlers.py` - Create new handler class
3. `chatbot/handlers.py` (line 253-261) - Register handler
4. Test with `interactive_client.py`

### "I want to modify the API"
1. `chatbot/serializers.py` - Modify request/response format
2. `chatbot/views.py` - Update endpoint logic
3. `chatbot/urls.py` - Add new endpoints if needed

### "I want to integrate ServiceNow"
1. `integrations/services.py` - Implement ServiceNowService
2. `chatbot/handlers.py` (line 108) - Update to use real API
3. `.env.example` - Document required credentials

---

## 💡 Pro Tips

1. **Use an IDE with "Go to Definition"** - Click on functions to jump to their implementation
2. **Follow the data flow** - Trace a message from view → intent → handler → database
3. **Run the code while reading** - Use `interactive_client.py` and set breakpoints
4. **Read comments** - I added detailed docstrings everywhere
5. **Check the tests** - Run `test_api.sh` to see expected behavior

---

## 🚦 Start Here

**If you have 15 minutes:**
Read `handlers.py` (just the CreateChangeRequestHandler class)

**If you have 1 hour:**
1. `README.md`
2. `chatbot/models.py`
3. `chatbot/handlers.py`
4. `chatbot/views.py`

**If you have 2 hours:**
Follow Phase 1 → Phase 4 order above

**Best approach:**
Run `python interactive_client.py` and read code as you interact!
