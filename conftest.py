# conftest.py
import pytest

from helpers.api_helpers import delete_user, get_ingredients
from helpers.user_helpers import generate_user_data, register_user


@pytest.fixture
def random_user_data():
    """Уникальные данные пользователя — генерируются хелпером."""
    return generate_user_data()


@pytest.fixture
def registered_user(random_user_data):
    """Регистрирует пользователя и удаляет его после теста."""
    data = register_user(random_user_data)

    yield data

    access = data.get('accessToken')
    if access:
        try:
            delete_user(access)
        except Exception:
            pass


@pytest.fixture
def auth_token(registered_user):
    return registered_user['accessToken']


@pytest.fixture
def ingredient_ids():
    """Гарантированно возвращает минимум 2 ID ингредиентов."""
    response = get_ingredients()
    if response.status_code == 200:
        data = response.json()
        if data.get('success') and data.get('data'):
            return [ing['_id'] for ing in data['data'][:2] if '_id' in ing]
    return ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]


@pytest.fixture
def cleanup_users():
    """Собирает токены созданных в тесте пользователей и удаляет их после.

    Использование в тесте:
        def test_...(..., cleanup_users):
            response = create_user(...)
            cleanup_users.append(response.json()['accessToken'])
    """
    tokens = []
    yield tokens

    for token in tokens:
        try:
            delete_user(token)
        except Exception:
            pass