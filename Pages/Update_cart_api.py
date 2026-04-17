import json
import requests
import allure
from Tests.constants import API2_url, bearer_token

url = API2_url  # URL для работы с корзиной
token = bearer_token

@allure.description("Тестирование обновления корзины на сайте Читай-город.")
class UpdateCartAPI:
    """
    Класс для работы с API обновления корзины на сайте Читай-город.

    Атрибуты:
        url (str): URL для работы с корзиной.
        Headers (dict): Заголовки запроса, включая авторизацию.
    """

    def __init__(self, url):
        """
        Инициализация класса UpdateCartAPI.

        :param url: URL, используемый для работы с корзиной.
        """
        self.url = url
        self.headers = {
            'Content-Type': 'application/json',  # Установка типа содержимого для JSON
            'Authorization': bearer_token  # Авторизационный токен для доступа к API
        }

    @allure.step("Обновление содержимого корзины")
    def update_cart(self, items: list) -> tuple:
        """
        Отправляет PUT-запрос для редактирования корзины.

        :param items: Список с товарами и их количеством для обновления корзины.
        Пример формата:
        [{"id": 1, "quantity": 2}, {"id": 2, "quantity": 1}]
        :return: Кортеж, содержащий статус-код ответа (int) и данные ответа от сервера (dict).
        """
        # Формируем тело запроса в правильном формате
        payload = {
            "items": items
        }

        # Отправляем PUT-запрос для редактирования корзины
        response = requests.put(self.url, headers=self.headers, data=json.dumps(payload))

        # Пытаемся расписать ответ как JSON
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            response_data = response.text

        return response.status_code, response_data  # Возвращаем статус-код и данные ответа



