import allure
import pytest
from Pages.Add_To_Cart_api import AddToCartAPI
from Pages.Wrong_Add_To_Cart_api import WrongRequestAPI
from constants import API1_url
from constants import API2_url
from Pages.Update_cart_api import UpdateCartAPI
from Pages.Delete_From_Cart_api import DeleteFromCart
from Pages.Send_Empty_Post_Request_api import EmptyPostRequest


@allure.feature("Тестирование API интернет-магазина")
@allure.story("Добавление продукта в корзину")
def test_add_product_to_cart():
    """
    Тест для метода добавления продукта в корзину.
    Проверяет, успешен ли запрос на добавление товара в корзину.
    """
    with allure.step("Добавить книгу в корзину"):
        product_id = 2963834  # ID продукта для добавления
        item_list_name = "search"  # Имя списка, откуда добавляется продукт
        add_to_cart_api = AddToCartAPI(API1_url)  # Создаем экземпляр API для добавления в корзину
        status_code = add_to_cart_api.add_product_to_cart(product_id, item_list_name)  # Выполняем запрос

    with allure.step("Проверить статус запроса"):
        assert status_code == 200, f"Expected 200, got {status_code}"  # Проверяем, что статус-код ответа равен 200