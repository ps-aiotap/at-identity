"""
API client for external applications to integrate with AT Identity
"""
import requests
from typing import Dict, List, Optional, Any
from django.conf import settings

class IdentityAPIClient:
    """Client for external apps to interact with AT Identity"""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or getattr(settings, 'AT_IDENTITY_API_URL', 'http://localhost:8000/api/identity/')
        self.api_key = api_key or getattr(settings, 'AT_IDENTITY_API_KEY', '')
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            response = self.session.get(f'{self.base_url}users/{user_id}/')
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None
    
    def get_user_permissions(self, user_id: int, app_context: str = 'shared') -> List[str]:
        """Get user permissions for specific app context"""
        try:
            response = self.session.get(
                f'{self.base_url}users/{user_id}/permissions/',
                params={'app_context': app_context}
            )
            response.raise_for_status()
            return response.json().get('permissions', [])
        except requests.RequestException:
            return []
    
    def get_user_organizations(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's organizations"""
        try:
            response = self.session.get(f'{self.base_url}users/{user_id}/organizations/')
            response.raise_for_status()
            return response.json().get('organizations', [])
        except requests.RequestException:
            return []
    
    def verify_permission(self, user_id: int, permission: str, app_context: str = 'shared') -> bool:
        """Verify if user has specific permission"""
        try:
            response = self.session.post(
                f'{self.base_url}users/{user_id}/verify-permission/',
                json={
                    'permission': permission,
                    'app_context': app_context
                }
            )
            response.raise_for_status()
            return response.json().get('has_permission', False)
        except requests.RequestException:
            return False
    
    def create_organization(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new organization"""
        try:
            response = self.session.post(f'{self.base_url}organizations/', json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None
    
    def add_user_to_organization(self, user_id: int, org_id: int, role_slug: str, app_context: str) -> bool:
        """Add user to organization with role"""
        try:
            response = self.session.post(
                f'{self.base_url}organizations/{org_id}/members/',
                json={
                    'user_id': user_id,
                    'role_slug': role_slug,
                    'app_context': app_context
                }
            )
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False

# Singleton instance for easy access
identity_client = IdentityAPIClient()