import pytest
import uuid

from faker import Faker

from helpers.api_helpers import (
    BASE_URL,
    create_user,
    logout_user,
    get_ingredients,
)

fake = Faker()


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
    response = create_user(random_user_data)

    if response.status_code != 200:
        # Это ошибка подготовки данных, а не провал теста.
        raise RuntimeError(
            f"Не удалось создать пользователя для теста: "
            f"status={response.status_code}, body={response.text}"
        )

    data = response.json()
    data['user_data'] = random_user_data

    yield data

    # Teardown — logout
    refresh = data.get('refreshToken')
    if refresh:
        try:
            logout_user(refresh)
        except Exception:
            pass


@pytest.fixture
def auth_token(registered_user):
    """Возвращает accessToken зарегистрированного пользователя."""
    return registered_user['accessToken']


@pytest.fixture
def ingredient_ids():
    """Гарантированно возвращает минимум 2 ID ингредиентов."""
    response = get_ingredients()

    if response.status_code == 200:
        data = response.json()
        if data.get('success') and data.get('data'):
            ingredients = data['data'][:2]
            ids = [ing['_id'] for ing in ingredients if '_id' in ing]
            if ids:
                return ids

    # Запасной вариант, если API недоступно.
    return ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]