from rest_framework import serializers
from .models import Conversation, Message, ConversationContext
from integrations.models import ChangeRequest


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'timestamp', 'metadata']
        read_only_fields = ['id', 'timestamp']


class ConversationContextSerializer(serializers.ModelSerializer):
    """Serializer for ConversationContext model"""

    class Meta:
        model = ConversationContext
        fields = [
            'intent',
            'collected_data',
            'required_fields',
            'next_field',
            'change_request'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with messages and context"""
    messages = MessageSerializer(many=True, read_only=True)
    context = ConversationContextSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'status', 'started_at', 'updated_at', 'messages', 'context']
        read_only_fields = ['id', 'started_at', 'updated_at']


class ChatMessageRequestSerializer(serializers.Serializer):
    """Serializer for incoming chat message requests"""
    conversation_id = serializers.UUIDField(required=False, allow_null=True)
    message = serializers.CharField(required=True, max_length=2000)


class ChatMessageResponseSerializer(serializers.Serializer):
    """Serializer for chat message responses"""
    conversation_id = serializers.UUIDField()
    intent = serializers.CharField()
    bot_message = serializers.CharField()
    required_fields = serializers.ListField(child=serializers.CharField())
    collected_data = serializers.DictField()
    next_field = serializers.CharField(allow_null=True)
    is_complete = serializers.BooleanField()
    change_request = serializers.DictField(required=False)


class ChangeRequestSerializer(serializers.ModelSerializer):
    """Serializer for ChangeRequest model"""

    class Meta:
        model = ChangeRequest
        fields = [
            'id',
            'servicenow_sys_id',
            'number',
            'short_description',
            'description',
            'state',
            'priority',
            'jira_issue_key',
            'github_repo',
            'github_pr_number',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
