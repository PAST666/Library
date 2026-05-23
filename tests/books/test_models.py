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
        genre = Genre(name="Фантастика")
        with pytest.raises(IntegrityError):
            genre.save()

    def test_len_150_symbols(self):
        genre = Genre(name="а" * 150)
        genre.full_clean()
        genre.save()
        assert len(genre.name) == 150

    def test_len_151_symbols(self):
        genre = Genre(name="а" * 151)
        with pytest.raises(ValidationError):
            genre.full_clean()

    def test_check_lower(self):
        self.genre = Genre(name="ФАНТАСТИКА")
        self.genre.full_clean()
        self.genre.save()
        assert self.genre.name == "фантастика"

    def test_str_method(self):
        genre = Genre(name="Фантастика")
        assert str(genre) == "фантастика"

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

    def test_empty_title(self):
        expected_date = date(2020, 1, 1)
        book = Book(
            title="",
            pages=300,
            publication_date=expected_date,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO")
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_len_title_150_symbols(self, user):
        expected_date = date(2020, 1, 1)
        book = Book(
            title="а" * 150,
            pages=300,
            publication_date=expected_date,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        book.full_clean()
        book.save()
        assert len(book.title) == 150

    def test_len_title_151_symbols(self, user):
        expected_date = date(2020, 1, 1)
        book = Book(
            title="а" * 151,
            pages=300,
            publication_date=expected_date,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_zero_pages(self, user):
        expected_date = date(2020, 1, 1)
        book = Book(
            title="Фантастика",
            pages=0,
            publication_date=expected_date,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_count_of_pages_one(self, user):
        expected_date = date(2020, 1, 1)
        book = Book(
            title="Фантастика",
            pages=1,
            publication_date=expected_date,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        book.full_clean()
        book.save()
        book_from_db = Book.objects.get(pk=book.pk)
        assert book_from_db.pages == 1
        assert Book.objects.filter(pk=book.pk).exists()

    def test_count_of_pages_low_zero(self, user):
        expected_date = date(2020, 1, 1)
        book = Book(
            title="Фантастика",
            pages=-1,
            publication_date=expected_date,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        with pytest.raises(ValidationError):
            book.full_clean()

    def isbn_is_not_unique(self, user):
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
        book2 = Book(
            title="Фантастика",
            pages=300,
            publication_date=expected_date,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        book2.full_clean()
        with pytest.raises(IntegrityError):
            book2.save()

    def test_isbn_not_valid(self, user):
        expected_date = date(2020, 1, 1)
        book = Book(
            title="Фантастика",
            pages=300,
            publication_date=expected_date,
            isbn="1234567890ABC",
            age_rating="ABOVE_ZERO",
            user=user
        )
        with pytest.raises(ValidationError):
            book.full_clean()

    def age_rating_is_valid(self, user):
        expected_date = date(2020, 1, 1)
        book1 = Book(
            title="Фантастика",
            pages=300,
            publication_date=expected_date,
            isbn="9780306406151",
            age_rating="ABOVE_ZERO",
            user=user
        )
        book1.full_clean()
        book1.save()
        book2 = Book(
            title="Фантастика",
            pages=300,
            publication_date=expected_date,
            isbn="9780306406152",
            age_rating="ABOVE_SIX",
            user=user
        )
        book2.full_clean()
        book2.save()
        book3 = Book(
            title="Фантастика",
            pages=300,
            publication_date=expected_date,
            isbn="9780306406153",
            age_rating="ABOVE_TWELVE",
            user=user
        )
        book3.full_clean()
        book3.save()
        book4 = Book(
            title="Фантастика",
            pages=300,
            publication_date=expected_date,
            isbn="9780306406154",
            age_rating="ABOVE_SIXTEEN",
            user=user
        )
        book4.full_clean()
        book4.save()
        book5 = Book(
            title="Фантастика",
            pages=300,
            publication_date=expected_date,
            isbn="9780306406155",
            age_rating="ABOVE_EIGHTEEN",
            user=user
        )
        book5.full_clean()
        book5.save()
        assert Book.objects.filter(pk=book1.pk).exists()
        assert Book.objects.filter(pk=book2.pk).exists()
        assert Book.objects.filter(pk=book3.pk).exists()
        assert Book.objects.filter(pk=book4.pk).exists()
        assert Book.objects.filter(pk=book5.pk).exists()

    def test_age_rating_not_valid(self, user):
        expected_date = date(2020, 1, 1)
        book = Book(
            title="Фантастика",
            pages=300,
            publication_date=expected_date,
            isbn="9780306406157",
            age_rating="ABOVE_HUNDRED",
            user=user
        )
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_without_publication_date(self, user):
        book = Book(
            title="Фантастика",
            pages=-1,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_create_book_without_user(self):
        book = Book(
            title="Фантастика",
            pages=300,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=None
        )
        book.full_clean()
        book.save()
        assert book.user is None

    def test_delete_user_and_userfield_is_null(self, user):
        book = Book(
            title="Фантастика",
            pages=300,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        book.full_clean()
        book.save()
        user.delete()
        book.refresh_from_db()
        assert Book.objects.filter(pk=book.pk).exists()
        assert book.user is None

    def test_one_book_has_two_authors(self, user, author, author2):
        book = Book(
            title="Фантастика",
            pages=300,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        book.full_clean()
        book.save()
        book.author.set([author, author2])
        assert book.author.count() == 2

    def test_one_book_has_two_genres(self, user):
        genre1 = Genre(name="Фантастика")
        genre2 = Genre(name="Детектив")
        book = Book(
            title="Фантастика",
            pages=300,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        book.full_clean()
        book.save()
        book.genre.set([genre1, genre2])
        assert book.genre.count() == 2

    def test_is_for_child_return_true_above_zero_and_above_six(self, user):
        book1 = Book(
            title="Фантастика",
            pages=300,
            isbn="9780306406151",
            age_rating="ABOVE_ZERO",
            user=user
        )
        book2 = Book(
            title="Фантастика",
            pages=300,
            isbn="9780306406152",
            age_rating="ABOVE_SIX",
            user=user
        )
        book1.full_clean()
        book2.full_clean()
        book1.save()
        book2.save()
        assert book1.is_for_child
        assert book2.is_for_child

    def test_is_for_child_return_false_above_twelve_and_above_sixteen(self, user):
        book1 = Book(
            title="Фантастика",
            pages=300,
            isbn="9780306406151",
            age_rating="ABOVE_TWELVE",
            user=user
        )
        book2 = Book(
            title="Фантастика",
            pages=300,
            isbn="9780306406152",
            age_rating="ABOVE_SIXTEEN",
            user=user
        )
        book3 = Book(
            title="Фантастика",
            pages=300,
            isbn="9780306406153",
            age_rating="ABOVE_EIGHTEEN",
            user=user
        )
        book1.full_clean()
        book2.full_clean()
        book3.full_clean()
        book1.save()
        book2.save()
        book3.save()
        assert not book1.is_for_child
        assert not book2.is_for_child
        assert not book3.is_for_child

    def test_is_for_teenager_return_true_above_twelve_and_above_sixteen(self, user):
        book1 = Book(
            title="Фантастика",
            pages=300,
            isbn="9780306406151",
            age_rating="ABOVE_TWELVE",
            user=user
        )
        book2 = Book(
            title="Детектив",
            pages=300,
            isbn="9780306406152",
            age_rating="ABOVE_SIXTEEN",
            user=user
        )
        book1.full_clean()
        book2.full_clean()
        book1.save()
        book2.save()
        assert book1.is_for_teenager
        assert book2.is_for_teenager
