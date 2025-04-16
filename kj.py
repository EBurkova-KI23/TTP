from base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
import math
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class ProductPage(BasePage):
    def add_to_basket(self):
        add_button = self.browser.find_element(By.CSS_SELECTOR, ".btn-add-to-basket")
        add_button.click()

    def solve_quiz_and_get_code(self):
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")

    def get_product_name(self):
        return self.browser.find_element(By.CSS_SELECTOR, ".product_main h1").text

    def get_basket_message(self):
        return self.browser.find_element(By.CSS_SELECTOR, ".alertinner strong").text

    def get_basket_value(self):
        return self.browser.find_element(By.CSS_SELECTOR, ".alert-info .alertinner p strong").text

link = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/?promo=newYear"

@pytest.fixture(scope="function")
def browser():
    service = Service(executable_path='C:\\chromedriver\\chromedriver.exe')  # Убедитесь, что путь правильный
    driver = webdriver.Chrome(service=service)
    yield driver  # Вернуть драйвер для использования в тестах
    driver.quit()  # Закрыть драйвер после завершения теста

def test_guest_can_add_product_to_basket(browser):
    page = ProductPage(browser, link)
    page.open()

    product_name = page.get_product_name()
    page.add_to_basket()
    page.solve_quiz_and_get_code()

    assert page.get_basket_message() == product_name, "Product name does not match!"

    basket_value = page.get_basket_value()
    expected_value = "£9.99"
    assert basket_value == expected_value, "Basket value does not match!"

