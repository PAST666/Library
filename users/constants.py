MAX_NAME_LENGTH: int = 150
MAX_PHONE_LENGTH: int = 12
MAX_EMAIL_LENGTH: int = 150
TOKEN_EXPIRES_MINUTES: int = 15
MAX_COUNTRY_LENGTH: int = 20
RUSSIAN_LETTERS_RE: str = r'^[а-яА-ЯёЁ]+$'
EMAIL_ALLOWED_DOMAINS_RE: str = r'^[A-Za-z0-9._%+-]+@(gmail.com|yandex.ru|ya.ru|mail.ru|yahoo.com|outlook.com)$'
PHONE_NUMBER_RE: str = r'^(?:+7|8)s*(?d{3})?[-s]?d{3}[-s]?d{2}[-s]?d{2}$'