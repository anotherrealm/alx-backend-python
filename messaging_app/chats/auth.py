from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Extend this class if you need to add custom logic
    (e.g., logging, token validation tweaks).
    """
    pass
