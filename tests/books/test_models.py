import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from books.models import Genre, Book, BookInventory


@pytest.mark.django_db
class TestGenreModel:

    def test_genre_created(self, genre_data):
        genre = Genre(**genre_data)
        genre.full_clean()
        genre.save()
        genre_from_db = Genre.objects.get(pk=genre.pk)
        assert genre_from_db.name == "фантастика"

    def test_empty_genre(self, genre_data):
        genre_data["name"] = ""
        empty_genre = Genre(**genre_data)
        with pytest.raises(ValidationError):
            empty_genre.full_clean()

    def test_unique_field(self, genre_data):
        genre1 = Genre(**genre_data)
        genre1.save()
        genre2 = Genre(**genre_data)
        with pytest.raises(IntegrityError):
            genre2.save()

    def test_len_150_symbols(self, genre_data):
        genre_data["name"] = "а" * 150
        genre = Genre(**genre_data)
        genre.full_clean()
        genre.save()
        assert len(genre.name) == 150

    def test_len_151_symbols(self, genre_data):
        genre_data["name"] = "а" * 151
        genre = Genre(**genre_data)
        with pytest.raises(ValidationError):
            genre.full_clean()

    def test_check_lower(self):
        self.genre = Genre(name="УЖАСЫ")
        self.genre.full_clean()
        self.genre.save()
        assert self.genre.name == "ужасы"

    def test_str_method(self):
        genre = Genre(name="Детектив")
        genre.save()
        genre.refresh_from_db()
        assert str(genre) == "детектив"

    def test_create_book_with_correct_fields(self, author, genre, user, book_data):
        book = Book(**book_data)
        book.full_clean()
        book.save()
        book.author.add(author)
        book.genre.add(genre)
        book_from_db = Book.objects.get(pk=book.pk)
        assert book_from_db.title == "Фантастика"
        assert book_from_db.pages == 300
        assert book_from_db.publication_date == book.publication_date
        assert book_from_db.isbn == "9780306406157"
        assert book_from_db.age_rating == "ABOVE_ZERO"
        assert book_from_db.user == user
        assert book_from_db.author.filter(pk=author.pk).exists()
        assert book_from_db.genre.filter(pk=genre.pk).exists()

    def test_empty_title(self, book_data):
        book_data["title"] = ""
        book = Book(**book_data)
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_len_title_150_symbols(self, user, book_data):
        book_data["title"] = "а" * 150
        book = Book(**book_data)
        book.full_clean()
        book.save()
        assert len(book.title) == 150

    def test_len_title_151_symbols(self, user, book_data):
        book_data["title"] = "а" * 151
        book = Book(**book_data)
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_zero_pages(self, book_data):
        book_data["pages"] = 0
        book = Book(**book_data)
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_count_of_pages_one(self, book_data):
        book_data["pages"] = 1
        book = Book(**book_data)
        book.full_clean()
        book.save()
        book_from_db = Book.objects.get(pk=book.pk)
        assert book_from_db.pages == 1
        assert Book.objects.filter(pk=book.pk).exists()

    def test_count_of_pages_low_zero(self, book_data):
        book_data["pages"] = -1
        book = Book(**book_data)
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_isbn_is_not_unique(self, book_data):
        book = Book(**book_data)
        book.full_clean()
        book.save()
        book2 = Book(**book_data)
        with pytest.raises(IntegrityError):
            book2.save()

    def test_isbn_not_valid(self, book_data):
        book_data["isbn"] = "1234567890ABC"
        book = Book(**book_data)
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_age_rating_is_valid(self, book_data, book_data_2, book_data_3, book_data_4, book_data_5):
        book1 = Book(**book_data)
        book1.full_clean()
        book1.save()
        book2 = Book(**book_data_2)
        book2.full_clean()
        book2.save()
        book3 = Book(**book_data_3)
        book3.full_clean()
        book3.save()
        book4 = Book(**book_data_4)
        book4.full_clean()
        book4.save()
        book5 = Book(**book_data_5)
        book5.full_clean()
        book5.save()
        assert Book.objects.filter(pk=book1.pk).exists()
        assert Book.objects.filter(pk=book2.pk).exists()
        assert Book.objects.filter(pk=book3.pk).exists()
        assert Book.objects.filter(pk=book4.pk).exists()
        assert Book.objects.filter(pk=book5.pk).exists()

    def test_age_rating_not_valid(self, book_data):
        book_data["age_rating"] = "ABOVE_HUNDRED"
        book = Book(**book_data)
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_without_publication_date(self, user):
        book = Book(
            title="Фантастика",
            pages=100,
            isbn="9780306406157",
            age_rating="ABOVE_ZERO",
            user=user
        )
        with pytest.raises(ValidationError):
            book.full_clean()

    def test_create_book_without_user(self, book_data):
        book_data["user"] = None
        book = Book(**book_data)
        assert book.full_clean() is None


    def test_delete_user_and_userfield_is_null(self, book_data):
        book = Book(**book_data)
        book.full_clean()
        book.save()
        book.user.delete()
        book.refresh_from_db()
        assert Book.objects.filter(pk=book.pk).exists()
        assert book.user is None

    def test_one_book_has_two_authors(self, user, author, author2, book_data):
        book = Book(**book_data)
        book.full_clean()
        book.save()
        book.author.set([author, author2])
        assert book.author.count() == 2

    def test_one_book_has_two_genres(self, book_data, genre_data, genre_data_2):
        genre1 = Genre(**genre_data)
        genre1.full_clean()
        genre1.save()
        genre2 = Genre(**genre_data_2)
        genre2.full_clean()
        genre2.save()
        book = Book(**book_data)
        book.full_clean()
        book.save()
        book.genre.set([genre1, genre2])
        assert book.genre.count() == 2

    def test_is_for_child_return_true_above_zero_and_above_six(self, book_data, book_data_2):
        book1 = Book(**book_data)
        book2 = Book(**book_data_2)
        book1.full_clean()
        book2.full_clean()
        book1.save()
        book2.save()
        assert book1.is_for_child
        assert book2.is_for_child

    def test_is_for_child_return_false_above_twelve_and_above_sixteen(self, book_data_3, book_data_4, book_data_5):
        book1 = Book(**book_data_3)
        book2 = Book(**book_data_4)
        book3 = Book(**book_data_5)
        book1.full_clean()
        book2.full_clean()
        book3.full_clean()
        book1.save()
        book2.save()
        book3.save()
        assert not book1.is_for_child
        assert not book2.is_for_child
        assert not book3.is_for_child

    def test_is_for_teenager_return_true_above_twelve_and_above_sixteen(self, book_data_3, book_data_4):
        book1 = Book(**book_data_3)
        book2 = Book(**book_data_4)
        book1.full_clean()
        book2.full_clean()
        book1.save()
        book2.save()
        assert book1.is_for_teenager
        assert book2.is_for_teenager

    def test_is_for_adult_return_true_above_eighteen(
            self,
            book_data,
            book_data_2,
            book_data_3,
            book_data_4,
            book_data_5
    ):
        book1 = Book(**book_data)
        book2 = Book(**book_data_2)
        book3 = Book(**book_data_3)
        book4 = Book(**book_data_4)
        book5 = Book(**book_data_5)
        book1.full_clean()
        book2.full_clean()
        book3.full_clean()
        book4.full_clean()
        book5.full_clean()
        book1.save()
        book2.save()
        book3.save()
        book4.save()
        book5.save()
        assert not book1.is_for_adult
        assert not book2.is_for_adult
        assert not book3.is_for_adult
        assert not book4.is_for_adult
        assert book5.is_for_adult

    def test_str_returns_correct_value(self, book_data):
        book_data["title"] = "Мастер и Маргарита"
        book = Book(**book_data)
        book.full_clean()
        book.save()
        assert str(book) == "Мастер и Маргарита"


@pytest.mark.django_db
class TestBookInventoryModel:

    def test_create_book_inventory(self, book_inventory_data):
        book_inventory = BookInventory(**book_inventory_data)
        book_inventory.full_clean()
        book_inventory.save()
        assert BookInventory.objects.filter(pk=book_inventory.pk).exists()

    def test_create_some_examples_of_book(self, book_data):
        book = Book(**book_data)
        book.full_clean()
        book.save()
        book_inventory1 = BookInventory(book=book, status="AVAILABLE")
        book_inventory2 = BookInventory(book=book, status="AVAILABLE")
        book_inventory3 = BookInventory(book=book, status="AVAILABLE")
        book_inventory1.full_clean()
        book_inventory2.full_clean()
        book_inventory3.full_clean()
        book_inventory1.save()
        book_inventory2.save()
        book_inventory3.save()
        assert BookInventory.objects.filter(pk=book_inventory1.pk).exists()
        assert BookInventory.objects.filter(pk=book_inventory2.pk).exists()
        assert BookInventory.objects.filter(pk=book_inventory3.pk).exists()

    def test_valid_records_book_inventories_with_all_statuses(self, book_data):
        book = Book(**book_data)
        book.full_clean()
        book.save()
        book_inventory1 = BookInventory(book=book, status="AVAILABLE")
        book_inventory2 = BookInventory(book=book, status="BUSY")
        book_inventory3 = BookInventory(book=book, status="RESERVED")
        book_inventory1.full_clean()
        book_inventory2.full_clean()
        book_inventory3.full_clean()
        book_inventory1.save()
        book_inventory2.save()
        book_inventory3.save()
        assert BookInventory.objects.filter(pk=book_inventory1.pk).exists()
        assert BookInventory.objects.filter(pk=book_inventory2.pk).exists()
        assert BookInventory.objects.filter(pk=book_inventory3.pk).exists()

    def test_create_record_with_not_valid_status(self, book_inventory_data):
        book_inventory_data["status"] = "LOST"
        book_inventory = BookInventory(**book_inventory_data)
        with pytest.raises(ValidationError):
            book_inventory.full_clean()

    def test_create_record_without_status(self, book_data):
        book = Book(**book_data)
        book.full_clean()
        book.save()
        book_inventory = BookInventory(book=book)
        with pytest.raises(ValidationError):
            book_inventory.full_clean()

    def test_str_at_created_book(self, book_data):
        book_data["title"] = "Мастер и Маргарита"
        book = Book(**book_data)
        book.full_clean()
        book.save()
        book_inventory = BookInventory(book=book, status="AVAILABLE")
        book_inventory.full_clean()
        book_inventory.save()
        assert str(book_inventory) == "Мастер и Маргар | 9780306406157 -> AVAILABLE"


@pytest.mark.django_db
class TestBookManagerModel:

    def test_get_all_books_list(self, book_data, book_data_2, book_data_3):
        book1 = Book(**book_data)
        book2 = Book(**book_data_2)
        book3 = Book(**book_data_3)
        book1.full_clean()
        book2.full_clean()
        book3.full_clean()
        book1.save()
        book2.save()
        book3.save()
        assert set(Book.objects.get_all_books_list()) == {book1, book2, book3}

    def test_return_available_only(self, book_data, book_data_2, book_data_3):
        book1 = Book(**book_data)
        book2 = Book(**book_data_2)
        book3 = Book(**book_data_3)
        book1.full_clean()
        book2.full_clean()
        book3.full_clean()
        book1.save()
        book2.save()
        book3.save()
        BookInventory.objects.create(book=book1, status="AVAILABLE")
        BookInventory.objects.create(book=book2, status="BUSY")
        BookInventory.objects.create(book=book3, status="RESERVED")
        assert list(Book.objects.available()) == [book1]

    def test_return_busy_only(self, book_data, book_data_2, book_data_3):
        book1 = Book(**book_data)
        book2 = Book(**book_data_2)
        book3 = Book(**book_data_3)
        book1.full_clean()
        book2.full_clean()
        book3.full_clean()
        book1.save()
        book2.save()
        book3.save()
        BookInventory.objects.create(book=book1, status="AVAILABLE")
        BookInventory.objects.create(book=book2, status="BUSY")
        BookInventory.objects.create(book=book3, status="RESERVED")
        assert list(Book.objects.busy()) == [book2]

    def test_return_reserved_only(self, book_data, book_data_2, book_data_3):
        book1 = Book(**book_data)
        book2 = Book(**book_data_2)
        book3 = Book(**book_data_3)
        book1.full_clean()
        book2.full_clean()
        book3.full_clean()
        book1.save()
        book2.save()
        book3.save()
        BookInventory.objects.create(book=book1, status="AVAILABLE")
        BookInventory.objects.create(book=book2, status="BUSY")
        BookInventory.objects.create(book=book3, status="RESERVED")
        assert list(Book.objects.reserved()) == [book3]

    def test_search_books(self, book_data, book_data_2):
        book_data["title"] = "Война и мир"
        book1 = Book.objects.create(**book_data)
        Book.objects.create(**book_data_2)
        search_result = Book.objects.search_books(title="Война")
        assert list(search_result) == [book1]

    def test_search_books_unknown_filter(self, book_data, book_data_2):
        book1 = Book(**book_data)
        book2 = Book(**book_data_2)
        book1.full_clean()
        book2.full_clean()
        book1.save()
        book2.save()
        assert set(Book.objects.search_books(unknown_field="значение")) == {book1, book2}

    def test_recent_five_years(self, book_data, book_data_2, book_data_3):
        book1 = Book(**book_data)
        book2 = Book(**book_data_2)
        book3 = Book(**book_data_3)
        book1.full_clean()
        book2.full_clean()
        book3.full_clean()
        book1.save()
        book2.save()
        book3.save()
        assert set(Book.objects.recent()) == {book2, book3}

    def test_recent_one_year(self, book_data, book_data_2, book_data_3):
        book1 = Book(**book_data)
        book2 = Book(**book_data_2)
        book3 = Book(**book_data_3)
        book1.full_clean()
        book2.full_clean()
        book3.full_clean()
        book1.save()
        book2.save()
        book3.save()
        assert list(Book.objects.recent(years=1)) == [book3]
