"""
Decorators for AT Identity permission checking
"""
from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings

def at_permission_required(permission):
    """Decorator to check AT Identity permissions"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if has_at_permission(request.user, permission):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Permission denied")
        return wrapper
    return decorator

def has_at_permission(user, permission):
    """Check if user has AT Identity permission"""
    if hasattr(user, '_at_permissions'):
        return permission in user._at_permissions
    
    # Fallback API call
    identity_url = getattr(settings, 'AT_IDENTITY_URL', 'http://localhost:8001/api/')
    app_name = getattr(settings, 'APP_NAME', 'unknown')
    
    try:
        response = requests.post(f'{identity_url}verify-permission/', json={
            'app_name': app_name,
            'external_user_id': user.id,
            'permission': permission
        }, timeout=2)
        
        if response.status_code == 200:
            return response.json().get('has_permission', False)
    except requests.RequestException:
        pass
    
    return False