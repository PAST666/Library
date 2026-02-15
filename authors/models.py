from django.db import models
from books.models import Genre

from .constants import MAX_NAME_LENGTH
from .validators import KirillicLettersValidator



class Author(models.Model):
    name: str = models.CharField(
        "Автор",
        max_length=MAX_NAME_LENGTH,
        validators=[KirillicLettersValidator()],
        unique=True,
        db_index=True,
        verbose_name="Автор"
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
        related_name="books"
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ("name",)

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
