import pytest
from datetime import date
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from users.constants import Roles
from users.models import Country, User


@pytest.mark.django_db
class TestCountryModel:

    def test_create_country_with_valid_fields(self):
        country = Country.objects.create(name="Россия", code="RU")
        country.full_clean()
        country.save()
        country.refresh_from_db()
        assert country.name == "Россия"
        assert country.code == "RU"

    def test_create_record_with_empty_field_name(self):
        country = Country(name="", code="RU")
        with pytest.raises(ValidationError):
            country.full_clean()

    def test_create_record_with_empty_code_name(self):
        country = Country(name="Россия", code="")
        with pytest.raises(ValidationError):
            country.full_clean()

    def test_unique_name_field(self):
        country1 = Country(name="Россия", code="RU")
        country1.save()
        country2 = Country(name="Россия", code="BY")
        with pytest.raises(IntegrityError):
            country2.save()

    def test_unique_code_field(self):
        country1 = Country(name="Россия", code="RU")
        country1.save()
        country2 = Country(name="Беларусь", code="RU")
        with pytest.raises(IntegrityError):
            country2.save()

    def test_name_field_max_valid_len_20_symbols(self):
        country = Country.objects.create(name="а"*20, code="RU")
        country.refresh_from_db()

    def test_name_field_len_21_symbols(self):
        country = Country(name="а"*21, code="RU")
        with pytest.raises(ValidationError):
            country.full_clean()

    def test_len_of_code_field_is_2_symbols(self):
        country = Country.objects.create(name="Россия", code="RU")
        country.full_clean()
        country.save()
        country.refresh_from_db()
        assert len(country.code) == 2

    def test_len_of_code_field_is_3_symbols(self):
        country = Country(name="Россия", code="RUS")
        with pytest.raises(ValidationError):
            country.full_clean()

    def test_len_of_code_field_is_1_symbol(self):
        country = Country(name="Россия", code="R")
        with pytest.raises(ValidationError):
            country.full_clean()

    def test_str_method_returns_valid_value(self):
        country = Country.objects.create(name="Россия", code="RU")
        country.refresh_from_db()
        assert str(country) == "Россия"


@pytest.mark.django_db
class TestUserModel:

    def test_create_valid_user(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123"
        )
        user.full_clean()
        user.save()
        user.refresh_from_db()
        assert user.username == "test_user"
        assert user.first_name == "Иван"
        assert user.last_name == "Иванов"
        assert user.email == "test@gmail.com"
        assert user.birth_date == expected_date
        assert user.password == "securepass123"
        assert user.role == Roles.USER

    def test_create_user_with_first_name_empty_field(self):
        user = User(
            username="test_user",
            first_name="",
            last_name="Иванов",
            email="test@gmail.com",
            password="securepass123"
        )
        with pytest.raises(ValidationError):
            user.full_clean()
