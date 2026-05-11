import allure
import pytest
from data import ERROR_INVALID_CREDENTIALS

class TestLoginUser:

    @allure.title('Логин пользователя с верными данными авторизации')
    def test_login_existing_user(self, create_user, user_methods):

        user_payload = create_user['payload']
        login_payload = {
            'email': user_payload['email'],
            'password': user_payload['password'],
        }
        
        with allure.step('Отправляем запрос на авторизацию для существующего пользователя'):
            response = user_methods.login_user(login_payload)
        
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 200, f"Ожидался код 200, получен {status_code}. Ответ: {response.text}"
                                        
        with allure.step('Проверяем что полученны данные пользователь под которым проходила авторизация'):
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


    @pytest.mark.parametrize("wrong_field, wrong_value",[
                    ["email", "wrong_email@example.com"],
                    ["email", ""],
                    ["password", "wrong_password"],
                    ["password", ""]
    ])
    @allure.title("Логин пользователя с неверными данными авторизации")
    def test_login_invalid_credentials(self, create_user, user_methods, wrong_field, wrong_value):
        user_payload = create_user['payload']
        login_payload = {
            'email': user_payload['email'],
            'password': user_payload['password'],
            }
        login_payload[wrong_field] = wrong_value

        with allure.step('Отправляем запрос на авторизацию для пользователя с неверными данными авторизации'):
            response = user_methods.login_user(login_payload)
            
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 401, 'Ожидался код 401, получен {status_code}. Ответ: {response.text}'
                                            
        with allure.step('Проверяем тело ответа'):
            response_data = response.json()
            assert response_data.get("success") is False, f"Поле success должно быть False: {response_data}"
            assert response_data.get("message") == ERROR_INVALID_CREDENTIALS, (
                f"Ожидалось сообщение '{ERROR_INVALID_CREDENTIALS}', "
                f"получено: '{response_data.get('message')}'"
            )