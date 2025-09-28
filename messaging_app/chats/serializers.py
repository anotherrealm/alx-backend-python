from rest_framework import serializers
from .models import User, Conversation, Message
from django.core.exceptions import ValidationError as DjangoValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']
    
    def validate_email(self, value):
        """Custom email validation"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(max_length=1000, min_length=1)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sender', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_messages(self, obj):
        """Get messages for this conversation with pagination"""
        messages = obj.messages.all().order_by('-sent_at')[:50]  # Last 50 messages
        return MessageSerializer(messages, many=True).data

class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        min_length=1
    )
    
    class Meta:
        model = Conversation
        fields = ['participant_ids']
    
    def validate_participant_ids(self, value):
        """Validate that participant IDs exist"""
        if len(value) < 1:
            raise serializers.ValidationError("At least one participant is required.")
        
        # Check if all users exist
        existing_users = User.objects.filter(user_id__in=value).values_list('user_id', flat=True)
        missing_users = set(value) - set(existing_users)
        
        if missing_users:
            raise serializers.ValidationError(f"Users not found: {missing_users}")
        
        return value
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create()
        
        # Add participants
        participants = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(participants)
        
        return conversation

class MessageCreateSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField(max_length=1000, min_length=1)
    
    class Meta:
        model = Message
        fields = ['message_body']
    
    def create(self, validated_data):
        conversation = self.context['conversation']
        sender = self.context['sender']
        
        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            **validated_data
        )
        return message