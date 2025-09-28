from rest_framework.permissions import BasePermission
from .models import Conversation, Message
from rest_framework import permissions
class IsParticipantOfConversation(BasePermission):
    """
    Only participants in a conversation can view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Must be logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If obj is a Conversation → check participants
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If obj is a Message → check participants of its conversation
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        # Explicitly allow GET, POST, PUT, PATCH, DELETE if participant
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return True

        return False
