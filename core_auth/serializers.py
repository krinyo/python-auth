from rest_framework import serializers
from .models import User, Role, BusinessElement, AccessRule

# Новый сериализатор для профиля
class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра и обновления профиля пользователя.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active')
        read_only_fields = ('id', 'email') # Пользователь не может изменить ID или email

# ... остальные сериализаторы, которые у вас уже есть ...

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        """Создание и сохранение пользователя с хешированным паролем."""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = '__all__'

class AccessRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRule
        fields = '__all__'