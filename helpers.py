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


def create_user_payload():
    """Генерирует payload для создания пользователя"""
    return {
        "email": generate_random_email(10),
        "password": generate_random_password(10),
        "name": generate_random_login(10)
    }

def prepare_login_payload(user_data):
    """Подготавливает payload для логина"""
    return {
        "email": user_data['payload']['email'],
        "password": user_data['payload']['password']
    }

def prepare_order_payload(ingredients, count=2):
    """Подготавливает payload для заказа"""
    return {"ingredients": ingredients[:count]}

def extract_ingredient_ids(response):
    """Извлекает ID ингредиентов из ответа"""
    ingredients_data = response.json()
    return [item["_id"] for item in ingredients_data.get("data", [])]

def extract_order_data(response):
    """Извлекает данные заказа из ответа"""
    response_data = response.json()
    return {
        'order_number': response_data["order"]["number"],
        'order_data': response_data["order"],
        'response': response_data
    }