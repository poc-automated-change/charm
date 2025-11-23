"""
Intent detection module - Phase 1: Rule-based keyword matching
This will be replaced with AI/NLU in Phase 2
"""


def detect_intent(message: str, current_intent: str = None) -> str:
    """
    Simple keyword-based intent detection

    Args:
        message: User's message text
        current_intent: Current intent in conversation (if any)

    Returns:
        Detected intent string
    """
    # If we're already in a conversation flow, maintain that intent
    # unless the user explicitly wants to do something else
    if current_intent and not _wants_to_change_intent(message):
        return current_intent

    message_lower = message.lower()

    # Create change request
    if any(word in message_lower for word in ['create', 'new', 'make', 'add', 'start']):
        if any(word in message_lower for word in ['change', 'ticket', 'request', 'cr']):
            return 'create_change_request'

    # Check status
    if any(word in message_lower for word in ['status', 'check', 'show', 'find', 'lookup', 'search']):
        if any(word in message_lower for word in ['change', 'ticket', 'request', 'chg']):
            return 'check_status'

    # Update change request
    if any(word in message_lower for word in ['update', 'modify', 'edit', 'change']):
        if any(word in message_lower for word in ['change', 'ticket', 'request']):
            return 'update_change_request'

    # List changes
    if any(word in message_lower for word in ['list', 'all', 'show all', 'my changes']):
        return 'list_changes'

    # Help
    if any(word in message_lower for word in ['help', 'what can you do', 'commands', 'how to']):
        return 'help'

    # Greeting
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        return 'greeting'

    # Default
    return 'unknown'


def _wants_to_change_intent(message: str) -> bool:
    """
    Check if user wants to change to a different intent

    Args:
        message: User's message text

    Returns:
        True if user wants to change intent
    """
    message_lower = message.lower()

    # Check for explicit intent change keywords
    change_keywords = [
        'cancel',
        'stop',
        'nevermind',
        'never mind',
        'forget it',
        'start over',
        'restart',
        'i want to',
        'instead',
    ]

    return any(keyword in message_lower for keyword in change_keywords)


def get_intent_description(intent: str) -> str:
    """
    Get human-readable description of intent

    Args:
        intent: Intent string

    Returns:
        Human-readable description
    """
    descriptions = {
        'create_change_request': 'Create a new change request',
        'check_status': 'Check the status of a change request',
        'update_change_request': 'Update an existing change request',
        'list_changes': 'List all change requests',
        'help': 'Get help and see available commands',
        'greeting': 'Greeting',
        'unknown': 'Unknown intent'
    }

    return descriptions.get(intent, 'Unknown')
