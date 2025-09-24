from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserSoftDeleteView, TestResourceView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('delete/', UserSoftDeleteView.as_view(), name='delete'),
    path('test-resource/', TestResourceView.as_view(), name='test-resource'),
]