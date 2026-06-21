from datetime import datetime

from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils import timezone

from .constants import TOKEN_EXPIRES_MINUTES, Roles


class ActivationTokenManager(models.Manager):
    def create_for_user(self, user):
        return self.create(
            user=user,
            expires_at=timezone.now() + timezone.timedelta(
                minutes=TOKEN_EXPIRES_MINUTES,
            )
        )


class UserManager(BaseUserManager):

    def create_user(self, email, birth_date, password=None, **kwargs):
        if not email:
            raise ValueError("Email является обязательным полем")
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            birth_date=birth_date,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('role', Roles.ADMIN)
        if kwargs.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        birth_date = kwargs.pop('birth_date', datetime.now().date())
        if isinstance(birth_date, datetime):
            birth_date = birth_date.date()

        return self.create_user(
            email=email,
            password=password,
            birth_date=birth_date,
            **kwargs
        )


