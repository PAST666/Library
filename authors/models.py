from django.db import models
from books.models import Genre, Book

from .constants import MAX_NAME_LENGTH
from .validators import KirillicLettersValidator


class Author(models.Model):
    first_name: str = models.CharField(
        "Имя",
        max_length=MAX_NAME_LENGTH,
        validators=[KirillicLettersValidator()],
        verbose_name="Имя"
    )
    last_name: str = models.CharField(
        "Фамилия",
        max_length=MAX_NAME_LENGTH,
        validators=[KirillicLettersValidator()],
        unique=True,
        db_index=True,
        verbose_name="Фамилия"
    )
    birth_date = models.DateField(
        "Дата рождения"
    )
    nationality: str = models.CharField(
        "Национальность",
        max_length=MAX_NAME_LENGTH,
        null=True,
        blank=True,
        verbose_name="Национальность"
    )
    genre: str = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        related_name="authors"
    )
    book: str = models.ManyToManyField(
        Book,
        verbose_name="Книга",
        related_name="authors"
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ("last_name", "first_name")

    @property
    def books_count(self) -> int:
        return self.book.count()

    def save(self, *args, **kwargs) -> None:
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
