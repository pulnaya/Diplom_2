import pytest
from helpers import (
    get_auth_token, create_user_payload,
    prepare_login_payload, prepare_order_payload,
    extract_ingredient_ids, extract_order_data
)
from methods.user_methods import UserMethods
from methods.orders_methods import OrderMethods


@pytest.fixture
def user_methods():
    """Фикстура создает экземпляр UserMethods"""
    return UserMethods()

@pytest.fixture
def create_user(user_methods):
    """Фикстура создает пользователя перед тестом и удаляет после"""
    user_payload = create_user_payload()
    create_response = user_methods.create_user(user_payload)
    
    token = None
    if create_response.status_code == 200:
        token = get_auth_token(create_response)
    
    user_data = {
        "payload": user_payload,
        "response": create_response,
        "token": token
    }
    
    yield user_data 
    
    if token:
        user_methods.delete_user(token)

@pytest.fixture
def cleanup_user(user_methods):
    """
    Фикстура для удалечения пользователя после теста.
    """
    token_storage = []  
    
    yield token_storage 
    
    for token in token_storage:
        if token:
            user_methods.delete_user(token)
    

@pytest.fixture
def authorized_user(create_user, user_methods):
    """
    Фикстура возвращает данные авторизованного пользователя.
    Уже содержит токен для использования в запросах.
    """
    user_data = create_user
    login_payload = prepare_login_payload(user_data)
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
    
    return extract_ingredient_ids(response)

@pytest.fixture
def created_order(authorized_user, order_ingredients, order_methods):
    """
    Фикстура создает заказ для авторизованного пользователя.
    Возвращает данные созданного заказа.
    """
    token = authorized_user['token']
    order_payload = prepare_order_payload(order_ingredients)
    
    response = order_methods.create_order(order_payload, token=token)
    
    return extract_order_data(response)