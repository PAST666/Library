from django.core.validators import RegexValidator


class UserFirstNameAndLastNameValidator(RegexValidator):
    code = "invalid name"
    message = _(
        "Имя должно содержать только буквы латинского или кириллического алфавита"
    )
    regex = r"^[a-zA-Zа-яА-я]*$"
