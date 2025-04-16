import pytest
import time
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Фикстура для настройки браузера
@pytest.fixture(scope='function')
def browser():
    service = Service(executable_path='C:\\chromedriver\\chromedriver.exe')  # Укажите правильный путь
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()


# Параметризованный тест
@pytest.mark.parametrize('link', [
    "https://stepik.org/lesson/236895/step/1",
    "https://stepik.org/lesson/236896/step/1",
    "https://stepik.org/lesson/236897/step/1",
    "https://stepik.org/lesson/236898/step/1",
    "https://stepik.org/lesson/236899/step/1",
    "https://stepik.org/lesson/236903/step/1",
    "https://stepik.org/lesson/236904/step/1",
    "https://stepik.org/lesson/236905/step/1",
])
def test_stepik_feedback(browser, link):
    # Открываем страницу
    browser.get(link)
    # Авторизация (замените на ваши учетные данные)
    browser.find_element(By.NAME, "login").send_keys("katiaburkova@yandex.ru")  # Логин
    browser.find_element(By.NAME, "password").send_keys("VPRfor3.14")  # Пароль
    browser.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    # Ждем, пока страница загрузится
    WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.TAG_NAME, "textarea"))  # Поле для ответа
    )

    # Вычисляем правильный ответ
    answer = math.log(int(time.time()))

    # Вводим ответ и нажимаем отправить
    answer_field = browser.find_element(By.TAG_NAME, "textarea")
    answer_field.clear()
    answer_field.send_keys(str(answer))
    browser.find_element(By.CLASS_NAME, "submit-submission").click()

    # Проверяем фидбек
    feedback = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "smart-hints__hint"))
    ).text

    assert feedback == "Correct!", f"Expected 'Correct!', but got '{feedback}'"
