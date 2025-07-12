"""
Completely userless authentication backend
"""
import requests
from django.contrib.auth.backends import BaseBackend
from django.conf import settings
from .user_proxy import ATIdentityUser

class UserlessATIdentityBackend(BaseBackend):
    """Authentication backend with no local user storage"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        
        identity_url = getattr(settings, 'AT_IDENTITY_URL', 'http://localhost:8001/api/')
        app_name = getattr(settings, 'APP_NAME', 'unknown')
        
        try:
            response = requests.post(f'{identity_url}auth/login/', json={
                'username': username,
                'password': password,
                'app_name': app_name
            })
            
            if response.status_code == 200:
                user_data = response.json()
                return ATIdentityUser(user_data)
                
        except requests.RequestException:
            pass
        
        return None
    
    def get_user(self, user_id):
        """Get user by ID from AT Identity service"""
        identity_url = getattr(settings, 'AT_IDENTITY_URL', 'http://localhost:8001/api/')
        
        try:
            response = requests.get(f'{identity_url}users/{user_id}/')
            if response.status_code == 200:
                user_data = response.json()
                return ATIdentityUser(user_data)
        except requests.RequestException:
            pass
        
        return None