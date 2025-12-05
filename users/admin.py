from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "full_name",
        "role",
        "is_blocked",
    )
    search_fields = (
        "username",
        "full_name",
        "email",
        "phone_number",
    )
