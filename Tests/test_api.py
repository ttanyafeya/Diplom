import allure
import requests
import pytest

from Tests.constants import bearer_token
from Tests.constants import API3_url

base_url = API3_url
token = bearer_token


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.story("Поиск по ключевым словам")
@allure.title("Поиск книги по названию")
@allure.description("Тест проверяет успешный поиск книги по названию")
@allure.severity(allure.severity_level.CRITICAL)
def test_search():
    with allure.step("Подготовка тестовых данных"):
        book = "запах смерти"
        param_q = {"phrase": f"{book}"}
        my_headers = {"authorization": f"Bearer {token}"}

    with allure.step(f"Выполнение GET запроса "
                     f"к /search/product с параметром phrase={book}"):
        res = requests.get(url=f"{base_url}/search/product",
                           params=param_q, headers=my_headers)

    with allure.step("Проверка статус кода ответа"):
        assert res.status_code == 200
        allure.attach(str(res.status_code),
                      "Status Code", allure.attachment_type.TEXT)

    with allure.step("Проверка наличия названия книги в ответе"):
        data = res.json()
        title = data['data']['attributes']['seo']['title']
        assert book in title
        allure.attach(title, "Заголовок страницы",
                      allure.attachment_type.TEXT)


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.story("Поиск по цифрам")
@allure.title("Поиск по фразе, состоящей из цифр")
@allure.description("Тест проверяет поиск книг по цифровой фразе")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_numbers():
    with allure.step("Подготовка тестовых данных"):
        search_phrase = "1984"
        param_q = {"phrase": search_phrase}
        my_headers = {"authorization": f"Bearer {token}"}

    with allure.step(f"Выполнение GET запроса "
                     f"с цифровой фразой: {search_phrase}"):
        res = requests.get(url=f"{base_url}/search/product",
                           params=param_q, headers=my_headers)

    with allure.step("Проверка статус кода ответа"):
        assert res.status_code == 200
        allure.attach(str(res.status_code),
                      "Status Code", allure.attachment_type.TEXT)

    with allure.step("Проверка, что ответ содержит данные"):
        data = res.json()
        assert 'data' in data
        allure.attach(f"Найдено результатов:"
                      f" {len(data.get('data', []))}",
                      "Results count", allure.attachment_type.TEXT)


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.story("Поиск с пустой фразой")
@allure.title("Поиск по пустой фразе")
@allure.description("Тест проверяет поведение системы"
                    " при поиске с пустой строкой")
@allure.severity(allure.severity_level.NORMAL)
def test_search_empty_phrase():
    with allure.step("Подготовка тестовых данных"):
        search_phrase = ""
        param_q = {"phrase": search_phrase}
        my_headers = {"authorization": f"Bearer {token}"}

    with allure.step("Выполнение GET запроса с пустой фразой"):
        res = requests.get(url=f"{base_url}/search/product",
                           params=param_q, headers=my_headers)

    with allure.step("Проверка статус кода ответа"):
        allure.attach(str(res.status_code),
                      "Status Code", allure.attachment_type.TEXT)
        allure.attach(str(res.text), "Response Body",
                      allure.attachment_type.TEXT)
        # Ожидаем либо 200, либо 400 (Bad Request)
        assert res.status_code in [200, 400]


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.story("Поиск без авторизации")
@allure.title("Поиск без авторизации")
@allure.description("Тест проверяет доступность поиска"
                    " без токена авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_without_auth():
    with allure.step("Подготовка тестовых данных"):
        search_phrase = "война и мир"
        param_q = {"phrase": search_phrase}

    with allure.step("Выполнение GET запроса "
                     "без заголовка авторизации"):
        res = requests.get(url=f"{base_url}/search/product", params=param_q)

    with allure.step("Проверка статус кода ответа"):
        allure.attach(str(res.status_code), "Status Code",
                      allure.attachment_type.TEXT)

        if res.status_code == 200:
            allure.attach("Поиск доступен без авторизации",
                          "Result", allure.attachment_type.TEXT)
            data = res.json()
            assert 'data' in data
        elif res.status_code == 401:
            allure.attach("Требуется авторизация",
                          "Result", allure.attachment_type.TEXT)
            assert 'error' in res.json() or 'message' in res.text
        else:
            pytest.fail(f"Неожиданный статус код:"
                        f" {res.status_code}")


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.story("Поиск по несуществующей фразе")
@allure.title("Поиск по несуществующей фразе")
@allure.description("Тест проверяет поиск по фразе,"
                    " которая не существует в каталоге")
@allure.severity(allure.severity_level.NORMAL)
def test_search_nonexistent_phrase():
    with allure.step("Подготовка тестовых данных"):
        search_phrase = "этого_слова_точно_нет_в_каталоге_123456789"
        param_q = {"phrase": search_phrase}
        my_headers = {"authorization": f"Bearer {token}"}

    with allure.step(f"Выполнение GET запроса "
                     f"с несуществующей фразой: {search_phrase}"):
        res = requests.get(url=f"{base_url}/search/product",
                           params=param_q, headers=my_headers)

    with allure.step("Проверка статус кода ответа"):
        assert res.status_code == 200
        allure.attach(str(res.status_code),
                      "Status Code", allure.attachment_type.TEXT)

    with allure.step("Проверка, что запрос выполнен успешно"):
        data = res.json()
        allure.attach("API вернул успешный ответ",
                      "Result", allure.attachment_type.TEXT)

        # Базовая проверка - просто убеждаемся, что ответ не содержит ошибок
        if 'errors' in data:
            allure.attach(str(data['errors']),
                          "Errors found", allure.attachment_type.TEXT)
            assert False, f"API вернул ошибки: {data['errors']}"


# Если нужно запустить все тесты вместе
if __name__ == "__main__":
    pytest.main([__file__, "--alluredir=allure-results", "-v"])

# # Установка необходимых пакетов
# pip install allure-pytest pytest requests
#
# # Запуск тестов с сохранением результатов Allure
# pytest test_api.py --alluredir=allure-results -v
#
# # Генерация и открытие Allure отчета
# allure generate allure-results -o allure-report --clean
# allure open allure-report
