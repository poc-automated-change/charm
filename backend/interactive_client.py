#!/usr/bin/env python3
"""
Interactive CLI client for testing the Chatbot API
Usage: python interactive_client.py
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"


class ChatbotClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.conversation_id: Optional[str] = None
        self.session = requests.Session()

    def send_message(self, message: str) -> dict:
        """Send a message to the chatbot"""
        url = f"{self.base_url}/api/chat/message/"
        payload = {"message": message}

        if self.conversation_id:
            payload["conversation_id"] = self.conversation_id

        response = self.session.post(url, json=payload)
        response.raise_for_status()

        data = response.json()

        # Update conversation ID
        if not self.conversation_id:
            self.conversation_id = data.get("conversation_id")

        return data

    def list_conversations(self) -> list:
        """List all conversations"""
        url = f"{self.base_url}/api/chat/conversations/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def list_change_requests(self) -> list:
        """List all change requests"""
        url = f"{self.base_url}/api/change-requests/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def reset_conversation(self):
        """Start a new conversation"""
        self.conversation_id = None
        print("✓ Started new conversation")


def print_response(response: dict):
    """Pretty print bot response"""
    print(f"\n{'='*60}")
    print(f"Bot: {response['bot_message']}")
    print(f"{'='*60}")

    if response.get('intent'):
        print(f"Intent: {response['intent']}")

    if response.get('next_field'):
        print(f"Waiting for: {response['next_field']}")

    if response.get('change_request'):
        cr = response['change_request']
        print(f"\n✓ Change Request Created: {cr['number']}")

    print()


def main():
    """Interactive chat session"""
    client = ChatbotClient()

    print("""
╔════════════════════════════════════════════════════════════╗
║        IT Change Management Chatbot - Test Client         ║
╚════════════════════════════════════════════════════════════╝

Commands:
  /new         - Start a new conversation
  /list        - List all conversations
  /changes     - List all change requests
  /quit        - Exit

Examples:
  > create a change request
  > check status of CHG0000001
  > help
    """)

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input == "/quit":
                print("Goodbye!")
                break
            elif user_input == "/new":
                client.reset_conversation()
                continue
            elif user_input == "/list":
                conversations = client.list_conversations()
                print(f"\n✓ Total Conversations: {len(conversations)}")
                for conv in conversations[:5]:
                    print(f"  - {conv['id'][:8]}... [{conv['status']}] - {conv['started_at']}")
                print()
                continue
            elif user_input == "/changes":
                changes = client.list_change_requests()
                print(f"\n✓ Total Change Requests: {len(changes)}")
                for cr in changes:
                    print(f"  - {cr['number']}: {cr['short_description']} [{cr['state']}]")
                print()
                continue

            # Send message to chatbot
            response = client.send_message(user_input)
            print_response(response)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except requests.exceptions.ConnectionError:
            print("\n❌ Error: Cannot connect to server. Is it running?")
            print("   Start server with: uv run python manage.py runserver")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
