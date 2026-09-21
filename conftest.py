import pytest
import requests
import uuid
from faker import Faker

fake = Faker()

BASE_URL = "https://stellarburgers.education-services.ru/api"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def random_user_data():
    """Уникальные данные пользователя."""
    unique = uuid.uuid4().hex[:8]
    return {
        "email": f"test_{unique}@example.com",
        "password": "TestPass123!",
        "name": f"Test User {unique}"
    }


@pytest.fixture
def registered_user(random_user_data):
    """Создаёт пользователя и удаляет его (через logout) после теста."""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=random_user_data
    )
    assert response.status_code == 200, \
        f"Не удалось создать пользователя: {response.text}"
    
    data = response.json()
    data['user_data'] = random_user_data
    
    yield data
    
    # Teardown — logout
    refresh_token = data.get('refreshToken')
    if refresh_token:
        try:
            requests.post(
                f"{BASE_URL}/auth/logout",
                json={"token": refresh_token}
            )
        except Exception:
            pass


@pytest.fixture
def auth_token(registered_user):
    """Возвращает accessToken зарегистрированного пользователя."""
    return registered_user['accessToken']


@pytest.fixture
def ingredient_ids():
    """Возвращает список ID ингредиентов."""
    response = requests.get(f"{BASE_URL}/ingredients")
    if response.status_code == 200:
        data = response.json()
        if data.get('success') and 'data' in data:
            ingredients = data['data'][:2]
            return [ing['_id'] for ing in ingredients if '_id' in ing]
    return ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]
