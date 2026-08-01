from datetime import date

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from users.constants import Roles
from users.models import ActivationToken, Country, User


@pytest.mark.django_db
class TestCountryModel:

    @pytest.fixture
    def country_data(self):
        return {
            "name": "Россия",
            "code": "RU",
        }

    def test_create_country_with_valid_fields(self, country_data):
        country = Country.objects.create(**country_data)
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

    def test_unique_name_field(self, country_data):
        country1 = Country(**country_data)
        country1.save()
        country2 = Country(name="Россия", code="BY")
        with pytest.raises(IntegrityError):
            country2.save()

    def test_unique_code_field(self, country_data):
        country1 = Country(**country_data)
        country1.save()
        country2 = Country(name="Беларусь", code="RU")
        with pytest.raises(IntegrityError):
            country2.save()

    def test_name_field_max_valid_len_20_symbols(self):
        country = Country.objects.create(name="а" * 20, code="RU")
        country.refresh_from_db()
        assert len(country.name) == 20

    def test_name_field_len_21_symbols(self):
        country = Country(name="а" * 21, code="RU")
        with pytest.raises(ValidationError):
            country.full_clean()

    def test_len_of_code_field_is_2_symbols(self, country_data):
        country = Country.objects.create(**country_data)
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

    def test_str_method_returns_valid_value(self, country_data):
        country = Country.objects.create(**country_data)
        country.refresh_from_db()
        assert str(country) == "Россия"


@pytest.mark.django_db
class TestUserModel:

    @pytest.fixture
    def country_data(self):
        return {
            "name": "Россия",
            "code": "RU",
        }

    @pytest.fixture
    def user_data(self):
        return {
            "username": "test_user",
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "test@gmail.com",
            "birth_date": date(1990, 1, 1),
            "password": "securepass123",
        }

    @pytest.fixture
    def user_data_2(self):
        return {
            "username": "test_user2",
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "test@yandex.ru",
            "birth_date": date(1990, 1, 1),
            "password": "securepass123",
        }

    @pytest.fixture
    def user_data_3(self):
        return {
            "username": "test_user3",
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "test@ya.ru",
            "birth_date": date(1990, 1, 1),
            "password": "securepass123",
        }

    @pytest.fixture
    def user_data_4(self):
        return {
            "username": "test_user4",
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "test@mail.ru",
            "birth_date": date(1990, 1, 1),
            "password": "securepass123",
        }

    @pytest.fixture
    def user_data_5(self):
        return {
            "username": "test_user5",
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "test@yahoo.com",
            "birth_date": date(1990, 1, 1),
            "password": "securepass123",
        }

    @pytest.fixture
    def user_data_6(self):
        return {
            "username": "test_user6",
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "test@outlook.com",
            "birth_date": date(1990, 1, 1),
            "password": "securepass123",
        }

    def test_create_valid_user(self, user_data):
        expected_date = date(1990, 1, 1)
        user = User.objects.create_user(**user_data)
        user.refresh_from_db()
        assert user.username == "test_user"
        assert user.first_name == "Иван"
        assert user.last_name == "Иванов"
        assert user.email == "test@gmail.com"
        assert user.birth_date == expected_date
        assert user.check_password("securepass123") is True
        assert user.role == "USER"

    def test_create_user_with_first_name_empty_field(self, user_data):
        user_data["first_name"] = ""
        user = User(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_create_user_with_last_name_empty_field(self, user_data):
        user_data["last_name"] = ""
        user = User(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_first_name_field_language(self, user_data):
        user_data["first_name"] = "Ivan"
        user = User(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_first_name_field_contains_numbers(self, user_data):
        user_data["first_name"] = "Иван123"
        user = User(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_email_field_unique(self, user_data, user_data_2):
        user1 = User(**user_data)
        user1.save()
        user_data_2["email"] = "test@gmail.com"
        user2 = User(**user_data_2)
        with pytest.raises(IntegrityError):
            user2.save()

    def test_different_emails(
        self,
        user_data,
        user_data_2,
        user_data_3,
        user_data_4,
        user_data_5,
        user_data_6,
    ):
        user1 = User.objects.create(**user_data)
        user2 = User.objects.create(**user_data_2)
        user3 = User.objects.create(**user_data_3)
        user4 = User.objects.create(**user_data_4)
        user5 = User.objects.create(**user_data_5)
        user6 = User.objects.create(**user_data_6)
        user1.full_clean()
        user2.full_clean()
        user3.full_clean()
        user4.full_clean()
        user5.full_clean()
        user6.full_clean()

    def test_email_not_valid_field(self, user_data):
        user_data["email"] = "user@protonmail.com"
        user = User(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_not_correct_email(self, user_data):
        user_data["email"] = "not-an-email"
        user = User(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_create_user_with_phone_number_field(self, user_data):
        user_data["phone_number"] = "+79001234567"
        user = User(**user_data)
        user.full_clean()

    def test_create_user_with_phone_number_field_begins_from_8(
        self, user_data
    ):
        user_data["phone_number"] = "89001234567"
        user = User(**user_data)
        user.full_clean()

    def test_invalid_phone_number_field(self, user_data):
        user_data["phone_number"] = "12345"
        user = User.objects.create_user(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_invalid_phone_number_field_with_suffix(self, user_data):
        user_data["phone_number"] = "+79001234567abc"
        user = User.objects.create_user(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_create_user_phone_number_field(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        user.refresh_from_db()
        assert user.phone_number is None

    def test_phone_number_field_unique(self, user_data, user_data_2):
        user_data["phone_number"] = "+79001234567"
        user1 = User(**user_data)
        user1.save()
        user_data_2["phone_number"] = "+79001234567"
        user2 = User(**user_data_2)
        with pytest.raises(IntegrityError):
            user2.save()

    def test_create_user_without_birth_date_field(self):
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            password="securepass123",
            phone_number="+79001234567",
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_birth_date_field_returns_valid_age(self, user_data):
        today = date.today()
        try:
            expected_date = today.replace(year=today.year - 30)
        except ValueError:
            expected_date = today.replace(year=today.year - 30, day=28)
        user_data["birth_date"] = expected_date
        user = User(**user_data)
        user.full_clean()
        user.save()
        user.refresh_from_db()
        assert user.age == 30

    def test_age_returns_none(self, user_data):
        user_data["birth_date"] = None
        user = User(**user_data)
        assert user.age is None

    def test_birth_date_is_later_than_today(self, user_data):
        today = date.today()
        try:
            future_date = today.replace(year=today.year + 1)
        except ValueError:
            future_date = today.replace(year=today.year + 1, day=28)
        user_data["birth_date"] = future_date
        user = User(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_full_name_returns_valid_value(self, user_data):
        user = User(**user_data)
        user.full_clean()
        assert user.full_name == "Иванов Иван"

    def test_default_role_is_user(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        user.refresh_from_db()
        assert user.role == "USER"

    def test_check_roles(
        self,
        user_data,
        user_data_2,
        user_data_3,
        user_data_4,
        user_data_5,
        user_data_6,
    ):
        user_data["role"] = Roles.ADMIN
        user1 = User.objects.create(**user_data)
        user_data_2["role"] = Roles.MODERATOR
        user2 = User.objects.create(**user_data_2)
        user_data_3["role"] = Roles.EDITOR
        user3 = User.objects.create(**user_data_3)
        user_data_4["role"] = Roles.LIBRARIAN
        user4 = User.objects.create(**user_data_4)
        user_data_5["role"] = Roles.VIP
        user5 = User.objects.create(**user_data_5)
        user_data_6["role"] = Roles.USER
        user6 = User.objects.create(**user_data_6)

        user1.full_clean()
        user2.full_clean()
        user3.full_clean()
        user4.full_clean()
        user5.full_clean()
        user6.full_clean()

        assert user1.is_admin is True
        assert user1.is_moderator is False
        assert user1.is_editor is False
        assert user1.is_librarian is False
        assert user1.is_vip is False
        assert user1.is_user is False

        assert user2.is_admin is False
        assert user2.is_moderator is True
        assert user2.is_editor is False
        assert user2.is_librarian is False
        assert user2.is_vip is False
        assert user2.is_user is False

        assert user3.is_admin is False
        assert user3.is_moderator is False
        assert user3.is_editor is True
        assert user3.is_librarian is False
        assert user3.is_vip is False
        assert user3.is_user is False

        assert user4.is_admin is False
        assert user4.is_moderator is False
        assert user4.is_editor is False
        assert user4.is_librarian is True
        assert user4.is_vip is False
        assert user4.is_user is False

        assert user5.is_admin is False
        assert user5.is_moderator is False
        assert user5.is_editor is False
        assert user5.is_librarian is False
        assert user5.is_vip is True
        assert user5.is_user is False

        assert user6.is_admin is False
        assert user6.is_moderator is False
        assert user6.is_editor is False
        assert user6.is_librarian is False
        assert user6.is_vip is False
        assert user6.is_user is True

    def test_is_blocked_false_by_default(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        user.refresh_from_db()
        assert user.is_blocked is False

    def test_country_field_becomes_none_after_delete(
        self, country_data, user_data
    ):
        country = Country.objects.create(**country_data)
        country.full_clean()
        country.save()
        user_data["country"] = country
        user = User(**user_data)
        user.full_clean()
        user.save()
        country.delete()
        user.refresh_from_db()
        assert user.country is None

    def test_str_method_returns_username(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        assert str(user) == "test_user"

    def test_usermanager_createsuperuser(self):
        expected_date = date(1990, 1, 1)
        user = User.objects.create_superuser(
            username="admin",
            first_name="Админ",
            last_name="Админов",
            email="admin@gmail.com",
            birth_date=expected_date,
            password="admin123",
        )
        user.full_clean()
        user.save()
        user.refresh_from_db()
        assert user.role == Roles.ADMIN
        assert user.is_superuser is True


@pytest.mark.django_db
class TestActivationTokenModel:

    @pytest.fixture
    def user_data(self):
        return {
            "username": "test_user",
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "test@gmail.com",
            "birth_date": date(1990, 1, 1),
            "password": "securepass123",
        }

    @pytest.fixture
    def user_data_2(self):
        return {
            "username": "test_user2",
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "test@yandex.ru",
            "birth_date": date(1990, 1, 1),
            "password": "securepass123",
        }

    def test_create_token(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        db_token = ActivationToken.objects.get(pk=token.pk)
        assert db_token is not None
        assert db_token.user == user

    def test_token_field_is_created_automatically(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        token.refresh_from_db()
        assert token.token is not None

    def test_token_field_unique(self, user_data, user_data_2):
        user1 = User(**user_data)
        user2 = User(**user_data_2)
        user1.full_clean()
        user2.full_clean()
        user1.save()
        user2.save()
        token1 = ActivationToken.objects.create_for_user(user1)
        token2 = ActivationToken.objects.create_for_user(user2)
        token1.refresh_from_db()
        token2.refresh_from_db()
        assert token1.token != token2.token

    def test_token_is_valid_true(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        token.refresh_from_db()
        assert token.is_valid is True

    def test_create_token_is_valid_false(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        token.expires_at = timezone.now() - timezone.timedelta(minutes=1)
        token.save()
        token.refresh_from_db()
        assert token.is_valid is False

    def test_error_when_another_token_created_for_user(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        token.refresh_from_db()
        with pytest.raises(IntegrityError):
            ActivationToken.objects.create_for_user(user)

    def test_token_is_deleted_when_user_is_deleted(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        user.delete()
        token_exists = ActivationToken.objects.filter(pk=token.pk).exists()
        assert token_exists is False

    def test_str_method_returns_valid_uuid_token(self, user_data):
        user = User(**user_data)
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        assert str(token) == f"{user.username} -> {token.token}"

    def test_time_of_expires_at_is_about_15_minutes_when_token_created(
        self, user_data
    ):
        user = User(**user_data)
        user.full_clean()
        user.save()
        fix_time = timezone.now()
        token = ActivationToken.objects.create_for_user(user)
        time_delta = token.expires_at - fix_time
        min_delta = timezone.timedelta(minutes=14, seconds=55)
        max_delta = timezone.timedelta(minutes=15, seconds=5)
        assert min_delta <= time_delta <= max_delta
