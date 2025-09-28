# messaging_app/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from chats.views import ConversationViewSet, MessageViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')


def api_root(request):
    """Simple API root view"""
    content = """
    <h1>Messaging App API</h1>
    <p>Welcome to the Messaging App API. Available endpoints:</p>
    <ul>
        <li><a href="/api/conversations/">Conversations</a></li>
        <li><a href="/api/messages/">Messages</a></li>
        <li><a href="/admin/">Admin Interface</a></li>
        <li><a href="/api-auth/login/">API Authentication</a></li>
    </ul>
    """
    return HttpResponse(content)


urlpatterns = [
    path('', api_root, name='root'),                        # Welcome page
    path('admin/', admin.site.urls),                        # Django admin
    path('api/', include(router.urls)),                     # API endpoints
    path('api-auth/', include('rest_framework.urls')),      # DRF login/logout
]