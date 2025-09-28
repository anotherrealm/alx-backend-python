from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'phone_number', 'role', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # nested user info

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)   # nested participants
    messages = MessageSerializer(many=True, read_only=True)    # nested messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
