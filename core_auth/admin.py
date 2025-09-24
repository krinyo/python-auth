from django.contrib import admin
from .models import User, Role, BusinessElement, AccessRule

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email']
    list_filter = ['is_active', 'is_staff', 'is_superuser']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(AccessRule)
class AccessRuleAdmin(admin.ModelAdmin):
    list_display = ['role', 'business_element', 'read_permission', 'create_permission', 'update_permission', 'delete_permission']
    list_filter = ['role', 'business_element']