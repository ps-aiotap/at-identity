"""
StoreLoop integration with AT Identity
"""
from typing import Dict, List, Any
from django.contrib.auth import get_user_model
from .base import BaseAppIntegration

User = get_user_model()

class StoreLoopIntegration(BaseAppIntegration):
    app_name = "StoreLoop"
    app_context = "storeloop"
    
    def get_default_roles(self) -> List[Dict[str, Any]]:
        return [
            {
                'name': 'Store Owner',
                'slug': 'store_owner',
                'description': 'Full control over store operations',
                'permissions': [
                    'store.create', 'store.edit', 'store.delete',
                    'product.create', 'product.edit', 'product.delete',
                    'order.view', 'order.manage',
                    'analytics.view'
                ]
            },
            {
                'name': 'Store Manager',
                'slug': 'store_manager',
                'description': 'Manage products and orders',
                'permissions': [
                    'product.create', 'product.edit',
                    'order.view', 'order.manage'
                ]
            },
            {
                'name': 'NGO Admin',
                'slug': 'ngo_admin',
                'description': 'Oversee multiple stores',
                'permissions': [
                    'store.view_all', 'store.manage',
                    'user.manage', 'analytics.view_all'
                ]
            }
        ]
    
    def get_user_context(self, user: User) -> Dict[str, Any]:
        """Get StoreLoop-specific user context"""
        context = {
            'has_store': False,
            'stores_count': 0,
            'is_ngo_admin': False,
            'permissions': self.get_user_permissions(user)
        }
        
        # Check if user has StoreLoop-related data
        try:
            # This would integrate with actual StoreLoop models
            # For now, return basic context
            if hasattr(user, 'profile') and user.profile.storeloop_data:
                context.update(user.profile.storeloop_data)
        except:
            pass
        
        return context