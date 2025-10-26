# messaging_app/chats/urls.py

from django.urls import path, include
from messaging_app.chats import admin
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  
from .views import ConversationViewSet, MessageViewSet

# Create the Default Router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create the Nested Router for messages under a conversation
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    # path('', include(router.urls)), 
    # path('', include(conversation_router.urls)), 
    path('admin/', admin.site.urls),
    path('api/', include('messaging_app.chats.urls')),  
    path('api-auth/', include('rest_framework.urls')),
    path('chats/', include('messaging_app.chats.urls')),  
 
]

