import pytest
import allure
from data import ERROR_USER_ALREADY_EXISTS, ERROR_MISSING_REQUIRED_FIELD
from helpers import create_user_payload


class TestUserCreation:
    
    @allure.title("Создать уникального пользователя")
    def test_create_unique_user(self, user_methods, cleanup_user):
        
        with allure.step('Отправляем запрос для регистрации нового пользователя'):
            user_payload = create_user_payload()
            response = user_methods.create_user(user_payload)  
            cleanup_user.append(response.json().get("accessToken"))

        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 200, f'Ожидался код 200, получен {status_code}. Ответ: {response.text}'
            
        with allure.step('Проверяем что пользователь был создан с переданными данными'):
            response_data = response.json()
            assert response_data.get("success") is True, f"Поле success должно быть True: {response_data}"
            assert "accessToken" in response_data, f"Нет accessToken: {response_data}"
            assert "refreshToken" in response_data, f"Нет refreshToken: {response_data}"
            assert "user" in response_data, f"Нет объекта user: {response_data}"
        
            user_data = response_data["user"]
            assert user_data["email"] == user_payload["email"], (
                f"Email не совпадает. Ожидали: {user_payload['email']}, "
                f"получили: {user_data.get('email')}"
            )
            assert user_data["name"] == user_payload["name"], (
                f"Name не совпадает. Ожидали: {user_payload['name']}, "
                f"получили: {user_data.get('name')}"
            )        

    
    @allure.title("Создать пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, user_methods, create_user):
        
        existing_user_payload = create_user['payload']
        
        with allure.step('Пытаемся зарегестрировать пользователя, который уже зарегистрирован'):
            response = user_methods.create_user(existing_user_payload)
            
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 403, f'Ожидался код 403, получен {status_code}. Ответ: {response.text}'
        
        with allure.step('Проверяем тело ответа'):
            response_data = response.json()
            assert response_data.get("success") is False, (
                f"Поле success должно быть False: {response_data}"
            )
            assert response_data.get("message") == ERROR_USER_ALREADY_EXISTS, (
                f"Ожидалось сообщение '{ERROR_USER_ALREADY_EXISTS}', "
                f"получено: '{response_data.get('message')}'"
            )
    

    @pytest.mark.parametrize(
        "field_to_remove",
        [ "email", 
          "password", 
          "name"
        ]
    )
    @allure.title("Создать пользователя без заполнения одного из обязательных полей")
    def test_create_user_without_required_field(self, user_methods, field_to_remove):
        
        test_payload = create_user_payload()
        test_payload[field_to_remove] = ""
        
        with allure.step(f'Пытаемся зарегестрировать пользователя без заполнения поля {field_to_remove}'):
            response = user_methods.create_user(test_payload)
            
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 403, f'Ожидался код 403, получен {status_code}. Ответ: {response.text}'
        
        with allure.step('Проверяем тело ответа'):
            response_data = response.json()
            assert response_data.get("success") is False, (
                f"Поле success должно быть False: {response_data}"
            )
            assert response_data.get("message") == ERROR_MISSING_REQUIRED_FIELD, (
                f"Ожидалось сообщение '{ERROR_MISSING_REQUIRED_FIELD}', "
                f"получено: '{response_data.get('message')}'"
            )
    