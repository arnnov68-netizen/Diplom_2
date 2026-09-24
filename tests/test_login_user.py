import allure
from helpers.api_helpers import login_user
from data.test_data import TestData


@allure.epic("Пользователь")
@allure.feature("Авторизация")
class TestLoginUser:

    @allure.story("Успешный вход")
    @allure.title("Вход существующего пользователя")
    @allure.description("Проверка успешного входа зарегистрированного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user(self, registered_user):
        user_data = registered_user['user_data']
        login_data = {
            "email": user_data['email'],
            "password": user_data['password']
        }

        response = login_user(login_data)

        with allure.step("Проверка статуса ответа 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        data = response.json()
        with allure.step("Проверка данных ответа"):
            assert data['success'] is True
            assert 'accessToken' in data, "Отсутствует accessToken"
            assert 'refreshToken' in data, "Отсутствует refreshToken"
            assert 'user' in data, "Отсутствуют данные пользователя"
            assert data['user']['email'] == user_data['email']
            assert data['user']['name'] == user_data['name']

        with allure.step("Проверка формата токена"):
            assert data['accessToken'].startswith('Bearer '), "Неверный формат accessToken"

    @allure.story("Ошибки входа")
    @allure.title("Вход с неверным логином")
    @allure.description("Проверка, что при неверном логине возвращается ошибка 401")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_email(self, registered_user):
        user_data = registered_user['user_data']
        login_data = {
            "email": "wrong_email@example.com",
            "password": user_data['password']
        }

        response = login_user(login_data)

        with allure.step("Проверка статуса ответа 401"):
            assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

        data = response.json()
        with allure.step("Проверка сообщения об ошибке"):
            assert data['success'] is False
            assert data['message'] in [
                TestData.ERROR_MESSAGES['LOGIN_FAILED'],
                TestData.ERROR_MESSAGES['INCORRECT_CREDENTIALS']
            ]

    @allure.story("Ошибки входа")
    @allure.title("Вход с неверным паролем")
    @allure.description("Проверка, что при неверном пароле возвращается ошибка 401")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, registered_user):
        user_data = registered_user['user_data']
        login_data = {
            "email": user_data['email'],
            "password": "wrong_password_12345"
        }

        response = login_user(login_data)

        with allure.step("Проверка статуса ответа 401"):
            assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

        data = response.json()
        with allure.step("Проверка сообщения об ошибке"):
            assert data['success'] is False
            assert data['message'] in [
                TestData.ERROR_MESSAGES['LOGIN_FAILED'],
                TestData.ERROR_MESSAGES['INCORRECT_CREDENTIALS']
            ]

    @allure.story("Ошибки входа")
    @allure.title("Вход без пароля")
    @allure.description("Проверка, что при отсутствии пароля возвращается ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_missing_password(self, registered_user):
        user_data = registered_user['user_data']
        login_data = {
            "email": user_data['email']
        }

        response = login_user(login_data)

        with allure.step("Проверка статуса ответа 401"):
            assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

    @allure.story("Ошибки входа")
    @allure.title("Вход несуществующего пользователя")
    @allure.description("Проверка, что при входе несуществующего пользователя возвращается ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_nonexistent_user(self):
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }

        response = login_user(login_data)

        with allure.step("Проверка статуса ответа 401"):
            assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

        data = response.json()
        with allure.step("Проверка сообщения об ошибке"):
            assert data['success'] is False
            assert data['message'] in [
                TestData.ERROR_MESSAGES['LOGIN_FAILED'],
                TestData.ERROR_MESSAGES['INCORRECT_CREDENTIALS']
            ]