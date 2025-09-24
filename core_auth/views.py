from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import HasAccessToBusinessElement

class UserRegistrationView(APIView):
    """Представление для регистрации пользователя."""
    permission_classes = [AllowAny]

    serializer_class = UserRegistrationSerializer
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Можно сразу же залогинить пользователя после регистрации
            refresh = RefreshToken.for_user(user)
            return Response({
                'user_id': user.pk,
                'email': user.email,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """Представление для входа пользователя."""
    permission_classes = [AllowAny]

    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Если пользователь аутентифицирован, выдаем токены
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Новые представления для профиля
class UserProfileView(APIView):
    """
    Представление для просмотра и обновления профиля текущего пользователя.
    """
    permission_classes = [IsAuthenticated] # Доступ только для аутентифицированных пользователей

    serializer_class = UserProfileSerializer
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSoftDeleteView(APIView):
    """
    Представление для "мягкого" удаления аккаунта.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False # Отключаем пользователя
        user.save()
        return Response({"detail": "Account deactivated successfully."}, status=status.HTTP_204_NO_CONTENT)


class TestResourceView(APIView):
    """
    Тестовое представление, защищенное кастомными правами доступа.
    """
    permission_classes = [HasAccessToBusinessElement]
    # Указываем имя бизнес-элемента, к которому относится это представление
    business_element_name = 'test_resource'

    def get(self, request):
        return Response({"message": "Доступ к тестовому ресурсу разрешен!"}, status=status.HTTP_200_OK)