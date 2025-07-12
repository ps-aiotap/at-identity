"""
Artisan CRM integration with AT Identity
"""
from typing import Dict, List, Any
from django.contrib.auth import get_user_model
from .base import BaseAppIntegration

User = get_user_model()

class ArtisanCRMIntegration(BaseAppIntegration):
    app_name = "Artisan CRM"
    app_context = "artisan_crm"
    
    def get_default_roles(self) -> List[Dict[str, Any]]:
        return [
            {
                'name': 'CRM Admin',
                'slug': 'crm_admin',
                'description': 'Full CRM access and management',
                'permissions': [
                    'customer.create', 'customer.edit', 'customer.delete',
                    'lead.manage', 'campaign.create', 'campaign.manage',
                    'analytics.view', 'settings.manage'
                ]
            },
            {
                'name': 'Sales Rep',
                'slug': 'sales_rep',
                'description': 'Customer and lead management',
                'permissions': [
                    'customer.view', 'customer.edit',
                    'lead.manage', 'interaction.create',
                    'campaign.view'
                ]
            },
            {
                'name': 'Sales Manager',
                'slug': 'sales_manager',
                'description': 'Team and pipeline oversight',
                'permissions': [
                    'customer.view', 'customer.edit',
                    'lead.manage', 'campaign.view',
                    'analytics.view', 'team.manage'
                ]
            }
        ]
    
    def get_user_context(self, user: User) -> Dict[str, Any]:
        """Get CRM-specific user context"""
        context = {
            'customers_count': 0,
            'active_leads': 0,
            'is_sales_rep': False,
            'is_crm_admin': False,
            'permissions': self.get_user_permissions(user)
        }
        
        # Check if user has CRM-related data
        try:
            if hasattr(user, 'profile') and user.profile.crm_data:
                context.update(user.profile.crm_data)
        except:
            pass
        
        return context