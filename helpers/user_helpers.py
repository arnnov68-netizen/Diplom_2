import uuid

import requests

from data.config import BASE_URL


def generate_user_data():
    """Генерирует уникальные данные пользователя."""
    unique = uuid.uuid4().hex[:8]
    return {
        "email": f"test_{unique}@example.com",
        "password": "TestPass123!",
        "name": f"Test User {unique}",
    }


def register_user(user_data=None):
    """Регистрирует пользователя через API.
    Возвращает полный ответ регистрации + user_data.
    Бросает RuntimeError, если регистрация не удалась.
    """
    if user_data is None:
        user_data = generate_user_data()

    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)

    if response.status_code == 403:
        user_data = generate_user_data()
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)

    if response.status_code != 200:
        raise RuntimeError(
            f"Не удалось зарегистрировать пользователя: "
            f"status={response.status_code}, body={response.text}"
        )

    result = response.json()
    result['user_data'] = user_data
    return result