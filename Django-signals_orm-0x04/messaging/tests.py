from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Message, Notification

User = get_user_model()

class MessageSignalTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass')
        self.bob = User.objects.create_user(username='bob', password='pass')

    def test_notification_created_on_new_message(self):
        # Initially no notifications
        self.assertEqual(Notification.objects.count(), 0)

        # Alice sends Bob a message
        msg = Message.objects.create(
            sender=self.alice,
            receiver=self.bob,
            content="Hello Bob!"
        )

        # One notification should exist for Bob
        notifications = Notification.objects.filter(user=self.bob, message=msg)
        self.assertEqual(notifications.count(), 1)
        notification = notifications.first()
        self.assertFalse(notification.is_read)

    def test_no_notification_on_message_update(self):
        msg = Message.objects.create(
            sender=self.alice,
            receiver=self.bob,
            content="First"
        )
        # Clear any notifications
        Notification.objects.all().delete()

        # Update the message content
        msg.content = "Updated"
        msg.save()

        # No new notification should be created on update
        self.assertEqual(Notification.objects.count(), 0)
