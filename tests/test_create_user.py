import allure
import pytest
from helpers.api_helpers import create_user
from data.test_data import TestData


@allure.epic("Пользователь")
@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.story("Успешное создание")
    @allure.title("Создание уникального пользователя")
    @allure.description("Проверка успешного создания нового пользователя с уникальными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user(self, random_user_data):
        response = create_user(random_user_data)

        with allure.step("Проверка статуса ответа 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        data = response.json()
        with allure.step("Проверка структуры ответа"):
            assert data['success'] is True
            assert 'accessToken' in data, "Отсутствует accessToken"
            assert 'refreshToken' in data, "Отсутствует refreshToken"
            assert 'user' in data, "Отсутствуют данные пользователя"
            assert data['user']['email'] == random_user_data['email']
            assert data['user']['name'] == random_user_data['name']
            assert 'password' not in data['user'], "Пароль не должен возвращаться"

        with allure.step("Проверка формата токенов"):
            assert data['accessToken'].startswith('Bearer '), "Неверный формат accessToken"
            assert len(data['refreshToken']) > 0, "refreshToken пустой"

    @allure.story("Ошибки создания")
    @allure.title("Создание существующего пользователя")
    @allure.description("Проверка, что при попытке создать существующего пользователя возвращается ошибка 403")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_existing_user(self, registered_user):
        user_data = registered_user['user_data']
        response = create_user(user_data)

        with allure.step("Проверка статуса ответа 403"):
            assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"

        data = response.json()
        with allure.step("Проверка сообщения об ошибке"):
            assert data['success'] is False
            assert data['message'] == TestData.ERROR_MESSAGES['USER_EXISTS']

    @allure.story("Ошибки создания")
    @allure.title("Создание пользователя без обязательных полей")
    @allure.description("Проверка, что при отсутствии обязательных полей возвращается ошибка 403")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", [
        'email',
        'password',
        'name'
    ], ids=["без email", "без password", "без name"])
    def test_create_user_missing_fields(self, random_user_data, missing_field):
        invalid_data = random_user_data.copy()
        invalid_data.pop(missing_field)

        response = create_user(invalid_data)

        with allure.step(f"Проверка статуса ответа 403 при отсутствии поля {missing_field}"):
            assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"

        data = response.json()
        with allure.step("Проверка сообщения об ошибке"):
            assert data['success'] is False
            assert data['message'] == TestData.ERROR_MESSAGES['REQUIRED_FIELDS']

    @allure.story("Ошибки создания")
    @allure.title("Создание пользователя с пустыми полями")
    @allure.description("Проверка, что при пустых обязательных полях возвращается ошибка")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_empty_fields(self):
        user_data = {
            "email": "",
            "password": "",
            "name": ""
        }
        response = create_user(user_data)

        with allure.step("Проверка статуса ответа 403"):
            assert response.status_code == 403