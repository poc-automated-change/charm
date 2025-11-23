from django.contrib import admin
from .models import Conversation, Message, ConversationContext


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['timestamp']


class ConversationContextInline(admin.StackedInline):
    model = ConversationContext
    extra = 0


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'started_at', 'updated_at']
    list_filter = ['status', 'started_at']
    search_fields = ['id']
    readonly_fields = ['id', 'started_at', 'updated_at']
    inlines = [ConversationContextInline, MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'text_preview', 'timestamp']
    list_filter = ['sender', 'timestamp']
    search_fields = ['text', 'conversation__id']
    readonly_fields = ['timestamp']

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'


@admin.register(ConversationContext)
class ConversationContextAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'intent', 'next_field', 'is_complete']
    list_filter = ['intent']
    search_fields = ['conversation__id', 'intent']
