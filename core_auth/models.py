from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Создаем наш кастомный UserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

# Модель пользователя
class User(AbstractUser):
    """
    Кастомная модель пользователя, которая расширяет AbstractUser.
    Используем email как уникальный идентификатор для аутентификации.
    """
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True) # Поле для "мягкого" удаления
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = CustomUserManager()
    def __str__(self):
        return self.email

# Модель для ролей
class Role(models.Model):
    """
    Модель для описания ролей пользователей в проекте.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

# Модель для бизнес-элементов
class BusinessElement(models.Model):
    """
    Модель для описания объектов приложения (ресурсов).
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.name

# Модель для правил доступа
class AccessRule(models.Model):
    """
    Модель, связывающая роли с бизнес-элементами и определяющая права доступа.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    business_element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)
    
    # Права доступа
    read_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)
    
    class Meta:
        # Уникальная связка роли и элемента
        unique_together = ('role', 'business_element')
        
    def __str__(self):
        return f"{self.role.name} - {self.business_element.name}"