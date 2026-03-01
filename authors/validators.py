from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class KirillicLettersValidator(RegexValidator):
    code = "invalid_name"
    message = _(
        "Имя должно содержать только буквы кириллического алфавита"
    )
    regex = r"^[а-яА-ЯёЁ]+$"
