from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'organizations', views.OrganizationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sync/user/', views.sync_user, name='sync_user'),
    path('permissions/', views.get_permissions, name='get_permissions'),
    path('verify-permission/', views.verify_permission, name='verify_permission'),
]