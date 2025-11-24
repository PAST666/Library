from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "photo",
        "is_blocked",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "photo",
        "username",
    )
