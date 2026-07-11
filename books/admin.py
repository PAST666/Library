from django.contrib import admin

from books.models import Book, BookInventory, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pages",
        "publication_date",
        "user",
        "isbn",
        "age_rating",
    )
    search_fields = (
        "title",
        "publication_date",
        "author",
        "isbn",
    )
    ordering = ("title",)
    list_filter = ("age_rating",)


@admin.register(BookInventory)
class AdminBookInventory(admin.ModelAdmin):
    list_display = (
        "book",
        "status",
    )
    search_fields = ("book",)
    ordering = ("book",)
    list_filter = ("status",)
