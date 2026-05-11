import requests
import allure
from urls import BASE_URL, REGISTRATION_URL, LOGIN_URL, USER_URL, LOGOUT_URL, TOKEN_URL


class UserMethods:
    def __init__(self):
        self.base_url = BASE_URL
        self.registration_url = REGISTRATION_URL
        self.login_url = LOGIN_URL
        self.logout_url = LOGOUT_URL
        self.user_url = USER_URL
        self.token_url = TOKEN_URL

    @allure.step('Создать пользователя')
    def create_user(self, payload):
        response = requests.post(
            f"{self.base_url}{self.registration_url}", 
            json=payload 
        )
        return response
    
    @allure.step('Удалить пользователя')
    def delete_user(self, token):
        """Удаление пользователя по токену"""
        headers = {"Authorization": f"{token}"}
        response = requests.delete(
            f"{self.base_url}{self.user_url}",
            headers=headers
        )
        return response
    
    @allure.step('Авторизовать пользователя')
    def login_user(self, payload):
        response = requests.post(
            f"{self.base_url}{self.login_url}", 
            json=payload
        )
        return response
    
    @allure.step('Выйти из системы')
    def logout_user(self, payload):
        response = requests.post(
            f"{self.base_url}{self.logout_url}", 
            json=payload
        )
        return response
    
    @allure.step('Обновить информацию о пользователе')
    def update_user_info(self, payload, token):
        headers = {"Authorization": token}
        response = requests.patch(
            f"{self.base_url}{self.user_url}", 
            headers=headers,
            json=payload
        )
        return response