import pytest
import requests
from faker import Faker
import allure

fake = Faker()

BASE_URL = "https://stellarburgers.education-services.ru/api"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def random_user_data():
    """Генерирует случайные данные пользователя"""
    return {
        "email": fake.email(),
        "password": fake.password(length=10, special_chars=False),
        "name": fake.name()
    }


@pytest.fixture
def registered_user(random_user_data):
    """Создает и возвращает зарегистрированного пользователя"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=random_user_data
    )

    if response.status_code == 200:
        data = response.json()
        data['user_data'] = random_user_data
        return data
    else:
        # Если не удалось создать пользователя, возвращаем None
        # и выводим информацию об ошибке
        print(f"Failed to create user: {response.status_code} - {response.text}")
        return None


@pytest.fixture
def auth_token(registered_user):
    """Возвращает токен авторизации"""
    if registered_user and 'accessToken' in registered_user:
        return registered_user['accessToken']
    return None


@pytest.fixture
def ingredient_ids():
    """Возвращает список ID ингредиентов для заказа"""
    try:
        response = requests.get(f"{BASE_URL}/ingredients")
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'data' in data:
                ingredients = data['data'][:2]
                return [ing['_id'] for ing in ingredients if '_id' in ing]
    except Exception as e:
        print(f"Error getting ingredients: {e}")

    # Fallback IDs из документации
    return ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]


@pytest.fixture
def created_user_with_cleanup(random_user_data):
    """Создает пользователя и автоматически удаляет его после теста"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=random_user_data
    )

    user_data = None
    if response.status_code == 200:
        data = response.json()
        data['user_data'] = random_user_data
        user_data = data

    yield user_data

    # Очистка после теста (если есть API для удаления пользователя)
    if user_data and 'refreshToken' in user_data:
        try:
            # Выход из системы
            requests.post(
                f"{BASE_URL}/auth/logout",
                json={"token": user_data['refreshToken']}
            )
        except:
            pass