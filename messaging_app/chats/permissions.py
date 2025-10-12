from rest_framework.permissions import BasePermission

from rest_framework.permissions import BasePermission

from rest_framework import permissions

class IsOwner(BasePermission):
    """
    Access  for only the owner of the message
    or participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'sender'): 
            return obj.sender == request.user
        elif hasattr(obj, 'participants'):  
            return request.user in obj.participants.all()
        return False
    
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - only authenticated users
    - only participants in a conversation to send, view, update, and delete messages
    """

    def has_permission(self, request, view):
        #ensure user authentication
        return request.user and request.user.is_authenticated   

    def has_object_permission(self, request, view, obj):
        #can be a message or covo
        if hasattr(obj, 'participants'):
            # if converastion 
            if request.user in obj.participants.all():
                return True
        elif hasattr(obj, 'conversation'):
            #if message
            if request.user in obj.conversation.participants.all():
                #allow crud methods
                if request.method in permissions.SAFE_METHODS:
                    return True
                if request.method in ["PUT", "PATCH", "DELETE"]: 
                    return True
        return False
