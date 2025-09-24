from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserSoftDeleteView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('delete/', UserSoftDeleteView.as_view(), name='delete')
]