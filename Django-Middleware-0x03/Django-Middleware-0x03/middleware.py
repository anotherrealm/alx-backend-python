# chats/middleware.py
from django.http import HttpResponseForbidden


class RolePermissionMiddleware:
    """
    Middleware that restricts access to certain actions
    based on the user's role (admin/moderator).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce role restrictions on specific paths (example: deleting conversations/messages)
        restricted_paths = ["/conversations/delete", "/messages/delete"]

        if any(path in request.path for path in restricted_paths):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to perform this action.")

            # Example role check:
            # - `is_staff` used as moderator
            # - `is_superuser` used as admin
            if not (request.user.is_staff or request.user.is_superuser):
                return HttpResponseForbidden(
                    "You do not have the required role (admin/moderator) to perform this action."
                )

        return self.get_response(request)
