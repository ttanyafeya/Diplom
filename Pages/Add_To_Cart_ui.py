# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import allure
#
#
# def search_by_title(driver: webdriver.Chrome, book_title: str) -> None:
#     """         Ищет книгу по названию и добавляет её в корзину.
#
#                 :param driver: Экземпляр драйвера Selenium.
#                 :param book_title: Название книги для поиска.
#                 :return: Словарь с результатами поиска (в данном методе возвращает None).
#     """
#     # Ввод названия книги в строку поиска
#     driver.find_element(By.NAME, "phrase").send_keys(book_title)
#
#     # Клик по кнопке поиска
#     search_button_find = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Искать']")
#     search_button_find.click()
#
#     # Клик по кнопке "Купить"
#     search_button_buy = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Купить']")
#     search_button_buy.click()
#
#     # Открытие корзины
#     cart_icon = driver.find_element(By.CSS_SELECTOR, '.header-cart__icon')
#     cart_icon.click()
#
#
# @allure.description("Тестирование добавления товара в корзину на сайте Читай-город.")
# class AddToCart:
#
#     # ИНИЦИАЛИЗАЦИЯ
#     def __init__(self, book_title: str):
#         """         Создает объект для добавления книги в корзину.
#
#                     :param book_title: Название книги для добавления в корзину.
#         """
#         self.book_title = book_title
#
#     # ПОИСК КНИГИ ПО НАЗВАНИЮ
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
import time


@allure.description("Тестирование добавления товара в корзину на сайте Читай-город.")
class AddToCart:

    # ИНИЦИАЛИЗАЦИЯ
    def __init__(self, driver: webdriver.Chrome, book_title: str):
        """Создает объект для добавления книги в корзину.

        :param driver: Экземпляр драйвера Selenium
        :param book_title: Название книги для добавления в корзину
        """
        self.driver = driver
        self.book_title = book_title
        self.wait = WebDriverWait(driver, 10)

    def search_by_title(self) -> None:
        """Ищет книгу по названию на сайте Читай-город."""
        with allure.step(f"Поиск книги по названию: {self.book_title}"):
            # Ожидаем и находим поле поиска
            search_input = self.wait.until(
                EC.element_to_be_clickable((By.NAME, "phrase"))
            )
            search_input.clear()
            search_input.send_keys(self.book_title)
            allure.attach(f"Введено название: {self.book_title}", "Поисковый запрос", allure.attachment_type.TEXT)

    def click_search_button(self) -> None:
        """Нажимает кнопку поиска."""
        with allure.step("Нажать кнопку поиска"):
            search_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Искать']"))
            )
            search_button.click()
            time.sleep(2)
            allure.attach("Кнопка поиска нажата", "Действие", allure.attachment_type.TEXT)

    def add_first_book_to_cart(self) -> None:
        """Добавляет первую найденную книгу в корзину."""
        with allure.step("Добавить первую книгу в корзину"):
            # Ожидаем появления результатов поиска
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card"))
            )

            # Находим первую книгу и кнопку "Купить"
            first_book = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Купить']"))
            )
            # Находим первую книгу и кнопку "Оформить"
            first_book = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Оформить']"))
            )
            # Прокручиваем до кнопки
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_book)
            time.sleep(1)
            first_book.click()
            time.sleep(2)
            allure.attach("Книга добавлена в корзину", "Действие", allure.attachment_type.TEXT)

    def open_cart(self) -> None:
        """Открывает корзину."""
        with allure.step("Открыть корзину"):
            cart_icon = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.header-cart__icon'))
            )
            cart_icon.click()
            time.sleep(2)
            allure.attach("Корзина открыта", "Действие", allure.attachment_type.TEXT)

    def verify_book_in_cart(self) -> bool:
        """Проверяет, что книга добавлена в корзину."""
        with allure.step("Проверить наличие книги в корзине"):
            try:
                # Проверяем, что корзина не пуста
                cart_items = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-item"))
                )
                assert cart_items.is_displayed(), "Корзина пуста"

                # Проверяем название книги в корзине
                book_title_in_cart = self.driver.find_element(By.CSS_SELECTOR, ".cart-item__title")
                assert self.book_title.lower() in book_title_in_cart.text.lower(), \
                    f"Книга '{self.book_title}' не найдена в корзине"

                allure.attach(f"Книга '{self.book_title}' найдена в корзине", "Проверка", allure.attachment_type.TEXT)
                return True

            except (TimeoutException, NoSuchElementException) as e:
                allure.attach(f"Ошибка: {str(e)}", "Ошибка проверки", allure.attachment_type.TEXT)
                return False

    def get_cart_count(self) -> int:
        """Получает количество товаров в корзине."""
        with allure.step("Получить количество товаров в корзине"):
            try:
                cart_count = self.driver.find_element(By.CSS_SELECTOR, ".header-cart__count")
                count = int(cart_count.text) if cart_count.text.isdigit() else 0
                allure.attach(f"Товаров в корзине: {count}", "Счетчик корзины", allure.attachment_type.TEXT)
                return count
            except:
                allure.attach("Счетчик корзины не найден", "Предупреждение", allure.attachment_type.TEXT)
                return 0

    def execute_add_to_cart_flow(self) -> dict:
        """Выполняет полный сценарий добавления книги в корзину.

        :return: Словарь с результатами выполнения
        """
        result = {
            "success": False,
            "message": "",
            "cart_count": 0
        }

        try:
            self.search_by_title()
            self.click_search_button()
            self.add_first_book_to_cart()

            # Получаем количество товаров до открытия корзины
            cart_count_before = self.get_cart_count()

            self.open_cart()

            # Проверяем результат
            if self.verify_book_in_cart():
                cart_count_after = self.get_cart_count()
                result["success"] = True
                result["message"] = f"Книга '{self.book_title}' успешно добавлена в корзину"
                result["cart_count"] = cart_count_after
            else:
                result["message"] = f"Не удалось добавить книгу '{self.book_title}' в корзину"

        except Exception as e:
            result["message"] = f"Ошибка: {str(e)}"
            allure.attach(f"Ошибка выполнения: {str(e)}", "Ошибка", allure.attachment_type.TEXT)

        return result