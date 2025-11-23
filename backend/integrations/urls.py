"""
URL configuration for integrations app
"""
from django.urls import path
from rest_framework import generics
from .models import ChangeRequest
from chatbot.serializers import ChangeRequestSerializer

app_name = 'integrations'


class ChangeRequestListView(generics.ListAPIView):
    """List all change requests"""
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer


class ChangeRequestDetailView(generics.RetrieveAPIView):
    """Get a specific change request"""
    queryset = ChangeRequest.objects.all()
    serializer_class = ChangeRequestSerializer
    lookup_field = 'id'


urlpatterns = [
    path('change-requests/', ChangeRequestListView.as_view(), name='change-request-list'),
    path('change-requests/<int:id>/', ChangeRequestDetailView.as_view(), name='change-request-detail'),
]
