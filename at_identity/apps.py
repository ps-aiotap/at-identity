from django.apps import AppConfig

class AtIdentityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'at_identity'
    verbose_name = 'AT Identity'
    
    def ready(self):
        import at_identity.signals
        
        # Register app integrations
        from .integration.base import IdentityService
        from .integration.storeloop import StoreLoopIntegration
        from .integration.artisan_crm import ArtisanCRMIntegration
        
        IdentityService.register_app(StoreLoopIntegration())
        IdentityService.register_app(ArtisanCRMIntegration())