import allure
import requests

from data.config import BASE_URL


@allure.step("POST /auth/register — регистрация пользователя")
def create_user(user_data):
    return requests.post(f"{BASE_URL}/auth/register", json=user_data)


@allure.step("POST /auth/login — авторизация пользователя")
def login_user(login_data):
    return requests.post(f"{BASE_URL}/auth/login", json=login_data)


@allure.step("DELETE /auth/user — удаление пользователя")
def delete_user(access_token):
    headers = {"Authorization": access_token}
    return requests.delete(f"{BASE_URL}/auth/user", headers=headers)


@allure.step("POST /orders — создание заказа")
def create_order(ingredients, token=None):
    headers = {}
    if token:
        headers['Authorization'] = token
    return requests.post(
        f"{BASE_URL}/orders",
        json={"ingredients": ingredients},
        headers=headers
    )


@allure.step("GET /ingredients — получение списка ингредиентов")
def get_ingredients():
    return requests.get(f"{BASE_URL}/ingredients")