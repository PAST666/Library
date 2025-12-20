from django.db import models
from django.utils import timezone

from .constants import (
    TOKEN_EXPIRES_MINUTES
)


class ActivationTokenManager(models.Manager):
    def create_for_user(self, user):
        return self.create(
            user=user,
            expires_at=timezone.now() + timezone.timedelta(
                minutes=TOKEN_EXPIRES_MINUTES,
            )
        )
