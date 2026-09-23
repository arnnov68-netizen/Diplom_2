import allure
import pytest
from helpers.api_helpers import create_order
from data.test_data import TestData


@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Авторизованные заказы")
    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Проверка создания заказа авторизованным пользователем с корректными ингредиентами")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_auth(self, auth_token, ingredient_ids):
        response = create_order(ingredient_ids, auth_token)

        with allure.step("Проверка статуса ответа 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        data = response.json()
        with allure.step("Проверка данных заказа"):
            assert data['success'] is True
            assert 'order' in data
            assert 'number' in data['order']
            assert data['order']['number'] > 0
            assert 'name' in data
            assert len(data['name']) > 0

    @allure.story("Неавторизованные заказы")
    @allure.title("Создание заказа неавторизованным пользователем")
    @allure.description("Проверка, что неавторизованный пользователь может создать заказ")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_auth(self, ingredient_ids):
        response = create_order(ingredient_ids)

        with allure.step("Проверка статуса ответа 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        data = response.json()
        with allure.step("Проверка данных заказа"):
            assert data['success'] is True
            assert 'order' in data
            assert 'number' in data['order']
            assert data['order']['number'] > 0

    @allure.story("Ошибки создания заказа")
    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Проверка, что при создании заказа без ингредиентов возвращается ошибка 400")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_without_ingredients(self, auth_token):
        response = create_order([], auth_token)

        with allure.step("Проверка статуса ответа 400"):
            assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

        data = response.json()
        with allure.step("Проверка сообщения об ошибке"):
            assert data['success'] is False
            assert data['message'] == TestData.ERROR_MESSAGES['INGREDIENTS_REQUIRED']

    @allure.story("Ошибки создания заказа")
    @allure.title("Создание заказа с невалидным хешем ингредиента")
    @allure.description("Проверка, что при передаче невалидного хеша возвращается ошибка 500")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_invalid_hash(self, auth_token):
        invalid_ingredients = [TestData.INVALID_INGREDIENT_HASH]
        response = create_order(invalid_ingredients, auth_token)

        with allure.step("Проверка статуса ответа 500"):
            assert response.status_code == 500, f"Ожидался статус 500, получен {response.status_code}"

    @allure.story("Ошибки создания заказа")
    @allure.title("Создание заказа с частично неверным хешем")
    @allure.description("Проверка, что при наличии хотя бы одного невалидного хеша возвращается ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_mixed_hash(self, auth_token, ingredient_ids):
        invalid_ingredients = [ingredient_ids[0], TestData.INVALID_INGREDIENT_HASH]
        response = create_order(invalid_ingredients, auth_token)

        with allure.step("Проверка статуса ответа 500"):
            assert response.status_code == 500, f"Ожидался статус 500, получен {response.status_code}"

    @allure.story("Ошибки создания заказа")
    @allure.title("Создание заказа с неверным токеном авторизации")
    @allure.description("Проверка, что при неверном токене авторизации заказ не создается")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_invalid_token(self, ingredient_ids):
        invalid_token = "Bearer invalid_token_12345"
        response = create_order(ingredient_ids, invalid_token)

        with allure.step("Проверка статуса ответа 401 или 403"):
            assert response.status_code in [401, 403], f"Ожидался статус 401 или 403, получен {response.status_code}"

    @allure.story("Создание заказа")
    @allure.title("Создание нескольких заказов подряд")
    @allure.description("Проверка возможности создания нескольких заказов")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_multiple_orders(self, auth_token, ingredient_ids):
        order_numbers = []
        for i in range(3):
            response = create_order(ingredient_ids, auth_token)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            order_numbers.append(data['order']['number'])

        with allure.step("Проверка, что заказы имеют разные номера"):
            assert len(set(order_numbers)) == 3, "Номера заказов должны быть уникальными"