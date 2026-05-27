import pytest
from datetime import date
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from authors.models import Nationality


@pytest.mark.django_db
class TestNationalityModel:

    def test_create_nationality_with_valid_fields(self):
        nationality = Nationality(nationality="Русский", code="RU")
        nationality.full_clean()
        nationality.save()
        nationality_from_db = Nationality.objects.get(pk=nationality.pk)
        assert nationality_from_db.nationality == "Русский"
        assert nationality_from_db.code == "RU"

    def test_create_record_with_empty_field_nationality(self):
        nationality = Nationality(nationality="", code="RU")
        with pytest.raises(ValidationError):
            nationality.full_clean()

    def test_create_record_with_empty_field_code(self):
        nationality = Nationality(nationality="Русский", code="")
        with pytest.raises(ValidationError):
            nationality.full_clean()
