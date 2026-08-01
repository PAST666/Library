from django.contrib import admin

from .models import Author, Nationality


@admin.register(Nationality)
class NationalityAdmin(admin.ModelAdmin):
    list_display = (
        "nationality",
        "code",
    )
    ordering = ("nationality",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "birth_date",
        "nationality",
    )
    search_fields = (
        "first_name",
        "last_name",
        "birth_date",
        "nationality",
    )
    ordering = ("last_name",)
    list_filter = ("nationality",)
