"""
Context manager for handling conversation state
"""
from typing import Optional
from .models import Conversation, ConversationContext


class ConversationManager:
    """Manages conversation context and state"""

    @staticmethod
    def get_or_create_context(conversation: Conversation) -> ConversationContext:
        """
        Get or create a conversation context

        Args:
            conversation: Conversation instance

        Returns:
            ConversationContext instance
        """
        context, created = ConversationContext.objects.get_or_create(
            conversation=conversation,
            defaults={
                'collected_data': {},
                'required_fields': []
            }
        )
        return context

    @staticmethod
    def reset_context(context: ConversationContext) -> None:
        """
        Reset conversation context for a new intent

        Args:
            context: ConversationContext to reset
        """
        context.intent = None
        context.collected_data = {}
        context.required_fields = []
        context.next_field = None
        context.change_request = None
        context.save()

    @staticmethod
    def is_context_active(context: ConversationContext) -> bool:
        """
        Check if context has an active intent flow

        Args:
            context: ConversationContext to check

        Returns:
            True if context has an active intent
        """
        return context.intent is not None and len(context.required_fields) > 0
