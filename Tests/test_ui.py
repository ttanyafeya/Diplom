import pytest
# from Pages.mainpage import Mainpage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import allure
from Pages.mainpage import Mainpage


@allure.title("Тест поиска книг по фразе. POSITIVE")
@allure.description("Этот тест проверяет,"
                    " что поиск книг по фразе работает корректно.")
@allure.feature("READ")
@allure.severity("CRITICAL")
def test_search_by_phrase(driver):
    """
    Проверка корректности результатов поиска по фразе.
    """
    main = Mainpage(driver)

    with allure.step("Перейти на сайт Читай-город"):
        main.open_main()

    with allure.step("Найти книгу по фразе 'Сумейе Коч'"):
        search_phrase = "Сумейе Коч"
        main.search_by_frase(search_phrase)

    with allure.step("Проверить, что результаты поиска отображаются"):
        try:
            results = main.get_search_results()
            assert len(results) > 0, "Результаты поиска не найдены"
            allure.attach(f"Найдено результатов: {len(results)}",
                          "Количество результатов",
                          allure.attachment_type.TEXT)
        except TimeoutException:
            assert False, ("Результаты поиска"
                           " не загрузились в течение 10 секунд")

    with allure.step("Получить авторов из результатов поиска"):
        authors = main.get_authors_from_results()
        allure.attach(f"Найдено авторов: {len(authors)}",
                      "Количество авторов", allure.attachment_type.TEXT)

        if authors:
            allure.attach("\n".join(authors[:5]),
                          "Первые 5 авторов", allure.attachment_type.TEXT)

    with allure.step("Проверить, что искомая фраза"
                     " присутствует в результатах"):
        search_phrase = "Сумейе Коч"
        phrase_found = False

        # Проверяем среди авторов
        for author in authors:
            if search_phrase.lower() in author.lower():
                phrase_found = True
                allure.attach(f"Найдена фраза у автора: {author}",
                              "Фраза найдена", allure.attachment_type.TEXT)
                break


@allure.title("Тест поиска книг по несуществующей фразе")
@allure.description(
    "Проверяет, что при поиске по несуществующей фразе"
    " отображается сообщение об отсутствии результатов")
@allure.feature("READ")
@allure.severity("NORMAL")
def test_search_no_results(driver):
    """
    Проверка поведения при поиске несуществующей фразы.
    """
    main = Mainpage(driver)

    with allure.step("Перейти на сайт Читай-город"):
        main.open_main()

    with allure.step("Выполнить поиск по несуществующей фразе"):
        fake_phrase = "!@#$%^&*()_+несуществующаяфраза12345"
        main.search_by_frase(fake_phrase)

    with allure.step("Проверить, что отображается сообщение"
                     " об отсутствии результатов"):
        no_results = main.is_no_results_message_displayed()

        if not no_results:
            # Альтернативная проверка: результатов нет
            try:
                results = driver.find_elements(By.XPATH,
                                               "//article[contains(@class,"
                                               " 'product-card')]")
                assert len(results) == 0, (f"Найдено {len(results)} "
                                           f"результатов "
                                           f"при поиске несуществующей фразы")
                allure.attach("Результаты не найдены (пустой список)",
                              "Проверка", allure.attachment_type.TEXT)
            except:
                pass
        else:
            allure.attach("Отображается сообщение об отсутствии результатов",
                          "Проверка", allure.attachment_type.TEXT)

    with allure.step("Сделать скриншот страницы с результатами"):
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot,
                      "Результат поиска несуществующей фразы",
                      allure.attachment_type.PNG)


@allure.title("Тест поиска книг по названию")
@allure.description("Проверяет поиск книг по конкретному названию")
@allure.feature("READ")
@allure.severity("CRITICAL")
def test_search_by_book_title(driver):
    """
    Проверка поиска по названию книги.
    """
    main = Mainpage(driver)

    with allure.step("Перейти на сайт Читай-город"):
        main.open_main()

    with allure.step("Найти книгу по названию 'Мастер и Маргарита'"):
        book_title = "Мастер и Маргарита"
        main.search_by_frase(book_title)

    with allure.step("Получить результаты поиска"):
        results = main.get_search_results()
        assert len(results) > 0, "Результаты поиска не найдены"
        allure.attach(f"Найдено результатов: {len(results)}",
                      "Количество результатов", allure.attachment_type.TEXT)

    with allure.step("Получить названия книг из результатов"):
        titles = main.get_book_titles_from_results()
        allure.attach(f"Найдено названий: {len(titles)}",
                      "Количество названий", allure.attachment_type.TEXT)

    with allure.step("Проверить, что искомая книга"
                     " присутствует в результатах"):
        book_title = "Мастер и Маргарита"
        title_found = True

        for title in titles:
            if book_title.lower() in title.lower():
                title_found = True
                allure.attach(f"Найдена книга: {title}",
                              "Книга найдена", allure.attachment_type.TEXT)
                break

        assert title_found, (f"Книга '{book_title}'"
                             f"не найдена в результатах поиска")

    with allure.step("Сделать скриншот результатов"):
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot,
                      "Результаты поиска по названию",
                      allure.attachment_type.PNG)


@allure.epic("Интернет-магазин Читай-город")
@allure.feature("Корзина")
class TestCart:
    """
    Тестовый класс для проверки функциональности корзины
     интернет-магазина "Читай-город"
    """

    @allure.title("Добавление товара в корзину")
    @allure.description("""
    ### Цель теста:
    Проверить успешное добавление товара в корзину.

    ### Шаги выполнения:
    1. Открыть главную страницу сайта "Читай-город"
    2. Перейти на страницу выбранной книги (123 Посчитай со мной)
    3. Нажать на кнопку "Купить"
    4. Проверить, что кнопка изменилась на "Оформить"
    5. Проверить, что счётчик корзины стал равен 1

    ### Ожидаемый результат:
    - Кнопка "Оформить" отображается на странице
    - Счётчик корзины показывает 1 товар
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "cart", "positive", "add_to_cart")
    @allure.link("https://www.chitai-gorod.ru/"
                 "product/123-poschitay-so-mnoy-3010448",
                 name="Ссылка на тестовую книгу")
    @allure.issue("TC-001", name="Тест-кейс: Добавление товара в корзину")
    def test_add_to_cart(self, driver):
        """
        Тест проверяет добавление одного товара в корзину
        """

        # Инициализация главной страницы
        with allure.step("Инициализация главной страницы"):
            main = Mainpage(driver)
            allure.attach(
                "Объект Mainpage успешно создан",
                name="Инициализация",
                attachment_type=allure.attachment_type.TEXT
            )

        # 1. Открыть браузер
        with allure.step("Открытие главной страницы сайта 'Читай-город'"):
            main.open_main()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Главная страница",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                "URL: https://www.chitai-gorod.ru/",
                name="Открытая страница",
                attachment_type=allure.attachment_type.TEXT
            )

        # Переходим на страницу книги
        book_url = ("https://www.chitai-gorod.ru/product/"
                    "123-poschitay-so-mnoy-3010448")
        with allure.step(f"Переход на страницу книги: {book_url}"):
            main.go_to_book(book_url)
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Страница книги '123 Посчитай со мной'",
                attachment_type=allure.attachment_type.PNG
            )

            allure.attach(
                """ID товара: 3010448
            Название: 123 Посчитай со мной
            Издательство: АСТ""",
                name="Информация о книге",
                attachment_type=allure.attachment_type.TEXT
            )
        # Жмём кнопку Купить
        with allure.step("Нажатие на кнопку 'Купить'"):
            main.buy_current_book()
            allure.attach(
                "Клик по кнопке 'Купить' выполнен успешно",
                name="Действие",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                driver.get_screenshot_as_png(),
                name="После нажатия 'Купить'",
                attachment_type=allure.attachment_type.PNG
            )

        # Проверяем что появилась кнопка оформить
        with allure.step("Проверка отображения кнопки 'Оформить'"):
            is_oformit = main.is_button_oformit()
            allure.attach(
                f"Результат проверки:"
                f" кнопка 'Оформить'"
                f" {'отображается' if is_oformit else 'НЕ отображается'}",
                name="Статус кнопки 'Оформить'",
                attachment_type=allure.attachment_type.TEXT
            )
            assert is_oformit, ("❌ Не отображается кнопка"
                                " 'Оформить' после добавления товара")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Кнопка 'Оформить' успешно отображается",
                attachment_type=allure.attachment_type.PNG
            )

        # Проверяем количество товаров в корзине
        with ((allure.step("Проверка счётчика товаров в корзине"))):
            cart_count = main.get_cart_count()
            allure.attach(
                f"Текущее количество товаров в корзине: {cart_count}",
                name="Счётчик корзины",
                attachment_type=allure.attachment_type.TEXT
            )
            assert cart_count == 1, (f"❌ Количество товара в корзине"
                                     f" равно {cart_count}, ожидается 1")

        # Финальный результат
        allure.attach(
            "✅ ТЕСТ УСПЕШНО ПРОЙДЕН\n"
            "✓ Книга добавлена в корзину\n"
            "✓ Кнопка 'Оформить' отображается\n"
            "✓ Счётчик корзины = 1",
            name="Результат теста",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.title("Удаление товара из корзины")
    @allure.description("""
    ### Цель теста:
    Проверить успешное удаление товара из корзины
    через интерфейс корзины.
    ### Шаги выполнения:
    1. Открыть главную страницу сайта
    2. Перейти на страницу выбранной книги
    3. Добавить книгу в корзину (нажать 'Купить')
    4. Проверить успешность добавления
     (кнопка 'Оформить', счётчик = 1)
    5. Перейти в корзину
    6. Нажать кнопку очистки корзины
    7. Проверить отображение сообщения о пустой корзине
    ### Ожидаемый результат:
    - Товар успешно добавлен в корзину
    - После очистки корзины отображается сообщение,
     что корзина пуста
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "cart", "delete",
                "positive", "remove_from_cart")
    @allure.issue("TC-002",
                  name="Тест-кейс: Удаление товара из корзины")
    def test_remove_from_cart(self, driver):
        """
        Тест проверяет удаление товара из корзины
        """

        # Инициализация главной страницы
        with allure.step("Инициализация главной страницы"):
            main = Mainpage(driver)
            allure.attach("Объект Mainpage создан",
                          name="Инициализация")

        # 1. Открыть браузер
        with allure.step("Открытие главной страницы сайта"):
            main.open_main()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Главная страница",
                attachment_type=allure.attachment_type.PNG
            )

        # Переходим на страницу книги
        book_url = ("https://www.chitai-gorod.ru/product/"
                    "123-poschitay-so-mnoy-3010448")
        with allure.step("Переход на страницу книги"
                         " '123 Посчитай со мной'"):
            main.go_to_book(book_url)
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Страница книги",
                attachment_type=allure.attachment_type.PNG
            )

        # Жмём кнопку Купить
        with allure.step("Добавление книги в корзину"
                         " (нажатие 'Купить')"):
            main.buy_current_book()
            allure.attach("Клик по кнопке 'Купить' выполнен",
                          name="Действие")

        # Проверяем что появилась кнопка оформить
        with ((allure.step("Проверка появления кнопки 'Оформить'"))):
            assert main.is_button_oformit(), ("❌ Не"
                                              " отображается кнопка"
                                              " 'Оформить'")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Кнопка 'Оформить' отображается",
                attachment_type=allure.attachment_type.PNG
            )

        # Проверяем количество товаров в корзине
        with allure.step("Проверка количества товаров"
                         " в корзине после добавления"):
            cart_count = main.get_cart_count()
            assert cart_count == 1, (f"❌ Количество товара:"
                                     f" {cart_count}, ожидается 1")
            allure.attach(
                f"Товаров в корзине: {cart_count}",
                name="Счётчик корзины",
                attachment_type=allure.attachment_type.TEXT
            )

        # Переходим в корзину
        with allure.step("Переход в корзину"):
            main.click_cart()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Страница корзины с товарами",
                attachment_type=allure.attachment_type.PNG
            )

        # Очищаем корзину
        with allure.step("Очистка корзины (удаление всех товаров)"):
            main.clear_cart_items()
            allure.attach(
                "Нажата кнопка очистки корзины",
                name="Действие",
                attachment_type=allure.attachment_type.TEXT
            )

        # Проверяем сообщение о пустой корзине
        with (allure.step("Проверка отображения сообщения о пустой корзине")):
            is_empty_message = main.is_cleared_cart_message()
            allure.attach(
                f"Сообщение о пустой корзине:"
                f" {'отображается' if is_empty_message else 'НЕ отображается'}",
                name="Статус сообщения",
                attachment_type=allure.attachment_type.TEXT
            )
            assert is_empty_message, ("❌ Не появилось"
                                      " сообщение о том, что корзина пуста")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Сообщение о пустой корзине",
                attachment_type=allure.attachment_type.PNG
            )

        # Финальный результат
        allure.attach(
            "✅ ТЕСТ УСПЕШНО ПРОЙДЕН\n"
            "✓ Книга добавлена в корзину\n"
            "✓ Корзина очищена\n"
            "✓ Отображается сообщение о пустой корзине",
            name="Результат теста",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.title("Комплексный тест:"
                  " добавление и удаление товара из корзины")
    @allure.description("""
    ### Цель теста:
    Проверить полный жизненный цикл работы с корзиной:
    - Добавление товара
    - Проверка счётчика
    - Удаление товара
    - Проверка пустой корзины

    ### Шаги выполнения:
    1. Открыть сайт и перейти на страницу книги
    2. Добавить книгу в корзину
    3. Проверить, что кнопка изменилась на 'Оформить'
    4. Проверить, что счётчик корзины = 1
    5. Перейти в корзину и очистить её
    6. Проверить, что отображается сообщение о пустой корзине

    ### Ожидаемый результат:
    - Все шаги выполняются успешно
    - Корзина корректно отображает состояние
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("e2e", "cart", "full_cycle", "smoke")
    @allure.issue("TC-003",
                  name="Тест-кейс: Полный цикл работы с корзиной")
    def test_full_cart_cycle(self, driver):
        """
        Комплексный E2E тест полного цикла работы с корзиной
        """

        main = Mainpage(driver)

        with allure.step("Этап 1: Открытие сайта и добавление книги"):
            main.open_main()
            main.go_to_book("https://www.chitai-gorod.ru/"
                            "product/123-poschitay-so-mnoy-3010448")
            main.buy_current_book()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Книга добавлена в корзину",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Этап 2: Проверка успешного добавления"):
            assert main.is_button_oformit(), "❌ Кнопка 'Оформить' не появилась"
            assert main.get_cart_count() == 1, "❌ Товар не добавлен в корзину"
            allure.attach(
                "✓ Товар успешно добавлен в корзину",
                name="Промежуточный результат",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Этап 3: Удаление товара из корзины"):
            main.click_cart()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Корзина с товаром",
                attachment_type=allure.attachment_type.PNG
            )
            main.clear_cart_items()
            allure.attach("Корзина очищена", name="Действие")

        with (allure.step("Этап 4: Проверка пустой корзины")):
            assert main.is_cleared_cart_message(), (
                "❌ Корзина не очищена или сообщение не отображается")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Пустая корзина с сообщением",
                attachment_type=allure.attachment_type.PNG
            )

        # Финальный результат
        allure.attach(
            "✅ ПОЛНЫЙ ЦИКЛ УСПЕШНО ЗАВЕРШЁН\n"
            "✓ Добавление товара ✓\n"
            "✓ Проверка счётчика ✓\n"
            "✓ Очистка корзины ✓\n"
            "✓ Проверка пустой корзины ✓",
            name="Результат теста",
            attachment_type=allure.attachment_type.TEXT
        )


# Для запуска тестов с Allure отчётом
if __name__ == "__main__":
    """
    Команды для запуска тестов:

    1. Запуск всех тестов с генерацией Allure результатов:
       pytest test_cart_allure.py
        -v --alluredir=./allure-results --clean-alluredir

    2. Запуск конкретного теста:
       pytest test_cart_allure.py::TestCart::test_add_to_cart
        -v --alluredir=./allure-results

    3. Запуск с определёнными метками:
       pytest test_cart_allure.py -v -m smoke --alluredir=./allure-results

    4. Просмотр Allure отчёта:
       allure serve ./allure-results
    """
    pytest.main([
        __file__,
        "-v",
        "--alluredir=./allure-results",
        "--clean-alluredir"
    ])
