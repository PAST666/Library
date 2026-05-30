import pytest
from datetime import date
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from authors.models import Nationality, Author


@pytest.mark.django_db
class TestNationalityModel:

    def test_create_nationality_with_valid_fields(self):
        nationality = Nationality(nationality="Русский", code="RU")
        nationality.full_clean()
        nationality.save()
        nationality.refresh_from_db()
        assert nationality.nationality == "Русский"
        assert nationality.code == "RU"

    def test_create_record_with_empty_field_nationality(self):
        nationality = Nationality(nationality="", code="RU")
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_create_record_with_empty_fields_nationality_and_code(self):
        nationality = Nationality(nationality="", code="")
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_field_nationality_unique(self):
        nationality1 = Nationality(nationality="Русский", code="RU")
        nationality1.save()
        nationality2 = Nationality(nationality="Русский", code="BY")
        with pytest.raises(IntegrityError):
            nationality2.save()

    def test_field_code_unique(self):
        nationality1 = Nationality(nationality="Русский", code="RU")
        nationality1.save()
        nationality2 = Nationality(nationality="Белорусский", code="RU")
        with pytest.raises(IntegrityError):
            nationality2.save()

    def test_max_len_nationality_field_150_symbols(self):
        nationality = Nationality(nationality="а"*150, code="RU")
        nationality.full_clean()
        nationality.save()
        nationality.refresh_from_db()
        assert len(nationality.nationality) == 150

    def test_len_nationality_field_151_symbols(self):
        nationality = Nationality(nationality="а"*151, code="RU")
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_len_code_field_2_symbols(self):
        nationality = Nationality(nationality="Русский", code="RU")
        nationality.full_clean()
        nationality.save()
        assert len(nationality.code) == 2

    def test_len_code_field_1_symbol(self):
        nationality = Nationality(nationality="Русский", code="R")
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_len_code_field_3_symbols(self):
        nationality = Nationality(nationality="Русский", code="RUS")
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_str_method_returns_correct_method(self):
        nationality = Nationality(nationality="Русский", code="RU")
        nationality.full_clean()
        nationality.save()
        nationality.refresh_from_db()
        assert str(nationality) == "Русский"


@pytest.mark.django_db
class TestAuthorModel:

    def test_create_valid_author_instance(self):
        expected_date = date(1990, 1, 1)
        nationality = Nationality(nationality="Русский", code="RU")
        nationality.full_clean()
        nationality.save()
        author = Author(
            first_name="Иван",
            last_name="Иванов",
            birth_date=expected_date,
            nationality=nationality)
        author.full_clean()
        author.save()
        assert author.first_name == "иван"
        assert author.last_name == "иванов"

    def test_create_author_instance_with_empty_first_name_field(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="",
            last_name="Иванов",
            birth_date=expected_date,
        )
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_create_author_instance_with_empty_last_name_field(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="Иван",
            last_name="",
            birth_date=expected_date,
        )
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_create_author_instance_with_empty_first_and_last_name_fields(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="",
            last_name="",
            birth_date=expected_date,
        )
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_first_name_field(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="Иван",
            last_name="Иванов",
            birth_date=expected_date,
        )
        author.full_clean()
        author.save()
        author.refresh_from_db()
        assert author.first_name == "иван"

    def test_first_name_field_latin(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="Ivan",
            last_name="Иванов",
            birth_date=expected_date,
        )
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_last_name_field_latin(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="Иван",
            last_name="Ivanov",
            birth_date=expected_date,
        )
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_first_name_field_contains_numbers(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="Иван123",
            last_name="Иванов",
            birth_date=expected_date,
        )
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_first_name_field_contains_special_symbols(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="Иван!",
            last_name="Иванов",
            birth_date=expected_date,
        )
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_first_name_contains_double_dash(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="Петр-Павел",
            last_name="Иванов",
            birth_date=expected_date,
        )
        author.full_clean()
        author.save()
        author.refresh_from_db()
        assert author.first_name == "петр-павел"

    def test_last_name_contains_double_dash(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="Иван",
            last_name="Сухотина-Толстая",
            birth_date=expected_date,
        )
        author.full_clean()
        author.save()
        author.refresh_from_db()
        assert author.last_name == "сухотина-толстая"

    def test_max_len_first_name_150_symbols(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="а"*150,
            last_name="Иванов",
            birth_date=expected_date,
        )
        author.full_clean()
        author.save()
        assert len(author.first_name) == 150

    def test_len_first_name_151_symbols(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="а"*151,
            last_name="Иванов",
            birth_date=expected_date,
        )
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_len_last_name_151_symbols(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="Иван",
            last_name="а"*151,
            birth_date=expected_date,
        )
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_create_author_with_nationality_field_is_none(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="Иван",
            last_name="Иванов",
            birth_date=expected_date,
            nationality=None,
        )
        author.full_clean()
        author.save()
        author.refresh_from_db()
        assert author.nationality is None

    def test_delete_nationality_field_becomes_none(self):
        expected_date = date(1990, 1, 1)
        nationality = Nationality(nationality="Русский", code="RU")
        nationality.full_clean()
        nationality.save()
        author = Author(
            first_name="Иван",
            last_name="Иванов",
            birth_date=expected_date,
            nationality=nationality,
        )
        author.full_clean()
        author.save()
        nationality.delete()
        author.refresh_from_db()
        assert author.nationality is None

    def test_str_returns_correct_value(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="ИВАН",
            last_name="ИВАНОВ",
            birth_date=expected_date,
        )
        author.full_clean()
        author.save()
        assert str(author) == "иван иванов"

    def test_first_name_and_second_name_become_lower_after_save(self):
        expected_date = date(1990, 1, 1)
        author = Author(
            first_name="ИВАН",
            last_name="ИВАНОВ",
            birth_date=expected_date,
        )
        author.full_clean()
        author.save()
        author.refresh_from_db()
        assert author.first_name == "иван"
        assert author.last_name == "иванов"

    def test_create_author_with_empty_field_birth_date(self):
        author = Author(
            first_name="Иван",
            last_name="Иванов",
        )
        with pytest.raises(ValidationError):
            author.full_clean()
