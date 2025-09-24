from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, 
    UserLoginView, 
    UserProfileView, 
    UserSoftDeleteView, 
    TestResourceView,
    RoleViewSet,
    BusinessElementViewSet,
    AccessRuleViewSet
)

# Создаем роутер и регистрируем ViewSet-ы
router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'business-elements', BusinessElementViewSet, basename='business-element')
router.register(r'access-rules', AccessRuleViewSet, basename='access-rule')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('delete/', UserSoftDeleteView.as_view(), name='delete'),
    path('test-resource/', TestResourceView.as_view(), name='test-resource'),

    path('admin/', include(router.urls)),
]