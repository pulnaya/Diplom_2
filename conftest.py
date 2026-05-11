import pytest
from helpers import generate_random_login, generate_random_email, generate_random_password, get_auth_token
from methods.user_methods import UserMethods
from methods.orders_methods import OrderMethods


@pytest.fixture
def user_methods():
    """Фикстура создает экземпляр UserMethods"""
    return UserMethods()

@pytest.fixture
def create_user_payload():
    """Фикстура генерирует payload для создания пользователя"""
    return {
        "email": generate_random_email(10),
        "password": generate_random_password(10),
        "name": generate_random_login(10)
    }

@pytest.fixture
def create_user(create_user_payload, user_methods):
    """Фикстура создает пользователя перед тестом и удаляет после"""
    create_response = user_methods.create_user(create_user_payload)
    
    token = None
    if create_response.status_code == 200:
        token = get_auth_token(create_response)
    
    user_data = {
        "payload": create_user_payload,
        "response": create_response,
        "token": token
    }
    
    yield user_data 
    
    if token:
        user_methods.delete_user(token)

@pytest.fixture
def authorized_user(create_user, user_methods):
    """
    Фикстура возвращает данные авторизованного пользователя.
    Уже содержит токен для использования в запросах.
    """
    user_data = create_user
    login_payload = {"email": user_data['payload']['email'], "password": user_data['payload']['password']}
    user_methods.login_user(login_payload)
    
    return {
        'email': user_data['payload']['email'],
        'name': user_data['payload']['name'],
        'token': user_data['token'], 
    }

@pytest.fixture
def order_methods():
    """Фикстура создает экземпляр OrderMethods"""
    return OrderMethods()

@pytest.fixture
def order_ingredients(order_methods):
    """Фикстура возвращает спислок валидных ID ингредиентов для заказа."""
    response = order_methods.get_ingredients()
    
    ingredients_data = response.json()
    
    ingredients = [item["_id"] for item in ingredients_data.get("data", [])]

    return ingredients

@pytest.fixture
def created_order(authorized_user, order_ingredients, order_methods):
    """
    Фикстура создает заказ для авторизованного пользователя.
    Возвращает данные созданного заказа.
    """
    token = authorized_user['token']
    ingredients = order_ingredients[:2]
    order_payload = {"ingredients": ingredients}
    
    response = order_methods.create_order(order_payload, token=token)
    response_data = response.json()
    
    return {
        'order_number': response_data["order"]["number"],
        'order_data': response_data["order"],
        'response': response_data
    }