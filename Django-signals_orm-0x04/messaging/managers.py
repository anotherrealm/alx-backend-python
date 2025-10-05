from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to return only unread messages for a given user,
    optimized to select related sender and pull only the needed fields.
    """
    def unread_for_user(self, user):
        return (
            self.get_queryset()
                .filter(receiver=user, read=False)
                .select_related('sender')
                .only('id', 'sender', 'content', 'timestamp')
        )
