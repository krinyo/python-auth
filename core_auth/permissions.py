from rest_framework import permissions
from .models import AccessRule, BusinessElement

class HasAccessToBusinessElement(permissions.BasePermission):
    """
    Кастомный класс, который проверяет права доступа пользователя к определенному
    бизнес-элементу.
    """
    message = "У вас нет прав для выполнения этого действия."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        business_element_name = view.business_element_name
        
        try:
            business_element = BusinessElement.objects.get(name=business_element_name)
        except BusinessElement.DoesNotExist:
            return False
        if request.user.is_superuser:
            return True
        if not hasattr(request.user, 'role') or not request.user.role:
            return False
        try:
            access_rule = AccessRule.objects.get(role=request.user.role, business_element=business_element)
        except AccessRule.DoesNotExist:
            return False

        if request.method in permissions.SAFE_METHODS:
            return access_rule.read_permission
        
        if request.method == 'POST':
            return access_rule.create_permission
            
        if request.method in ['PUT', 'PATCH']:
            return access_rule.update_permission
            
        if request.method == 'DELETE':
            return access_rule.delete_permission
            
        return False