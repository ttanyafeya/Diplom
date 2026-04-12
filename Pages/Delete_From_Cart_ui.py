from selenium import webdriver
from selenium.webdriver.common.by import By
import allure


@allure.description("Тестирование удаления товара из корзины на сайте Читай-город.")
class DeleteFromCart:
    """Класс для удаления товара из корзины на сайте Читай-город."""

    def __init__(self, book_title: str):
        """
        Инициализация класса DeleteFromCart.

        :param book_title: Название книги, которую нужно удалить из корзины.
        """
        self.book_title = book_title

    @allure.step("Поиск книги по названию и удаление из корзины")
    def delete_from_cart(self, driver: webdriver.Chrome) -> None:
        """
        Поиск книги по названию, добавление в корзину и удаление из нее.

        :param driver: Экземпляр драйвера Selenium (в данном случае Chrome).
        :raises Exception: Возникает, если не удается найти элементы на странице.
        """

        # Поиск книги по названию
        driver.find_element(By.NAME, "phrase").send_keys(self.book_title)

        # Клик по кнопке поиска
        search_button_find = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Искать']")
        search_button_find.click()

        # Клик по кнопке "Купить"
        search_button_buy = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Купить']")
        search_button_buy.click()

        # Открытие корзины
        cart_icon = driver.find_element(By.CSS_SELECTOR, '.header-cart__icon')
        cart_icon.click()

        # Клик по кнопке "Очистить корзину"
        delete_button = driver.find_element(By.CSS_SELECTOR, 'span.clear-cart')
        delete_button.click()