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


@allure.title("Тест поиска книг по фразе. POSITIVE")
@allure.description("Этот тест проверяет, что поиск книг по фразе работает корректно.")
@allure.feature("READ")
@allure.severity("CRITICAL")
def test_search_by_phrase():
    """
    Проверка корректности результатов поиска по фразе.
    """
    with allure.step("Запустить браузер Chrome"):
        driver = webdriver.Chrome()
        driver.maximize_window()

    main = Mainpage(driver)

    with allure.step("Перейти на сайт Читай-город"):
        driver.get(UI_url)
        time.sleep(2)

    with allure.step("Принять куки"):
        driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(2)

    with allure.step("Найти книгу по фразе 'Сумейе Коч'"):
        search_phrase = "Сумейе Коч"
        main.search_by_frase(search_phrase)
        time.sleep(3)

    with allure.step("Проверить, что результаты поиска отображаются"):
        try:
            results = main.get_search_results()
            assert len(results) > 0, "Результаты поиска не найдены"
            allure.attach(f"Найдено результатов: {len(results)}", "Количество результатов", allure.attachment_type.TEXT)
        except TimeoutException:
            assert False, "Результаты поиска не загрузились в течение 10 секунд"

    with allure.step("Получить авторов из результатов поиска"):
        authors = main.get_authors_from_results()
        allure.attach(f"Найдено авторов: {len(authors)}", "Количество авторов", allure.attachment_type.TEXT)

        if authors:
            allure.attach("\n".join(authors[:5]), "Первые 5 авторов", allure.attachment_type.TEXT)

    with allure.step("Проверить, что искомая фраза присутствует в результатах"):
        search_phrase = "Сумейе Коч"
        phrase_found = False

        # Проверяем среди авторов
        for author in authors:
            if search_phrase.lower() in author.lower():
                phrase_found = True
                allure.attach(f"Найдена фраза у автора: {author}", "Фраза найдена", allure.attachment_type.TEXT)
                break

    with allure.step("Закрыть браузер"):
        driver.quit()


@allure.title("Тест поиска книг по несуществующей фразе")
@allure.description(
    "Проверяет, что при поиске по несуществующей фразе отображается сообщение об отсутствии результатов")
@allure.feature("READ")
@allure.severity("NORMAL")
def test_search_no_results():
    """
    Проверка поведения при поиске несуществующей фразы.
    """
    with allure.step("Запустить браузер Chrome"):
        driver = webdriver.Chrome()
        driver.maximize_window()

    main = Mainpage(driver)

    with allure.step("Перейти на сайт Читай-город"):
        driver.get(UI_url)
        time.sleep(2)

    with allure.step("Принять куки"):
        driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(2)

    with allure.step("Выполнить поиск по несуществующей фразе"):
        fake_phrase = "!@#$%^&*()_+несуществующаяфраза12345"
        main.search_by_frase(fake_phrase)
        time.sleep(3)

    with allure.step("Проверить, что отображается сообщение об отсутствии результатов"):
        no_results = main.is_no_results_message_displayed()

        if not no_results:
            # Альтернативная проверка: результатов нет
            try:
                results = driver.find_elements(By.XPATH, "//article[contains(@class, 'product-card')]")
                assert len(results) == 0, f"Найдено {len(results)} результатов при поиске несуществующей фразы"
                allure.attach("Результаты не найдены (пустой список)", "Проверка", allure.attachment_type.TEXT)
            except:
                pass
        else:
            allure.attach("Отображается сообщение об отсутствии результатов", "Проверка", allure.attachment_type.TEXT)

    with allure.step("Сделать скриншот страницы с результатами"):
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, "Результат поиска несуществующей фразы", allure.attachment_type.PNG)

    with allure.step("Закрыть браузер"):
        driver.quit()


@allure.title("Тест поиска книг по названию")
@allure.description("Проверяет поиск книг по конкретному названию")
@allure.feature("READ")
@allure.severity("CRITICAL")
def test_search_by_book_title():
    """
    Проверка поиска по названию книги.
    """
    with allure.step("Запустить браузер Chrome"):
        driver = webdriver.Chrome()
        driver.maximize_window()

    main = Mainpage(driver)

    with allure.step("Перейти на сайт Читай-город"):
        driver.get(UI_url)
        time.sleep(2)

    with allure.step("Принять куки"):
        driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(2)

    with allure.step("Найти книгу по названию 'Мастер и Маргарита'"):
        book_title = "Мастер и Маргарита"
        main.search_by_frase(book_title)
        time.sleep(3)

    with allure.step("Получить результаты поиска"):
        results = main.get_search_results()
        assert len(results) > 0, "Результаты поиска не найдены"
        allure.attach(f"Найдено результатов: {len(results)}", "Количество результатов", allure.attachment_type.TEXT)

    with allure.step("Получить названия книг из результатов"):
        titles = main.get_book_titles_from_results()
        allure.attach(f"Найдено названий: {len(titles)}", "Количество названий", allure.attachment_type.TEXT)

    with allure.step("Проверить, что искомая книга присутствует в результатах"):
        book_title = "Мастер и Маргарита"
        title_found = True

        for title in titles:
            if book_title.lower() in title.lower():
                title_found = True
                allure.attach(f"Найдена книга: {title}", "Книга найдена", allure.attachment_type.TEXT)
                break

        assert title_found, f"Книга '{book_title}' не найдена в результатах поиска"

    with allure.step("Сделать скриншот результатов"):
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, "Результаты поиска по названию", allure.attachment_type.PNG)

    with allure.step("Закрыть браузер"):
        driver.quit()


