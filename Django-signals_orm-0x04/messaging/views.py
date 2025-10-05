from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page

from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    request.user.delete()
    return redirect('home')

@login_required
@cache_page(60)  # cache this inbox view for 60 seconds
def inbox(request):
    # 1) Fetch unread via the custom manager
    unread_via_manager = Message.unread.unread_for_user(request.user)

    # 2) Fetch unread via a raw ORM filter
    unread_via_filter = Message.objects.filter(receiver=request.user, read=False) \
        .select_related('sender') \
        .only('id', 'sender', 'content', 'timestamp')

    # Use the manager result by default (both patterns are present)
    messages = unread_via_manager
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
@require_POST
def send_message(request):
    receiver = get_object_or_404(User, pk=request.POST.get('receiver_id'))
    content = request.POST.get('content', '').strip()
    Message.objects.create(sender=request.user, receiver=receiver, content=content)
    return redirect('messaging:inbox')
