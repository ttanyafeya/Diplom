import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
from Pages.mainpage import Mainpage
from constants import UI_url

cookie = {"name": "cookie_policy", "value": "1"}


@allure.epic("Интернет-магазин Читай-город")
@allure.feature("Корзина")
@allure.story("Добавление товаров в корзину")
@allure.title("Добавление первой книги с главной страницы в корзину")
@allure.description("""
    Тест проверяет возможность добавления первой книги с главной страницы сайта в корзину.
    Включает следующие шаги:
    1. Открытие главной страницы
    2. Поиск первой книги на странице
    3. Добавление книги в корзину
    4. Проверка, что книга успешно добавлена
    5. Переход в корзину для подтверждения
""")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("UI", "CART", "POSITIVE")
@allure.link("https://www.chitai-gorod.ru/", name="Website")
def test_add_first_book_to_cart():
    """
    Тест добавления первой книги с главной страницы в корзину
    """

    with allure.step("Инициализация браузера Chrome"):
        driver = webdriver.Chrome()
        driver.maximize_window()
        allure.attach(
            driver.get_window_size().__str__(),
            "Размер окна браузера",
            allure.attachment_type.TEXT
        )

    main = Mainpage(driver)

    try:
        with allure.step("Открытие главной страницы сайта"):
            driver.get(UI_url)
            time.sleep(2)
            allure.attach(
                driver.current_url,
                "Текущий URL",
                allure.attachment_type.TEXT
            )
            allure.attach(
                driver.get_screenshot_as_png(),
                "Главная страница",
                allure.attachment_type.PNG
            )

        with allure.step("Принятие cookie-соглашения"):
            driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(2)
            allure.attach(
                "Cookie policy accepted",
                "Статус cookie",
                allure.attachment_type.TEXT
            )

        with allure.step("Поиск первой книги на главной странице"):
            # Локаторы для первой книги на главной странице
            first_book_locators = [
                "//article[contains(@class, 'product-card')][1]",
                "//div[contains(@class, 'products-list')]//article[1]",
                "//div[@data-testid='product-card'][1]"
            ]

            first_book = None
            for locator in first_book_locators:
                try:
                    first_book = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, locator))
                    )
                    if first_book:
                        allure.attach(
                            f"Найден по локатору: {locator}",
                            "Локатор первой книги",
                            allure.attachment_type.TEXT
                        )
                        break
                except:
                    continue

            assert first_book is not None, "Первая книга не найдена на главной странице"

            # Получаем название книги
            try:
                book_title_element = first_book.find_element(By.XPATH,
                                                             ".//div[contains(@class, 'product-card__title')]")
                book_title = book_title_element.text
            except:
                book_title = "Название не определено"

            # Получаем автора книги
            try:
                book_author_element = first_book.find_element(By.XPATH,
                                                              ".//div[contains(@class, 'product-card__author')]")
                book_author = book_author_element.text
            except:
                book_author = "Автор не указан"

            allure.attach(
                f"Название: {book_title}\nАвтор: {book_author}",
                "Информация о первой книге",
                allure.attachment_type.TEXT
            )

            # Скроллим до книги
            driver.execute_script("arguments[0].scrollIntoView(true);", first_book)
            time.sleep(1)

            # Делаем скриншот найденной книги
            allure.attach(
                driver.get_screenshot_as_png(),
                f"Первая книга - {book_title[:30]}",
                allure.attachment_type.PNG
            )

        with allure.step("Нахождение и нажатие кнопки 'В корзину'"):
            # Пробуем разные локаторы для кнопки добавления в корзину
            add_to_cart_locators = [
                ".//button[contains(@class, 'product-card__add-to-cart')]",
                ".//button[contains(text(), 'В корзину')]",
                ".//button[contains(@class, 'btn--cart')]",
                ".//button[@data-testid='add-to-cart']",
                ".//button[contains(@class, 'add-to-cart')]"
            ]

            add_button = None
            for locator in add_to_cart_locators:
                try:
                    add_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, locator))
                    )
                    if add_button:
                        allure.attach(
                            f"Кнопка найдена по локатору: {locator}",
                            "Локатор кнопки",
                            allure.attachment_type.TEXT
                        )
                        break
                except:
                    continue

            assert add_button is not None, "Кнопка добавления в корзину не найдена"

            # Нажимаем кнопку
            driver.execute_script("arguments[0].click();", add_button)
            allure.attach(
                "Кнопка 'В корзину' нажата",
                "Действие",
                allure.attachment_type.TEXT
            )
            time.sleep(2)

        with allure.step("Проверка успешного добавления в корзину"):
            # Проверяем появление уведомления о добавлении
            notification_locators = [
                "//div[contains(@class, 'notification')]",
                "//div[contains(text(), 'добавлен')]",
                "//div[contains(@class, 'toast')]"
            ]

            notification_found = False
            for locator in notification_locators:
                try:
                    notification = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, locator))
                    )
                    if notification.is_displayed():
                        notification_found = True
                        allure.attach(
                            f"Уведомление: {notification.text}",
                            "Уведомление о добавлении",
                            allure.attachment_type.TEXT
                        )
                        break
                except:
                    continue

            if notification_found:
                allure.attach(
                    "Товар успешно добавлен в корзину",
                    "Результат",
                    allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    "Уведомление не найдено, но это не критично",
                    "Предупреждение",
                    allure.attachment_type.TEXT
                )

        with allure.step("Проверка счетчика корзины"):
            # Проверяем, что счетчик корзины увеличился
            cart_counter_locators = [
                "//span[contains(@class, 'cart-counter')]",
                "//div[contains(@class, 'cart__count')]",
                "//a[@href='/cart']//span"
            ]

            counter_value = 0
            for locator in cart_counter_locators:
                try:
                    counter_element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, locator))
                    )
                    counter_text = counter_element.text
                    if counter_text and counter_text.isdigit():
                        counter_value = int(counter_text)
                        allure.attach(
                            f"Счетчик корзины: {counter_value}",
                            "Счетчик товаров",
                            allure.attachment_type.TEXT
                        )
                        break
                except:
                    continue

            assert counter_value > 0, "Счетчик корзины не обновился"

        with allure.step("Переход в корзину для финальной проверки"):
            cart_icon_locators = [
                "//a[@href='/cart']",
                "//div[contains(@class, 'cart')]//a",
                "//button[contains(@class, 'cart')]"
            ]

            for locator in cart_icon_locators:
                try:
                    cart_icon = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, locator))
                    )
                    cart_icon.click()
                    allure.attach(
                        "Переход в корзину выполнен",
                        "Действие",
                        allure.attachment_type.TEXT
                    )
                    break
                except:
                    continue

            time.sleep(3)

            # Проверяем, что мы на странице корзины
            current_url = driver.current_url
            assert "cart" in current_url.lower(), "Не удалось перейти в корзину"
            allure.attach(
                current_url,
                "URL корзины",
                allure.attachment_type.TEXT
            )

            # Проверяем наличие товаров в корзине
            cart_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'cart-item')]")
            assert len(cart_items) > 0, "В корзине нет товаров"
            allure.attach(
                f"Найдено товаров в корзине: {len(cart_items)}",
                "Содержимое корзины",
                allure.attachment_type.TEXT
            )

            # Делаем скриншот корзины
            allure.attach(
                driver.get_screenshot_as_png(),
                "Корзина с добавленным товаром",
                allure.attachment_type.PNG
            )

        with allure.step("Тест успешно завершен"):
            allure.attach(
                "✅ Все проверки пройдены успешно",
                "Результат теста",
                allure.attachment_type.TEXT
            )

    except Exception as e:
        with allure.step(f"Ошибка в тесте: {str(e)}"):
            allure.attach(
                driver.get_screenshot_as_png(),
                "Скриншот ошибки",
                allure.attachment_type.PNG
            )
            raise

    finally:
        with allure.step("Закрытие браузера"):
            driver.quit()
            allure.attach(
                "Браузер закрыт",
                "Завершение",
                allure.attachment_type.TEXT
            )


@allure.epic("Интернет-магазин Читай-город")
@allure.feature("Корзина")
@allure.story("Добавление товаров в корзину")
@allure.title("Добавление первой книги с главной страницы в корзину (улучшенная версия)")
@allure.description("""
    Улучшенная версия теста с дополнительными проверками:
    - Проверка изменения счетчика корзины
    - Проверка текста кнопки до и после добавления
    - Повторная проверка содержимого корзины
""")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_first_book_to_cart_enhanced():
    """
    Улучшенная версия теста с дополнительными проверками
    """

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        with allure.step("Открытие сайта и настройка"):
            driver.get(UI_url)
            driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(2)
            allure.attach(
                "Сайт открыт, куки приняты",
                "Инициализация",
                allure.attachment_type.TEXT
            )

        with allure.step("Поиск первой книги и получение информации"):
            # Находим первую книгу
            first_book = wait.until(
                EC.presence_of_element_located((By.XPATH, "//article[contains(@class, 'product-card')][1]"))
            )

            # Получаем информацию о книге
            book_info = {}

            try:
                title_elem = first_book.find_element(By.XPATH, ".//div[contains(@class, 'product-card__title')]")
                book_info['title'] = title_elem.text
            except:
                book_info['title'] = "Unknown"

            try:
                price_elem = first_book.find_element(By.XPATH, ".//div[contains(@class, 'product-card__price')]")
                book_info['price'] = price_elem.text
            except:
                book_info['price'] = "Price not found"

            allure.attach(
                f"Книга: {book_info['title']}\nЦена: {book_info['price']}",
                "Информация о добавляемой книге",
                allure.attachment_type.TEXT
            )

        with allure.step("Запоминаем начальное состояние корзины"):
            # Находим начальное значение счетчика
            initial_counter = 0
            try:
                counter_elem = driver.find_element(By.XPATH, "//span[contains(@class, 'cart-counter')]")
                if counter_elem.text.isdigit():
                    initial_counter = int(counter_elem.text)
            except:
                initial_counter = 0

            allure.attach(
                f"Начальное значение счетчика: {initial_counter}",
                "Счетчик корзины",
                allure.attachment_type.TEXT
            )

        with allure.step("Добавление книги в корзину"):
            # Находим и нажимаем кнопку добавления
            add_button = wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//article[contains(@class, 'product-card')][1]//button[contains(@class, 'add-to-cart')]"))
            )

            # Запоминаем текст кнопки
            button_text_before = add_button.text
            allure.attach(
                f"Текст кнопки до нажатия: {button_text_before}",
                "Кнопка добавления",
                allure.attachment_type.TEXT
            )

            # Нажимаем кнопку
            driver.execute_script("arguments[0].click();", add_button)
            time.sleep(2)

            # Проверяем, изменился ли текст кнопки
            try:
                button_text_after = add_button.text
                if button_text_before != button_text_after:
                    allure.attach(
                        f"Текст кнопки изменился на: {button_text_after}",
                        "Изменение кнопки",
                        allure.attachment_type.TEXT
                    )
            except:
                pass

        with allure.step("Проверка обновления счетчика корзины"):
            # Ждем обновления счетчика
            time.sleep(2)

            final_counter = 0
            try:
                counter_elem = driver.find_element(By.XPATH, "//span[contains(@class, 'cart-counter')]")
                if counter_elem.text.isdigit():
                    final_counter = int(counter_elem.text)
            except:
                final_counter = initial_counter

            allure.attach(
                f"Конечное значение счетчика: {final_counter}",
                "Счетчик корзины после добавления",
                allure.attachment_type.TEXT
            )

            assert final_counter > initial_counter, "Счетчик корзины не увеличился"

        with allure.step("Финальная проверка в корзине"):
            # Переходим в корзину
            cart_link = driver.find_element(By.XPATH, "//a[@href='/cart']")
            cart_link.click()
            time.sleep(2)

            # Проверяем, что добавленная книга присутствует
            cart_items = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'cart-item')]"))
            )

            assert len(cart_items) > 0, "Корзина пуста"

            # Ищем нашу книгу в корзине
            book_found = False
            for item in cart_items:
                try:
                    item_title = item.find_element(By.XPATH, ".//div[contains(@class, 'cart-item__title')]").text
                    if book_info['title'].lower() in item_title.lower():
                        book_found = True
                        allure.attach(
                            f"Книга '{item_title}' найдена в корзине",
                            "Проверка содержимого",
                            allure.attachment_type.TEXT
                        )
                        break
                except:
                    continue

            assert book_found, f"Книга '{book_info['title']}' не найдена в корзине"

            allure.attach(
                driver.get_screenshot_as_png(),
                "Финальный скриншот корзины",
                allure.attachment_type.PNG
            )

    finally:
        driver.quit()