import requests
import json
import allure
from Tests.constants import API1_url
from Tests.constants import API2_url
from Tests.constants import bearer_token


@allure.description("Тестирование добавления товара в корзину на сайте Читай-город.")
class WrongRequestAPI:
    """
                Класс для тестирования некорректных запросов к API добавления товара в корзину
                на сайте Читай-город.
    """

    url = API1_url
    url_2 = API2_url

    def __init__(self, url: str):
        """
                Инициализация класса WrongRequestAPI.

                :param url: URL API для выполнения запросов.
        """
        self.url = url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': bearer_token
        }

    def wrong_add_product(self, product_id: int, item_list_name: str) -> requests.Response:
        """
                 Отправляет некорректный запрос для добавления товара в корзину с указанным product_id
                и именем списка товаров.

                :param product_id: Идентификатор товара, который нужно добавить в корзину.
                :param item_list_name: Название списка товаров.

                :return: Статус код ответа от API.
        """
        payload = {
            "id": product_id,
            "adData": {
                "item_list_name": item_list_name,
            }
        }
        resp = requests.patch(self.url, headers=self.headers, data=json.dumps(payload))
        return resp.Response
