import allure
from data import ERROR_UNAUTHORIZED


class TestGetOrders:
    
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, authorized_user, created_order, order_methods):   

        token = authorized_user['token']
        created_order_number = created_order['order_number']
        
        with allure.step('Получаем заказы пользователя'):
            response = order_methods.get_user_orders(token=token)
            
        with allure.step('Проверяем статус код'):
            assert response.status_code == 200, f'Ожидался код 200, получен {response.status_code}. Ответ: {response.text}'
            
        with allure.step('Проверяем тело ответа'):
            response_data = response.json()
            assert response_data.get("success") is True, f"Поле success должно быть True: {response_data}"
            assert "orders" in response_data, f"В ответе должен быть список 'orders': {response_data}"
            
            orders = response_data["orders"]
            assert isinstance(orders, list), f"orders должен быть списком: {type(orders)}"
            assert len(orders) > 0, f"В списке заказов должен быть хотя бы один заказ: {orders}"
            
            order_numbers = [order["number"] for order in orders]
            assert created_order_number in order_numbers, f"Созданный заказ {created_order_number})не найден в списке: {order_numbers}"


    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_without_auth(self, order_methods):

        with allure.step('Получаем заказы без авторизации'):
            response = order_methods.get_user_orders()
            
        with allure.step('Проверяем статус код'):
            assert response.status_code == 401, f'Ожидался код 401, получен {response.status_code}. Ответ: {response.text}'
            
        with allure.step('Проверяем тело ответа с ошибкой'):
            response_data = response.json()
            assert response_data.get("success") is False, f"Поле success должно быть False: {response_data}"
            assert response_data.get("message") == ERROR_UNAUTHORIZED, (
                f"Ожидалось сообщение '{ERROR_UNAUTHORIZED}', "
                f"получено: '{response_data.get('message')}'"
                )
            