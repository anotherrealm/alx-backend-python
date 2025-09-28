# chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the chat app outside working hours.
    Allowed: between 6 AM and 9 PM.
    Blocked: between 9 PM and 6 AM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow only between 6 AM (06:00) and 9 PM (21:00)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to the chat is restricted outside 6 AM - 9 PM."
            )

        return self.get_response(request)
