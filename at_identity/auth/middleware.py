"""
Userless middleware for AT Identity integration
"""
import requests
from django.conf import settings
from .user_proxy import ATIdentityUser

class ATIdentityMiddleware:
    """Middleware to handle userless authentication"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.identity_url = getattr(settings, 'AT_IDENTITY_URL', 'http://localhost:8001/api/')
        self.app_name = getattr(settings, 'APP_NAME', 'unknown')
    
    def __call__(self, request):
        # Set user from session
        user_id = request.session.get('at_identity_user_id')
        if user_id:
            try:
                response = requests.get(f'{self.identity_url}users/{user_id}/', timeout=2)
                if response.status_code == 200:
                    user_data = response.json()
                    request.user = ATIdentityUser(user_data)
                else:
                    request.user = AnonymousATUser()
            except:
                request.user = AnonymousATUser()
        else:
            request.user = AnonymousATUser()
        
        response = self.get_response(request)
        return response

class AnonymousATUser:
    """Anonymous user for userless system"""
    is_authenticated = False
    is_anonymous = True
    id = None
    username = ''