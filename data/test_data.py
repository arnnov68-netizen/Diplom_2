# Тестовые данные для API тестов

class TestData:
    INVALID_INGREDIENT_HASH = "invalid_hash_12345"

    ERROR_MESSAGES = {
        "USER_EXISTS": "User already exists",
        "REQUIRED_FIELDS": "Email, password and name are required fields",
        "INGREDIENTS_REQUIRED": "Ingredient ids must be provided",
        "UNAUTHORIZED": "You should be authorised",
        "LOGIN_FAILED": "email or password are incorrect",
        "INCORRECT_CREDENTIALS": "email or password are incorrect"
    }

    # Тестовые пользователи
    TEST_USER = {
        "email": "testuser@example.com",
        "password": "TestPassword123",
        "name": "Test User"
    }