import pytest
from datetime import date
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from authors.models import Nationality, Author


@pytest.mark.django_db
class TestNationalityModel:

    @pytest.fixture
    def nationality_data(self):
        return {
            "nationality": "Русский",
            "code": "RU",
        }

    def test_create_nationality_with_valid_fields(self, nationality_data):
        nationality = Nationality(**nationality_data)
        nationality.full_clean()
        nationality.save()
        nationality.refresh_from_db()
        assert nationality.nationality == "Русский"
        assert nationality.code == "RU"

    def test_create_record_with_empty_field_nationality(self, nationality_data):
        nationality_data["nationality"] = ""
        nationality = Nationality(**nationality_data)
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_create_record_with_empty_fields_nationality_and_code(self, nationality_data):
        nationality_data["nationality"] = ""
        nationality_data["code"] = ""
        nationality = Nationality(**nationality_data)
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_field_nationality_unique(self, nationality_data):
        nationality1 = Nationality(**nationality_data)
        nationality1.save()
        nationality_data["code"] = "BY"
        nationality2 = Nationality(**nationality_data)
        with pytest.raises(IntegrityError):
            nationality2.save()

    def test_field_code_unique(self, nationality_data):
        nationality1 = Nationality(**nationality_data)
        nationality1.save()
        nationality_data["nationality"] = "Белорусский"
        nationality2 = Nationality(**nationality_data)
        with pytest.raises(IntegrityError):
            nationality2.save()

    def test_max_len_nationality_field_150_symbols(self, nationality_data):
        nationality_data["nationality"] = "а"*150
        nationality = Nationality(**nationality_data)
        nationality.full_clean()
        nationality.save()
        nationality.refresh_from_db()
        assert len(nationality.nationality) == 150

    def test_len_nationality_field_151_symbols(self, nationality_data):
        nationality_data["nationality"] = "а" * 151
        nationality = Nationality(**nationality_data)
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_len_code_field_2_symbols(self, nationality_data):
        nationality = Nationality(**nationality_data)
        nationality.full_clean()
        nationality.save()
        assert len(nationality.code) == 2

    def test_len_code_field_1_symbol(self, nationality_data):
        nationality_data["code"] = "R"
        nationality = Nationality(**nationality_data)
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_len_code_field_3_symbols(self, nationality_data):
        nationality_data["code"] = "RUS"
        nationality = Nationality(**nationality_data)
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_str_method_returns_correct_method(self, nationality_data):
        nationality = Nationality(**nationality_data)
        nationality.full_clean()
        nationality.save()
        nationality.refresh_from_db()
        assert str(nationality) == "Русский"


@pytest.mark.django_db
class TestAuthorModel:

    @pytest.fixture
    def author_data(self):
        return {
            "first_name": "Иван",
            "last_name": "Иванов",
            "birth_date": date(1990, 1, 1)
        }

    def test_create_valid_author_instance(self, author_data):
        author = Author(**author_data)
        author.full_clean()
        author.save()
        assert author.first_name == "иван"
        assert author.last_name == "иванов"

    def test_create_author_instance_with_empty_first_name_field(self, author_data):
        author_data["first_name"] = ""
        author = Author(**author_data)
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_create_author_instance_with_empty_last_name_field(self, author_data):
        author_data["last_name"] = ""
        author = Author(**author_data)
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_create_author_instance_with_empty_first_and_last_name_fields(self, author_data):
        author_data["first_name"] = ""
        author_data["last_name"] = ""
        author = Author(**author_data)
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_first_name_field(self, author_data):
        author = Author(**author_data)
        author.full_clean()
        author.save()
        author.refresh_from_db()
        assert author.first_name == "иван"

    def test_first_name_field_latin(self, author_data):
        author_data["first_name"] = "Ivan"
        author = Author(**author_data)
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_last_name_field_latin(self, author_data):
        author_data["last_name"] = "Ivanov"
        author = Author(**author_data)
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_first_name_field_contains_numbers(self, author_data):
        author_data["first_name"] = "Иван123"
        author = Author(**author_data)
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_first_name_field_contains_special_symbols(self, author_data):
        author_data["first_name"] = "Иван!"
        author = Author(**author_data)
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_first_name_contains_double_dash(self, author_data):
        author_data["first_name"] = "Петр-Павел"
        author = Author(**author_data)
        author.full_clean()
        author.save()
        author.refresh_from_db()
        assert author.first_name == "петр-павел"

    def test_last_name_contains_double_dash(self, author_data):
        author_data["last_name"] = "Сухотина-Толстая"
        author = Author(**author_data)
        author.full_clean()
        author.save()
        author.refresh_from_db()
        assert author.last_name == "сухотина-толстая"

    def test_max_len_first_name_150_symbols(self, author_data):
        author_data["first_name"] = "а"*150
        author = Author(**author_data)
        author.full_clean()
        author.save()
        author.refresh_from_db()
        assert len(author.first_name) == 150

    def test_len_first_name_151_symbols(self, author_data):
        author_data["first_name"] = "а"*151
        author = Author(**author_data)
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_len_last_name_151_symbols(self, author_data):
        author_data["last_name"] = "а"*151
        author = Author(**author_data)
        with pytest.raises(ValidationError):
            author.full_clean()

    def test_create_author_with_nationality_field_is_none(self, author_data):
        author = Author(**author_data)
        author.nationality = None
        author.full_clean()
        author.save()
        author.refresh_from_db()
        assert author.nationality is None

    def test_delete_nationality_field_becomes_none(self, author_data):
        nationality = Nationality.objects.create(nationality="Русский", code="RU")
        author_data['nationality'] = nationality
        author = Author.objects.create(**author_data)
        assert author.nationality == nationality
        nationality.delete()
        author.refresh_from_db()
        assert author.nationality is None

    def test_str_returns_correct_value(self, author_data):
        author_data["first_name"] = "ИВАН"
        author_data["last_name"] = "ИВАНОВ"
        author = Author(**author_data)
        author.full_clean()
        author.save()
        assert str(author) == "иван иванов"

    def test_first_name_and_second_name_become_lower_after_save(self, author_data):
        author_data["first_name"] = "ИВАН"
        author_data["last_name"] = "ИВАНОВ"
        author = Author(**author_data)
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
