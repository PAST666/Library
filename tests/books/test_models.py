import pytest
from datetime import date
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from books.models import Genre, Book


@pytest.mark.django_db
class TestGenreModel:

    @pytest.fixture(autouse=True)
    def setup(self):

        self.object = Genre(
            name="Фантастика"
        )
        self.object.name = self.object.name.lower()
        self.object.full_clean()
        self.object.save()

    def test_genre_created(self):
        genre_from_db = Genre.objects.get(name="фантастика")
        assert genre_from_db.name == "фантастика"

    def test_empty_genre(self):
        empty_genre = Genre(name="")
        with pytest.raises(ValidationError):
            empty_genre.full_clean()

    def test_unique_field(self):
        self.genre = Genre(name="Фантастика")
        with pytest.raises(IntegrityError):
            self.genre.save()

    def test_len_150_symbols(self):
        self.genre = Genre(name="а"*150)
        self.genre.full_clean()
        self.genre.save()
        assert len(self.genre.name) == 150

    def test_len_151_symbols(self):
        self.genre = Genre(name="а" * 151)
        self.genre.full_clean()
        with pytest.raises(ValidationError):
            self.genre.save()

    def test_check_lower(self):
        self.genre = Genre(name="ФАНТАСТИКА")
        self.genre.full_clean()
        self.genre.save()
        assert self.genre.name == "фантастика"

    def test_str_method(self):
        self.genre = Genre(name="Фантастика")
        assert str(self.genre) == "фантастика"

    def test_create_book_with_correct_fields(self, author, genre, user):
        expected_date = date(2020, 1, 1)
        book = Book(
            title="Фантастика",
            pages=300,
            publication_date=expected_date,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        book.full_clean()
        book.save()
        book.author.add(author)
        book.genre.add(genre)
        book_from_db = Book.objects.get(pk=book.pk)
        assert book_from_db.title == "Фантастика"
        assert book_from_db.pages == 300
        assert book_from_db.publication_date == expected_date
        assert book_from_db.isbn == "9780306406157"
        assert book_from_db.age_rating == "ABOVE_ZERO"
        assert book_from_db.user == user
        assert book_from_db.author.filter(pk=author.pk).exists()
        assert book_from_db.genre.filter(pk=genre.pk).exists()
