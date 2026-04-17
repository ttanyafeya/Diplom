import requests
import json
import allure
from Tests.constants import API2_url, bearer_token


@allure.title("Класс для удаления товара из корзины")
class DeleteFromCart:
    """
    Класс для работы с удалением товаров из корзины.
    """

    @allure.step("Инициализация класса DeleteFromCart")
    def __init__(self, url):
        """
        Создает объект для работы с корзиной.

        :param url: URL для работы с корзиной.
        """
        self.url = url
        self.headers = {
            'Content-Type': 'application/json',  # Указываем, что отправляем JSON
            'Authorization': bearer_token  # Токен для авторизации
        }

    @allure.step("Получение содержимого корзины")
    def get_cart_contents(self) -> tuple:
        """
        Получает содержимое корзины.

        :return: Кортеж (статус-код, содержимое корзины в формате JSON).
        """
        # Отправляем GET-запрос для получения содержимого корзины
        response = requests.get(self.url, headers=self.headers)

        # Пытаемся распарсить ответ как JSON
        try:
            cart_data = response.json()
        except json.JSONDecodeError:
            cart_data = response.text

        return response.status_code, cart_data  # Возвращаем статус-код и данные корзины

    @allure.step("Удаление товара из корзины")
    def delete_product_from_cart(self, prod_id: int) -> int:
        """
        Удаляет товар из корзины.

        :param prod_id: ID товара, который нужно удалить.
        :return: Статус-код ответа от сервера.
        """
        # Формируем тело запроса в правильном формате
        payload = {
            "productId": prod_id
        }

        # Отправляем DELETE-запрос для удаления товара из корзины
        response = requests.delete(self.url, headers=self.headers, data=json.dumps(payload))
        return response.status_code  # Возвращаем статус-код ответа