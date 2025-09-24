from rest_framework import permissions
from .models import AccessRule, BusinessElement

class HasAccessToBusinessElement(permissions.BasePermission):
    """
    Кастомный класс, который проверяет права доступа пользователя к определенному
    бизнес-элементу.
    """
    message = "У вас нет прав для выполнения этого действия."

    def has_permission(self, request, view):
        # Если пользователь не аутентифицирован, доступ запрещен
        if not request.user.is_authenticated:
            return False
            
        # Определяем, к какому бизнес-элементу идет запрос
        # В этом примере мы получаем имя элемента из URL, например 'test_resource'
        business_element_name = view.business_element_name
        
        try:
            business_element = BusinessElement.objects.get(name=business_element_name)
        except BusinessElement.DoesNotExist:
            # Если такого элемента не существует, доступ запрещен
            return False

        # Проверяем, является ли пользователь суперпользователем
        if request.user.is_superuser:
            return True
            
        # Находим роль пользователя
        # Здесь мы предполагаем, что у пользователя есть поле 'role',
        # которое ссылается на модель Role. Если у вас другая логика,
        # например, many-to-many, ее нужно адаптировать.
        if not hasattr(request.user, 'role') or not request.user.role:
            return False

        # Ищем правило доступа для роли пользователя и бизнес-элемента
        try:
            access_rule = AccessRule.objects.get(role=request.user.role, business_element=business_element)
        except AccessRule.DoesNotExist:
            return False

        # Проверяем права в зависимости от метода запроса
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return access_rule.read_permission
        
        if request.method == 'POST':
            return access_rule.create_permission
            
        if request.method in ['PUT', 'PATCH']:
            return access_rule.update_permission
            
        if request.method == 'DELETE':
            return access_rule.delete_permission
            
        return False