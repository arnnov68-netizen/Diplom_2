### Чистый Allure-отчёт

`pytest-randomly` дописывает значения параметров в имя теста, из-за чего
в заголовках параметризованных кейсов появляется «шум». Чтобы получить
чистые заголовки в Allure, запускайте без случайного порядка:

```bash
pytest -p no:randomly --alluredir=allure-results --clean-alluredir
allure serve allure-results