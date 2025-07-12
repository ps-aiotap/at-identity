"""
Authentication views for AT Identity service
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..api.sync import UserSyncService

@api_view(['POST'])
def login(request):
    """Login endpoint for external apps"""
    username = request.data.get('username')
    password = request.data.get('password')
    app_name = request.data.get('app_name')
    
    if not all([username, password, app_name]):
        return Response({'error': 'Missing credentials'}, status=400)
    
    # Authenticate against AT Identity
    user = authenticate(username=username, password=password)
    
    if user:
        # Sync user data for external app
        user_data = UserSyncService.sync_user_to_external(user, app_name)
        return Response(user_data)
    
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
def register(request):
    """Register endpoint for external apps"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    app_name = request.data.get('app_name')
    
    if not all([username, email, password, app_name]):
        return Response({'error': 'Missing required fields'}, status=400)
    
    try:
        # Create AT Identity user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=request.data.get('first_name', ''),
            last_name=request.data.get('last_name', '')
        )
        
        # Sync to external app
        user_data = UserSyncService.sync_user_to_external(user, app_name)
        return Response(user_data, status=201)
        
    except Exception as e:
        return Response({'error': str(e)}, status=400)