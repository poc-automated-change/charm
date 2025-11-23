from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, ConversationContext
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    ChatMessageRequestSerializer,
    ChatMessageResponseSerializer
)
from .intents import detect_intent
from .handlers import get_handler
from .context_manager import ConversationManager


class ChatMessageView(APIView):
    """
    Handle chat messages - main endpoint for the chatbot
    POST /api/chat/message/
    """

    def post(self, request):
        """Process a user message and return bot response"""

        # Validate request
        request_serializer = ChatMessageRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(
                request_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation_id = request_serializer.validated_data.get('conversation_id')
        user_message = request_serializer.validated_data.get('message')

        # Get or create conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
        else:
            conversation = Conversation.objects.create(status='active')

        # Get or create context
        context = ConversationManager.get_or_create_context(conversation)

        # Save user message
        Message.objects.create(
            conversation=conversation,
            sender='user',
            text=user_message
        )

        # Detect intent if not already set or if user wants to change
        current_intent = context.intent
        detected_intent = detect_intent(user_message, current_intent)

        # If intent changed, reset context
        if detected_intent != current_intent and current_intent is not None:
            ConversationManager.reset_context(context)
            context.intent = detected_intent
            context.save()

        # Route to appropriate handler
        handler = get_handler(detected_intent or 'unknown')
        result = handler.handle(context, user_message)

        # Save bot response
        bot_message_obj = Message.objects.create(
            conversation=conversation,
            sender='bot',
            text=result['bot_message'],
            metadata=result.get('change_request')
        )

        # Mark conversation as completed if done
        if result.get('is_complete'):
            conversation.status = 'completed'
            conversation.save()

        # Refresh context from database
        context.refresh_from_db()

        # Build response
        response_data = {
            'conversation_id': str(conversation.id),
            'intent': context.intent or 'unknown',
            'bot_message': result['bot_message'],
            'required_fields': context.required_fields,
            'collected_data': context.collected_data,
            'next_field': context.next_field,
            'is_complete': result.get('is_complete', False)
        }

        if 'change_request' in result:
            response_data['change_request'] = result['change_request']

        return Response(response_data, status=status.HTTP_200_OK)


class ConversationListView(generics.ListAPIView):
    """
    List all conversations
    GET /api/chat/conversations/
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class ConversationDetailView(generics.RetrieveAPIView):
    """
    Get a specific conversation with all messages
    GET /api/chat/conversations/{id}/
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    lookup_field = 'id'


class ConversationDeleteView(generics.DestroyAPIView):
    """
    Delete a conversation
    DELETE /api/chat/conversations/{id}/
    """
    queryset = Conversation.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Conversation deleted successfully'},
            status=status.HTTP_200_OK
        )
