"""
User synchronization between AT Identity and external applications
"""
from typing import Dict, Optional
from django.contrib.auth import get_user_model
from ..models import ExternalUser, Organization, UserOrganization, Role

User = get_user_model()

class UserSyncService:
    """Synchronize users between AT Identity and external apps"""
    
    @staticmethod
    def sync_user_from_external(app_name: str, external_user_data: Dict) -> User:
        """Create/update AT Identity user from external app data"""
        external_id = external_user_data['id']
        
        # Check if external user mapping exists
        try:
            external_user = ExternalUser.objects.get(
                app_name=app_name,
                external_id=external_id
            )
            user = external_user.user
        except ExternalUser.DoesNotExist:
            # Create new AT Identity user
            user = User.objects.create(
                username=external_user_data['username'],
                email=external_user_data['email'],
                first_name=external_user_data.get('first_name', ''),
                last_name=external_user_data.get('last_name', '')
            )
            
            # Create external user mapping
            ExternalUser.objects.create(
                user=user,
                app_name=app_name,
                external_id=external_id,
                external_data=external_user_data
            )
        
        # Update user data
        user.email = external_user_data['email']
        user.first_name = external_user_data.get('first_name', '')
        user.last_name = external_user_data.get('last_name', '')
        user.save()
        
        return user
    
    @staticmethod
    def get_external_user_id(user: User, app_name: str) -> Optional[int]:
        """Get external app user ID for AT Identity user"""
        try:
            external_user = ExternalUser.objects.get(
                user=user,
                app_name=app_name
            )
            return external_user.external_id
        except ExternalUser.DoesNotExist:
            return None
    
    @staticmethod
    def sync_user_to_external(user: User, app_name: str) -> Dict:
        """Prepare user data for external app"""
        return {
            'at_identity_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': getattr(user, 'phone', ''),
            'language': getattr(user, 'language', 'en')
        }