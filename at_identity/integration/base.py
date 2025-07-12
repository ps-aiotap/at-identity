"""
Base integration layer for AT Identity with external applications
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from django.contrib.auth import get_user_model
from ..models import Organization, Role, UserOrganization

User = get_user_model()

class BaseAppIntegration(ABC):
    """Base class for app integrations with AT Identity"""
    
    app_name: str = None
    app_context: str = None
    
    @abstractmethod
    def get_default_roles(self) -> List[Dict[str, Any]]:
        """Return default roles for this app"""
        pass
    
    @abstractmethod
    def get_user_context(self, user: User) -> Dict[str, Any]:
        """Get app-specific user context"""
        pass
    
    def setup_roles(self):
        """Setup default roles for this app"""
        roles_data = self.get_default_roles()
        created_roles = []
        
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                slug=role_data['slug'],
                app_context=self.app_context,
                defaults=role_data
            )
            if created:
                created_roles.append(role)
        
        return created_roles
    
    def assign_user_role(self, user: User, organization: Organization, role_slug: str) -> UserOrganization:
        """Assign role to user in organization"""
        role = Role.objects.get(slug=role_slug, app_context=self.app_context)
        membership, created = UserOrganization.objects.get_or_create(
            user=user,
            organization=organization,
            defaults={'role': role}
        )
        if not created:
            membership.role = role
            membership.save()
        return membership
    
    def get_user_permissions(self, user: User, organization: Optional[Organization] = None) -> List[str]:
        """Get user permissions for this app"""
        from ..utils.permissions import PermissionManager
        return PermissionManager.get_user_permissions(
            user, organization, self.app_context
        )

class IdentityService:
    """Central service for identity operations across apps"""
    
    _integrations: Dict[str, BaseAppIntegration] = {}
    
    @classmethod
    def register_app(cls, integration: BaseAppIntegration):
        """Register an app integration"""
        cls._integrations[integration.app_context] = integration
    
    @classmethod
    def get_app_integration(cls, app_context: str) -> Optional[BaseAppIntegration]:
        """Get app integration by context"""
        return cls._integrations.get(app_context)
    
    @classmethod
    def setup_all_roles(cls):
        """Setup roles for all registered apps"""
        for integration in cls._integrations.values():
            integration.setup_roles()
    
    @classmethod
    def get_user_app_context(cls, user: User) -> Dict[str, Dict[str, Any]]:
        """Get user context for all apps"""
        context = {}
        for app_context, integration in cls._integrations.items():
            context[app_context] = integration.get_user_context(user)
        return context