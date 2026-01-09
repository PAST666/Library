from django.db import models
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404


from .constants import (
    MAX_NAME_LENGTH,
    MAX_PAGES_COUNT_LENGTH,
    MAX_PUBLICATION_YEAR_LENGTH,
    MAX_NUMBER_ISBN,
    MAX_AGE_RATING_LENGTH,
    Genre,
    AgeRating
)

from .managers import BookManager

from users.models import User


class Book(models.Model):
    title: str = models.CharField(
        "Книга",
        max_length=MAX_NAME_LENGTH,
    )
    pages: int = models.PositiveSmallIntegerField(
        "Количество страниц",
        validators=[MinValueValidator(1)]
    )
    publication_date: int = models.DateField(
        "Дата издания",
        db_index=True
    )
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Пользователь",
        db_index=True
    )
    genre: str = models.CharField(
        "Жанр",
        choices=Genre.choices,
        max_length=MAX_NAME_LENGTH
    )
    isbn: str = models.CharField(
        "ISBN",
        max_length=MAX_NUMBER_ISBN,
        unique=True
    )
    age_rating: str = models.CharField(
        "Возрастной рейтинг",
        choices=AgeRating.choices,
        max_length=MAX_AGE_RATING_LENGTH
    )
    is_taken: bool = models.BooleanField(
        "Выдана",
        db_index=True,
        default=False
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

    def __str__(self):
        return self.title
