import requests
import allure
from urls import BASE_URL, ORDERS_URL, INGREDIENTS_URL



class OrderMethods:
    def __init__(self):
        self.base_url = BASE_URL
        self.orders_url = ORDERS_URL
        self.ingredients_url = INGREDIENTS_URL
    
    @allure.step('Создать заказ')
    def create_order(self, payload, token=None):
        headers = {}
        if token:
            headers["Authorization"] = token
        
        response = requests.post(
            f"{self.base_url}{self.orders_url}",
            headers=headers,
            json=payload
        )
        return response
    
    @allure.step('Получить список ингредиентов')
    def get_ingredients(self):
        response = requests.get(f"{self.base_url}{self.ingredients_url}")
        return response

    @allure.step('Получить заказы пользователя')
    def get_user_orders(self, token=None):
        headers = {}
        if token:
            headers["Authorization"] = token

        response = requests.get(
            f"{self.base_url}{self.orders_url}",
            headers=headers
        )
        return response