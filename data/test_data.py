# Тестовые данные для API тестов

class TestData:
    INVALID_INGREDIENT_HASH = "invalid_hash_12345"

    ERROR_MESSAGES = {
        "USER_EXISTS": "User already exists",
        "REQUIRED_FIELDS": "Email, password and name are required fields",
        "INGREDIENTS_REQUIRED": "Ingredient ids must be provided",
        "LOGIN_FAILED": "email or password are incorrect",
        "INCORRECT_CREDENTIALS": "email or password are incorrect",
    }

    # Маркер текста ответа при 500 — сервис отдаёт HTML/строку,
    # поэтому проверяем вхождение подстроки, а не точное равенство.
    INTERNAL_SERVER_ERROR_MARKER = "Internal Server Error"