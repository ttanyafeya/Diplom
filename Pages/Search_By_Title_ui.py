from selenium import webdriver
from selenium.webdriver.common.by import By
import allure

@allure.description("Тестирование поля поиска по названию на сайте Читай-город.")
class SearchByTitle:
    """Класс для выполнения поиска книг по названию на сайте Читай-город."""

    def __init__(self, book_title: str):
        """
                    Инициализация класса SearchByTitle.

                    :param book_title: Название книги, которую необходимо найти.
        """
        self.book_title = book_title

    @allure.step("Поиск книги по названию")
    def search_by_title(self, driver: webdriver.Chrome) -> None:
        """
                    Поиск книг по названию на сайте Читай-город.

                    :param driver: Экземпляр драйвера Selenium (в данном случае Chrome).
                    :raises Exception: Возникает, если не удается найти элементы поиска на странице.
        """
        # Ввод названия в строку поиска
        try:
            search_input = driver.find_element(By.NAME, "phrase")
            search_input.send_keys(self.book_title)

            # Клик по кнопке поиска
            search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Искать']")
            search_button.click()
        except Exception as e:
            allure.attach(str(e), name="error", attachment_type=allure.attachment_type.TEXT)
            raise