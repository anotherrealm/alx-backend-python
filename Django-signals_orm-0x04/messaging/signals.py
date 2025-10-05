from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Message, Notification, MessageHistory

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance._state.adding:
        try:
            old = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if old.content != instance.content:
            MessageHistory.objects.create(
                message=old,
                old_content=old.content
            )
            instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Remove any straggler notifications
    Notification.objects.filter(user=instance).delete()
    # Clean up messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    # Ensure history is gone (cascade would handle this, but just in case)
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
