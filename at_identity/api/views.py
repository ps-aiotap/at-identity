from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from ..models import Organization, Role, UserOrganization, ExternalUser
from ..utils.permissions import PermissionManager
from ..api.sync import UserSyncService
from .serializers import UserSerializer, OrganizationSerializer

User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

@api_view(['POST'])
def sync_user(request):
    """Sync user from external application"""
    app_name = request.data.get('app_name')
    user_data = request.data.get('user_data')
    
    if not app_name or not user_data:
        return Response({'error': 'Missing app_name or user_data'}, status=400)
    
    try:
        user = UserSyncService.sync_user_from_external(app_name, user_data)
        return Response({'id': user.id, 'synced': True})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def get_permissions(request):
    """Get permissions for external user"""
    app_name = request.query_params.get('app_name')
    external_user_id = request.query_params.get('external_user_id')
    
    if not app_name or not external_user_id:
        return Response({'error': 'Missing parameters'}, status=400)
    
    try:
        external_user = ExternalUser.objects.get(
            app_name=app_name,
            external_id=external_user_id
        )
        permissions = PermissionManager.get_user_permissions(
            external_user.user, app_context=app_name
        )
        return Response({'permissions': permissions})
    except ExternalUser.DoesNotExist:
        return Response({'permissions': []})

@api_view(['POST'])
def verify_permission(request):
    """Verify if external user has permission"""
    app_name = request.data.get('app_name')
    external_user_id = request.data.get('external_user_id')
    permission = request.data.get('permission')
    
    if not all([app_name, external_user_id, permission]):
        return Response({'error': 'Missing parameters'}, status=400)
    
    try:
        external_user = ExternalUser.objects.get(
            app_name=app_name,
            external_id=external_user_id
        )
        has_permission = PermissionManager.user_has_permission(
            external_user.user, permission, app_context=app_name
        )
        return Response({'has_permission': has_permission})
    except ExternalUser.DoesNotExist:
        return Response({'has_permission': False})