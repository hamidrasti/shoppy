from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
