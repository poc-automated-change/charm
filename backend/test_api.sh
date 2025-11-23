#!/bin/bash
# API Testing Script for Chatbot Backend

BASE_URL="http://localhost:8000"

echo "=================================="
echo "  Chatbot API Testing Script"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Greeting
echo -e "${BLUE}Test 1: Greeting${NC}"
echo "Request: {\"message\": \"Hello\"}"
RESPONSE=$(curl -s -X POST $BASE_URL/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}')
echo -e "${GREEN}Response:${NC}"
echo $RESPONSE | python3 -m json.tool 2>/dev/null || echo $RESPONSE
echo ""
echo "---"
echo ""

# Test 2: Help
echo -e "${BLUE}Test 2: Help Command${NC}"
echo "Request: {\"message\": \"help\"}"
RESPONSE=$(curl -s -X POST $BASE_URL/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "help"}')
echo -e "${GREEN}Response:${NC}"
echo $RESPONSE | python3 -m json.tool 2>/dev/null || echo $RESPONSE
echo ""
echo "---"
echo ""

# Test 3: Create Change Request (Full Flow)
echo -e "${BLUE}Test 3: Create Change Request (Full Flow)${NC}"

echo -e "${YELLOW}Step 1: Initiate${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "create a change request"}')
CONV_ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['conversation_id'])" 2>/dev/null)
echo "Conversation ID: $CONV_ID"
echo "Bot: $(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['bot_message'])" 2>/dev/null)"
echo ""

echo -e "${YELLOW}Step 2: Short Description${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"Upgrade production database\"}")
echo "Bot: $(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['bot_message'])" 2>/dev/null)"
echo ""

echo -e "${YELLOW}Step 3: Description${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"Migrate from PostgreSQL 14 to 15\"}")
echo "Bot: $(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['bot_message'])" 2>/dev/null)"
echo ""

echo -e "${YELLOW}Step 4: Priority${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"2\"}")
echo "Bot: $(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['bot_message'])" 2>/dev/null)"
echo ""

echo -e "${YELLOW}Step 5: Start Date${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"2025-03-01\"}")
echo "Bot: $(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['bot_message'])" 2>/dev/null)"
echo ""

echo -e "${YELLOW}Step 6: End Date (Final)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"2025-03-15\"}")
echo -e "${GREEN}Final Response:${NC}"
echo $RESPONSE | python3 -m json.tool 2>/dev/null || echo $RESPONSE
CHG_NUMBER=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('change_request', {}).get('number', 'N/A'))" 2>/dev/null)
echo ""
echo -e "${GREEN}✓ Created Change Request: $CHG_NUMBER${NC}"
echo ""
echo "---"
echo ""

# Test 4: Check Status
if [ "$CHG_NUMBER" != "N/A" ]; then
  echo -e "${BLUE}Test 4: Check Status${NC}"

  echo -e "${YELLOW}Step 1: Initiate status check${NC}"
  RESPONSE=$(curl -s -X POST $BASE_URL/api/chat/message/ \
    -H "Content-Type: application/json" \
    -d '{"message": "check status"}')
  CONV_ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['conversation_id'])" 2>/dev/null)
  echo "Bot: $(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['bot_message'])" 2>/dev/null)"
  echo ""

  echo -e "${YELLOW}Step 2: Provide CHG number${NC}"
  RESPONSE=$(curl -s -X POST $BASE_URL/api/chat/message/ \
    -H "Content-Type: application/json" \
    -d "{\"conversation_id\": \"$CONV_ID\", \"message\": \"$CHG_NUMBER\"}")
  echo -e "${GREEN}Response:${NC}"
  echo $RESPONSE | python3 -m json.tool 2>/dev/null || echo $RESPONSE
  echo ""
  echo "---"
  echo ""
fi

# Test 5: List All Conversations
echo -e "${BLUE}Test 5: List All Conversations${NC}"
RESPONSE=$(curl -s $BASE_URL/api/chat/conversations/)
COUNT=$(echo $RESPONSE | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
echo -e "${GREEN}Total Conversations: $COUNT${NC}"
echo $RESPONSE | python3 -m json.tool 2>/dev/null | head -30 || echo $RESPONSE
echo ""
echo "---"
echo ""

# Test 6: List All Change Requests
echo -e "${BLUE}Test 6: List All Change Requests${NC}"
RESPONSE=$(curl -s $BASE_URL/api/change-requests/)
echo -e "${GREEN}Response:${NC}"
echo $RESPONSE | python3 -m json.tool 2>/dev/null || echo $RESPONSE
echo ""

echo "=================================="
echo "  ✓ All Tests Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "  - View Django Admin: http://localhost:8000/admin/"
echo "  - Read API_TESTING_GUIDE.md for more examples"
echo "  - Check server logs: tail -f /tmp/django.log"
