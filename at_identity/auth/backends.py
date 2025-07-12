"""
Authentication backends for AT Identity integration
"""
import requests
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.conf import settings

class ATIdentityBackend(BaseBackend):
    """Authentication backend that validates against AT Identity service"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        
        # Authenticate with AT Identity service
        identity_url = getattr(settings, 'AT_IDENTITY_URL', 'http://localhost:8001/api/')
        
        try:
            response = requests.post(f'{identity_url}auth/login/', json={
                'username': username,
                'password': password,
                'app_name': getattr(settings, 'APP_NAME', 'unknown')
            })
            
            if response.status_code == 200:
                user_data = response.json()
                
                # Get or create local user
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': user_data.get('email', ''),
                        'first_name': user_data.get('first_name', ''),
                        'last_name': user_data.get('last_name', ''),
                        'is_active': True
                    }
                )
                
                # Store AT Identity user ID for future reference
                if hasattr(user, '_at_identity_id'):
                    user._at_identity_id = user_data.get('id')
                
                return user
                
        except requests.RequestException:
            pass
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None