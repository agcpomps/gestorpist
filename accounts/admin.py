from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Department


CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ["email", "username", "departamento", "is_superuser"]
    fieldsets = UserAdmin.fieldsets + (
        ("Departamento", {"fields": ("departamento",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Departamento", {"fields": ("departamento",)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
