from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class KirillicLettersValidator(RegexValidator):
    code = "invalid_name"
    message = _("Имя должно содержать только буквы кириллического алфавита")
    regex = r"^[а-яА-ЯёЁ]+(?:-[а-яА-ЯёЁ]+)*$"


class EmailValidator(RegexValidator):
    code = "invalid_user_email"
    message = _(
        "Почта должна быть следующих сервисов: gmail.com, yandex.ru, ya.ru, mail.ru, yahoo.com, outlook.com"
    )
    regex = r"^[A-Za-z0-9._%+-]+@(gmail.com|yandex.ru|ya.ru|mail.ru|yahoo.com|outlook.com)$"


class PhoneNumberValidator(RegexValidator):
    code = "invalid_user_phone_number"
    message = _(
        "Номер телефона начинается с +7 или 8, далее - код оператора 3 цифры (9XX), его допускается брать в скобки, "
        "далее - 7 цифр группами: 3 цифры, 2 цифры, 2 цифры, слитно или с использованием дефисов и/или пробелов. "
        "Допускается весь номер указывать слитно."
    )
    regex = r"^(\+7|8)[\s\-]?\(?[9][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$"
