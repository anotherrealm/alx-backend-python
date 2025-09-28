import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

# Configure logging
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """Middleware that logs every request with timestamp, user, and path."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """Middleware that restricts chat access outside 6AM–9PM."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().hour
        if now < 6 or now > 21:  # Before 6AM or after 9PM
            return HttpResponseForbidden("Access to chat is restricted at this time.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Middleware that rate-limits messages per IP address.
    Max 5 messages per minute per IP.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}

    def __call__(self, request):
        if request.method == "POST" and "messages" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize for new IP
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Remove timestamps older than 1 minute
            self.message_log[ip] = [
                ts for ts in self.message_log[ip] if now - ts < timedelta(minutes=1)
            ]

            # Check limit
            if len(self.message_log[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Try again later.")

            # Log new request
            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class RolepermissionMiddleware:
    """
    Middleware to enforce role-based access.
    Only users with role 'admin' or 'moderator' can perform restricted actions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: restrict DELETE requests unless user is admin/moderator
        if request.method in ["DELETE", "PUT", "PATCH"]:
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")

            user_role = getattr(request.user, "role", None)
            if user_role not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to perform this action.")

        return self.get_response(request)
