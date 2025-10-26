# messaging_app/chats/views.py
from messaging_app.chats.filters import MessageFilter
from messaging_app.chats.pagination import MessagePagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwner, IsParticipantOfConversation  

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['participants__username']
    permission_classes = [IsAuthenticated, IsOwner]
    permission_classes = [IsParticipantOfConversation]  

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        participants = request.data.get('participants')
        if not participants or len(participants) < 2:
            return Response({"error": "A conversation must have at least two participants."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        for user_id in participants:
            try:
                user = User.objects.get(id=user_id)
                conversation.participants.add(user)
            except User.DoesNotExist:
                return Response({"error": f"User with id {user_id} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)

        conversation.save()
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body', 'sender__username']
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination 

    def get_queryset(self):
        """
        Limit messages so user only sees those in conversations they participate in.
        """
        conversation_id = self.kwargs.get("conversation_id")  
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.none()

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        try:
            conversation = Conversation.objects.get(id=pk)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        #is user a participant
        if request.user not in conversation.participants.all():
            return Response({"error": "You are not allowed to send messages to this conversation."},
                            status=status.HTTP_403_FORBIDDEN)  

        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        if not sender_id or not message_body:
            return Response({"error": "Both sender ID and message body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = User.objects.get(id=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender not found."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(sender=sender, message_body=message_body, conversation=conversation)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)