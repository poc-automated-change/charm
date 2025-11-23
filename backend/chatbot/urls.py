"""
URL configuration for chatbot app
"""
from django.urls import path
from .views import (
    ChatMessageView,
    ConversationListView,
    ConversationDetailView,
    ConversationDeleteView
)

app_name = 'chatbot'

urlpatterns = [
    # Chat endpoint
    path('message/', ChatMessageView.as_view(), name='chat-message'),

    # Conversation management
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<uuid:id>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<uuid:id>/delete/', ConversationDeleteView.as_view(), name='conversation-delete'),
]
