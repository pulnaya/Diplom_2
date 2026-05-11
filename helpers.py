import random
import string


def generate_random_login(length=10):
    """Генерирует случайную строку"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_email(length=10):
    """Генерирует случайный email"""
    username = generate_random_login(length)
    return f"{username}@example.com"


def generate_random_password(length=10):
    """Генерирует случайный пароль"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def get_auth_token(response):
    """Извлекает токен из ответа API"""
    response_data = response.json()
    return response_data.get("accessToken")
