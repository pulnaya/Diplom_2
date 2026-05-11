import allure
from data import ERROR_MISSING_INGREDIENTS


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, authorized_user, order_ingredients, order_methods):
        
        token = authorized_user['token'] 
        ingredients = order_ingredients[:2]
        order_payload = {"ingredients": ingredients}

        with allure.step('Создаем заказ с авторизацией'):
            response = order_methods.create_order(order_payload, token=token)

        with allure.step('Проверяем статус код'):
            assert response.status_code == 200, f'Ожидался код 200, получен {response.status_code}.'

        with allure.step('Проверяем тело ответа'):
            response_data = response.json()
            assert response_data.get("success") is True, f"Поле success должно быть True: {response_data}"
            assert "name" in response_data, f"В ответе должно быть название заказа: {response_data}"
            assert "order" in response_data, f"В ответе должен быть объект 'order': {response_data}"
            assert "number" in response_data["order"], f"В заказе должен быть номер: : {response_data}"


    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, order_ingredients, order_methods):

        ingredients = order_ingredients[:2]
        order_payload = {"ingredients": ingredients}
        
        with allure.step('Создаем заказ без авторизации'):
            response = order_methods.create_order(order_payload)
            
        with allure.step('Проверяем статус код'):
            assert response.status_code == 200, f'Ожидался код 200, получен {response.status_code}. Ответ: {response.text}'
            
        with allure.step('Проверяем тело ответа'):
            response_data = response.json()
            assert response_data.get("success") is True, f"Поле success должно быть True: {response_data}"
            assert "name" in response_data, f"В ответе должно быть название заказа: {response_data}"
            assert "order" in response_data, f"В ответе должен быть объект 'order': {response_data}"
            assert "number" in response_data["order"], f"В заказе должен быть номер: {response_data}"
                    
    
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, order_methods):
    
        order_payload = {"ingredients": []}
        
        with allure.step('Создаем заказ с пустым списком ингредиентов'):
            response = order_methods.create_order(order_payload)
            
        with allure.step('Проверяем статус код'):
            assert response.status_code == 400, f'Ожидался код 400, получен {response.status_code}. Ответ: {response.text}'
            
        with allure.step('Проверяем тело ответа с ошибкой'):
            response_data = response.json()
            assert response_data.get("success") is False, f"Поле success должно быть False: {response_data}"
            assert response_data.get("message") == ERROR_MISSING_INGREDIENTS, f"Неправильное сообщение об ошибке: {response_data['message']}"
    

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, order_methods):
        
        order_payload = {"ingredients": ["invalid_ingridient_id_1", "invalid_ingridient_id_2"]}
        
        with allure.step('Создаем заказ с неверными ID ингредиентов'):
            response = order_methods.create_order(order_payload)
            
        with allure.step('Проверяем статус код'):
            assert response.status_code == 500, f'Ожидался код 500, получен {response.status_code}. Ответ: {response.text}'
