from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User, ActivationToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "full_name",
        "role",
        "is_blocked",
        "date_joined",
        "last_login",
    )
    search_fields = (
        "username",
        "full_name",
        "email",
        "phone_number",
    )
    readonly_fields = ("date_joined", "last_login")
    ordering = ("username",)

    list_filter = (
        "is_blocked",
        "role",
    )

    fieldsets = (
        ("Основная информация", {
            "fields": (
                "username",
                "password",
                "role",
            )
        }),
        ("Контактные данные", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "country",
            )
        }),
        ("Статус", {
            "fields": (
                "is_active",
                "is_blocked",
            )
        }),
        ("Права доступа", {
            "classes": ("collapse",),
            "fields": (
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Системная информация", {
            "classes": ("collapse",),
            "fields": (
                "last_login",
                "date_joined",
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role"),
        }),
    )


@admin.register(ActivationToken)
class ActivationTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at", "expires_at")
    search_fields = ("user", "token")
    list_filter = ("created_at", "expires_at")
