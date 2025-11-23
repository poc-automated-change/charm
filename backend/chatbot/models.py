import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):
    """Tracks chat sessions"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="User for future authentication"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'

    def __str__(self):
        return f"Conversation {self.id} - {self.status}"


class Message(models.Model):
    """Individual chat messages"""
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]

    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        on_delete=models.CASCADE
    )
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(null=True, blank=True, help_text="For rich content")

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f"{self.sender}: {self.text[:50]}"


class ConversationContext(models.Model):
    """Tracks conversation state and collected data"""
    conversation = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        related_name='context'
    )
    intent = models.CharField(max_length=50, null=True, blank=True)
    collected_data = models.JSONField(default=dict, help_text="Fields collected so far")
    required_fields = models.JSONField(default=list, help_text="Fields still needed")
    next_field = models.CharField(max_length=50, null=True, blank=True)
    change_request = models.ForeignKey(
        'integrations.ChangeRequest',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = 'Conversation Context'
        verbose_name_plural = 'Conversation Contexts'

    def __str__(self):
        return f"Context for {self.conversation.id} - Intent: {self.intent}"

    def is_complete(self):
        """Check if all required fields have been collected"""
        return len(self.required_fields) == 0
