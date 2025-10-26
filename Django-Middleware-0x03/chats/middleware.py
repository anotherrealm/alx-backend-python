from collections import defaultdict, deque
import logging
from pathlib import Path
from datetime import datetime

class RequestLoggingMiddleware:
    """
    logs each request to a file including timestamp, user and path
    Implements __init__ and __call__
    """

    def __init__(self, get_response):
        #middleware initialization
        self.get_response = get_response

        project_root = Path(__file__).resolve().parent.parent
        self.log_path = project_root / "requests.log"

        #logger
        logging.basicConfig(
            filename=str(self.log_path),
            level=logging.INFO,
            format="%(message)s"
        )
        self.logger = logging.getLogger("request_logger")

    def __call__(self, request):
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else "Anonymous"

        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware restricts access during certain hours
    Denies access (403) if the current time is not between 6PM and 9PM
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #current server time
        current_hour = datetime.now().hour

        #allowed range
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to this app is restricted at this time")

        return self.get_response(request)
    
class OffensiveLanguageMiddleware:
    """
    Limits number of POST requests
    per IP address
    """

    def __init__(self, get_response):
        self.get_response = get_response
        #track requests
        self.request_log = defaultdict(deque)
        self.limit = 5              
        self.time_window = 60       

    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path:
            #client IP
            ip = self.get_client_ip(request)
            now = datetime.now()

    
            while self.request_log[ip] and (now - self.request_log[ip][0]).seconds > self.time_window:
                self.request_log[ip].popleft()

            #user exceeded limi
            if len(self.request_log[ip]) >= self.limit:
                return HttpResponseForbidden(
                    "Rate limit exceeded: You can only send 5 messages per minute."
                )

            #log request
            self.request_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Helper to get client IP address from request headers"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    
class RolepermissionMiddleware:
    """
    Checks if a user has the role of admin or moderator
    before allowing access to certain actions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        #enforce if user is authenticated
        if user and user.is_authenticated:
            if not (user.is_staff or user.is_superuser):
                return HttpResponseForbidden(
                    "You do not have permission to perform this action."
                )

        return self.get_response(request)