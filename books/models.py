from django.db import models
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from isbn_field import ISBNField
from users.models import User

from .constants import (
    MAX_NAME_LENGTH,
    MAX_NUMBER_ISBN,
    MAX_AGE_RATING_LENGTH,
    MAX_STATUS_LENGTH,
    AgeRating,
    Status
)

from .managers import BookManager


class Author(models.Model):
    name: str = models.CharField(
        "Автор",
        db_index=True
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name: str = models.CharField(
        "Жанр",
        max_length=MAX_NAME_LENGTH,
        db_index=True
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Book(models.Model):
    title: str = models.CharField(
        "Книга",
        max_length=MAX_NAME_LENGTH,
        db_index=True
    )
    pages: int = models.PositiveSmallIntegerField(
        "Количество страниц",
        validators=[MinValueValidator(1)]
    )
    publication_date: int = models.DateField(
        "Дата издания",
        db_index=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Пользователь",
        related_name="books",
        db_index=True
    )
    author: str = models.ManyToManyField(
        Author,
        related_name="authors"
    )
    genre: str = models.ManyToManyField(
        Genre,
        related_name="books"
    )
    isbn: str = ISBNField(
        "ISBN",
        max_length=MAX_NUMBER_ISBN,
        unique=True
    )
    age_rating: str = models.CharField(
        "Возрастной рейтинг",
        choices=AgeRating.choices,
        max_length=MAX_AGE_RATING_LENGTH
    )
    objects = BookManager()

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ("title",)

    def create_book(self, user, **kwargs):
        return self.create(user=user, **kwargs)

    def update_book(self, book_id, new_title=None, new_pages=None, new_publication_year=None):
        book = get_object_or_404(self.model, id=book_id)
        if new_title:
            book.title = new_title
        if new_pages is not None:
            book.pages = new_pages
        if new_publication_year is not None:
            book.publication_year = new_publication_year
        book.save()
        return book

    def delete_book(self, book_id):
        book = get_object_or_404(self.model, id=book_id)
        book.delete()

    def clean_isbn(self):
        if not self.isbn:
            return ""
        clean_number = self.replace(" ", "").replace("-", "").removeprefix("ISBN")
        if len(clean_number) != MAX_NUMBER_ISBN:
            raise ValueError("Количество цифр в номере ISBN некорректное.")
        return clean_number

    @property
    def is_for_child(self) -> bool:
        return self.age_rating == "ABOVE_ZERO" or "ABOVE_SIX"

    @property
    def is_for_teenager(self) -> bool:
        return self.age_rating == "ABOVE_TWELVE" or "ABOVE_SIXTEEN"

    @property
    def is_for_adult(self) -> bool:
        return self.age_rating == "ABOVE_EIGHTEEN"

    def __str__(self):
        return self.title


class BookInventory(models.Model):
    book: str = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        related_name="book_inventory",
        db_index=True
    )
    status: str = models.CharField(
        "Статус",
        choices=Status.choices,
        max_length=MAX_STATUS_LENGTH
    )

    class Meta:
        verbose_name = "Перечень книг"
        verbose_name_plural = "Перечни книг"
        ordering = ("status",)

    def __str__(self):
        return self.book
