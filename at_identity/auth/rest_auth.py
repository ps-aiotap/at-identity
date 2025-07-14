"""
Custom REST Framework authentication for AT Identity
"""
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser
from .user_proxy import ATIdentityUser

class ATIdentityAuthentication(BaseAuthentication):
    """
    Custom authentication for AT Identity that works with REST Framework
    """
    
    def authenticate(self, request):
        # Get user from our middleware
        user = getattr(request, 'user', None)
        
        # If it's our ATIdentityUser, return it
        if isinstance(user, ATIdentityUser):
            return (user, None)
        
        # Otherwise return None to let other authenticators handle it
        return None