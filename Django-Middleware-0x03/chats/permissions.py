# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission: allow access only if the object belongs to the requesting user.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
# chats/permissions.py
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to ensure only participants of a conversation
    can access or modify its messages.
    """

    def has_permission(self, request, view):
        # Require authentication globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be either a Conversation or a Message instance.
        We assume:
          - Conversation model has a ManyToMany field `participants`
          - Message model has a FK `conversation` → Conversation
        """
        if hasattr(obj, "participants"):  # Conversation object
            return request.user in obj.participants.all()
        elif hasattr(obj, "conversation"):  # Message object
            return request.user in obj.conversation.participants.all()
        return False
