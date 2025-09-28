from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Conversation, Message
import uuid

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.role, 'guest')

class ConversationModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            first_name='User1',
            last_name='Test',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            first_name='User2',
            last_name='Test',
            password='testpass123'
        )
    
    def test_create_conversation(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        
        self.assertEqual(conversation.participants.count(), 2)
        self.assertIn(self.user1, conversation.participants.all())
        self.assertIn(self.user2, conversation.participants.all())

class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            first_name='User1',
            last_name='Test',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            first_name='User2',
            last_name='Test',
            password='testpass123'
        )
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)
    
    def test_create_message(self):
        message = Message.objects.create(
            sender=self.user1,
            conversation=self.conversation,
            message_body='Hello, world!'
        )
        
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.message_body, 'Hello, world!')

class APITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            first_name='User1',
            last_name='Test',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            first_name='User2',
            last_name='Test',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user1)
    
    def test_create_conversation(self):
        url = '/api/conversations/'
        data = {
            'participant_ids': [str(self.user2.user_id)]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['participants'][1]['email'], 'user2@example.com')