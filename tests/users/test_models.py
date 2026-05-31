import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from users.constants import Roles
from users.models import Country, User, ActivationToken


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
        country = Country.objects.create(name="а" * 20, code="RU")
        country.refresh_from_db()

    def test_name_field_len_21_symbols(self):
        country = Country(name="а" * 21, code="RU")
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
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123"
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_create_user_with_last_name_empty_field(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123"
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_first_name_field_language(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Ivan",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123"
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_first_name_field_contains_numbers(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван123",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123"
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_email_field_unique(self):
        expected_date = date(1990, 1, 1)
        user1 = User(
            username="test_user1",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123"
        )
        user1.save()
        user2 = User(
            username="test_user2",
            first_name="Андрей",
            last_name="Белов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass345"
        )
        with pytest.raises(IntegrityError):
            user2.save()

    def test_different_emails(self):
        expected_date = date(1990, 1, 1)
        user1 = User.objects.create(
            username="test_user1",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123"
        )
        user2 = User.objects.create(
            username="test_user2",
            first_name="Иван",
            last_name="Иванов",
            email="test@yandex.ru",
            birth_date=expected_date,
            password="securepass123"
        )
        user3 = User.objects.create(
            username="test_user3",
            first_name="Иван",
            last_name="Иванов",
            email="test@ya.ru",
            birth_date=expected_date,
            password="securepass123"
        )
        user4 = User.objects.create(
            username="test_user4",
            first_name="Иван",
            last_name="Иванов",
            email="test@mail.ru",
            birth_date=expected_date,
            password="securepass123"
        )
        user5 = User.objects.create(
            username="test_user5",
            first_name="Иван",
            last_name="Иванов",
            email="test@yahoo.com",
            birth_date=expected_date,
            password="securepass123"
        )
        user6 = User.objects.create(
            username="test_user6",
            first_name="Иван",
            last_name="Иванов",
            email="test@outlook.com",
            birth_date=expected_date,
            password="securepass123"
        )
        user1.full_clean()
        user2.full_clean()
        user3.full_clean()
        user4.full_clean()
        user5.full_clean()
        user6.full_clean()

    def test_email_not_valid_field(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="user@protonmail.com",
            birth_date=expected_date,
            password="securepass123"
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_not_correct_email(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="not-an-email",
            birth_date=expected_date,
            password="securepass123"
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_create_user_with_phone_number_field(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            phone_number="+79001234567"
        )
        user.full_clean()

    def test_create_user_with_phone_number_field_begins_from_8(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            phone_number="89001234567"
        )
        user.full_clean()

    def test_invalid_phone_number_field(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            phone_number="12345"
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_invalid_phone_number_field_with_suffix(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            phone_number="+79001234567abc"
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_create_user_phone_number_field(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123",
        )
        user.full_clean()
        user.save()
        user.refresh_from_db()
        assert user.phone_number is None

    def test_phone_number_field_unique(self):
        expected_date = date(1990, 1, 1)
        user1 = User(
            username="test_user1",
            first_name="Иван",
            last_name="Иванов",
            email="test1@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            phone_number="+79001234567"
        )
        user1.save()
        user2 = User(
            username="test_user2",
            first_name="Андрей",
            last_name="Белов",
            email="test2@gmail.com",
            birth_date=expected_date,
            password="securepass345",
            phone_number="+79001234567"
        )
        with pytest.raises(IntegrityError):
            user2.save()

    def test_create_user_without_birth_date_field(self):
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            password="securepass123",
            phone_number="+79001234567"
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_birth_date_field_returns_valid_age(self):
        today = date.today()
        try:
            expected_date = today.replace(year=today.year - 30)
        except ValueError:
            expected_date = today.replace(year=today.year - 30, day=28)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123",
        )
        user.full_clean()
        user.save()
        user.refresh_from_db()
        assert user.age == 30

    def test_age_returns_none(self):
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=None,
            password="securepass123",
            phone_number="+79001234567"
        )
        assert user.age is None

    def test_birth_date_is_later_than_today(self):
        today = date.today()
        try:
            future_date = today.replace(year=today.year + 1)
        except ValueError:
            future_date = today.replace(year=today.year + 1, day=28)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=future_date,
            password="securepass123",
        )
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_full_name_returns_valid_value(self):
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
        assert user.full_name == "Иванов Иван"

    def test_default_role_is_user(self):
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
        assert user.role == "USER"

    def test_check_roles(self):
        expected_date = date(1990, 1, 1)
        user1 = User.objects.create(
            username="test_user1",
            first_name="Иван",
            last_name="Иванов",
            email="test1@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            role="ADMIN"
        )
        user2 = User.objects.create(
            username="test_user2",
            first_name="Иван",
            last_name="Иванов",
            email="test2@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            role="MODERATOR"
        )
        user3 = User.objects.create(
            username="test_user3",
            first_name="Иван",
            last_name="Иванов",
            email="test3@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            role="EDITOR"
        )
        user4 = User.objects.create(
            username="test_user4",
            first_name="Иван",
            last_name="Иванов",
            email="test4@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            role="LIBRARIAN"
        )
        user5 = User.objects.create(
            username="test_user5",
            first_name="Иван",
            last_name="Иванов",
            email="test5@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            role="VIP"
        )
        user6 = User.objects.create(
            username="test_user6",
            first_name="Иван",
            last_name="Иванов",
            email="test6@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            role="USER"
        )
        user1.full_clean()
        user2.full_clean()
        user3.full_clean()
        user4.full_clean()
        user5.full_clean()
        user6.full_clean()

        assert user1.role == "ADMIN"
        assert not user1.role == "MODERATOR"
        assert not user1.role == "EDITOR"
        assert not user1.role == "LIBRARIAN"
        assert not user1.role == "VIP"
        assert not user1.role == "USER"

        assert not user2.role == "ADMIN"
        assert user2.role == "MODERATOR"
        assert not user2.role == "EDITOR"
        assert not user2.role == "LIBRARIAN"
        assert not user2.role == "VIP"
        assert not user2.role == "USER"

        assert not user3.role == "ADMIN"
        assert not user3.role == "MODERATOR"
        assert user3.role == "EDITOR"
        assert not user3.role == "LIBRARIAN"
        assert not user3.role == "VIP"
        assert not user3.role == "USER"

        assert not user4.role == "ADMIN"
        assert not user4.role == "MODERATOR"
        assert not user4.role == "EDITOR"
        assert user4.role == "LIBRARIAN"
        assert not user4.role == "VIP"
        assert not user4.role == "USER"

        assert not user5.role == "ADMIN"
        assert not user5.role == "MODERATOR"
        assert not user5.role == "EDITOR"
        assert not user5.role == "LIBRARIAN"
        assert user5.role == "VIP"
        assert not user5.role == "USER"

        assert not user6.role == "ADMIN"
        assert not user6.role == "MODERATOR"
        assert not user6.role == "EDITOR"
        assert not user6.role == "LIBRARIAN"
        assert not user6.role == "VIP"
        assert user6.role == "USER"

    def test_is_blocked_false_by_default(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user1",
            first_name="Иван",
            last_name="Иванов",
            email="test1@gmail.com",
            birth_date=expected_date,
            password="securepass123",
        )
        user.full_clean()
        user.save()
        user.refresh_from_db()
        assert user.is_blocked is False

    def test_country_field_becomes_none_after_delete(self):
        expected_date = date(1990, 1, 1)
        country = Country.objects.create(name="Россия", code="RU")
        country.full_clean()
        country.save()
        user = User(
            username="test_user1",
            first_name="Иван",
            last_name="Иванов",
            email="test1@gmail.com",
            birth_date=expected_date,
            password="securepass123",
            country=country
        )
        user.full_clean()
        user.save()
        country.delete()
        user.refresh_from_db()
        assert user.country is None

    def test_str_method_returns_username(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test1@gmail.com",
            birth_date=expected_date,
            password="securepass123",
        )
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
            role="ADMIN"
        )
        user.full_clean()
        user.save()
        user.refresh_from_db()
        assert user.role == "ADMIN"
        assert user.is_superuser is True


@pytest.mark.django_db
class TestActivationTokenModel:

    def test_create_token(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123",
        )
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        db_token = ActivationToken.objects.get(pk=token.pk)
        assert db_token is not None
        assert db_token.user == user

    def test_token_field_is_created_automatically(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123",
        )
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        token.refresh_from_db()
        assert token.token is not None

    def test_token_field_unique(self):
        expected_date = date(1990, 1, 1)
        user1 = User(
            username="test_user1",
            first_name="Иван",
            last_name="Иванов",
            email="test1@gmail.com",
            birth_date=expected_date,
            password="securepass123",
        )
        user2 = User(
            username="test_user2",
            first_name="Иван",
            last_name="Иванов",
            email="test2@gmail.com",
            birth_date=expected_date,
            password="securepass123",
        )
        user1.full_clean()
        user2.full_clean()
        user1.save()
        user2.save()
        token1 = ActivationToken.objects.create_for_user(user1)
        token2 = ActivationToken.objects.create_for_user(user2)
        token1.refresh_from_db()
        token2.refresh_from_db()
        assert token1.token != token2.token

    def test_token_is_valid_true(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123",
        )
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        token.refresh_from_db()
        assert token.is_valid() is True

    def test_create_token_is_valid_false(self):
        expected_date = date(1990, 1, 1)
        user = User(
            username="test_user",
            first_name="Иван",
            last_name="Иванов",
            email="test@gmail.com",
            birth_date=expected_date,
            password="securepass123",
        )
        user.full_clean()
        user.save()
        token = ActivationToken.objects.create_for_user(user)
        token.expires_at = timezone.now() - timezone.timedelta(minutes=1)
        token.save()
        token.refresh_from_db()
        assert token.is_valid() is False
