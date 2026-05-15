import allure
import pytest
from data import ERROR_UNAUTHORIZED 

class TestUserUpdate:
    
    @allure.title("Изменение данных пользователя с авторизацией")
    @pytest.mark.parametrize("field_to_update,new_value", [
        ("name", "НовоеИмя_Тест"),
        ("email", "new_email_test@example.com"),
    ])
    def test_update_user_with_auth(self, create_user, user_methods, field_to_update, new_value):

        user_data = create_user
        token = user_data["token"]
        update_payload = {field_to_update: new_value}
        
        with allure.step(f'Изменяем поле {field_to_update} на значение "{new_value}"'):
            response = user_methods.update_user_info(update_payload, token)
            
        with allure.step('Проверяем статус код ответа'):
            status_code = response.status_code
            assert status_code == 200, f'Ожидался код 200, получен {status_code}. Ответ: {response.text}'
            
        with allure.step('Проверяем тело ответа'):
            response_data = response.json()
            assert response_data.get("success") is True, f"Поле success должно быть True: {response_data}"
            
            updated_user = response_data.get("user", {})
            assert updated_user.get(field_to_update) == new_value, (
                f"Поле {field_to_update} не обновилось. "
                f"Ожидалось: {new_value}, получено: {updated_user.get(field_to_update)}"
            )

     
    @allure.title("Изменение данных пользователя без авторизации")
    @pytest.mark.parametrize("field_to_update,new_value", [
        ("name", "НовоеИмя_БезАвторизации"),
        ("email", "unauthorized_change@example.com"),
    ])
    def test_update_user_without_auth(self, user_methods, field_to_update, new_value):
        update_payload = {field_to_update: new_value}
        
        with allure.step(f'Пытаемся изменить поле {field_to_update} без авторизации'):
            response = user_methods.update_user_info(update_payload, token=None)
            
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 401, f'Ожидался код 401, получен {status_code}. Ответ: {response.text}'
        
        with allure.step('Проверяем тело ответа'):
            response_data = response.json()
            assert response_data.get("success") is False, f"Поле success должно быть False: {response_data}"
            assert response_data.get("message") == ERROR_UNAUTHORIZED, (
                f"Ожидалось сообщение '{ERROR_UNAUTHORIZED}', "
                f"получено: '{response_data.get('message')}'"
            )