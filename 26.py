from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import math
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class BasePage():
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def open(self):
        self.browser.get(self.url)

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException). \
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True


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

    def get_product_price(self):
        return self.browser.find_element(By.CSS_SELECTOR, ".product_main .price_color").text

    def get_basket_message(self):
        return self.browser.find_element(By.CSS_SELECTOR, ".alert-success .alertinner strong").text

    def get_basket_value(self):
        return self.browser.find_element(By.CSS_SELECTOR, ".alert-info .alertinner p strong").text


@pytest.fixture(scope="function")
def browser():
    service = Service(executable_path='C:\\chromedriver\\chromedriver.exe')  # Убедитесь, что путь правильный
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()


def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0"
    page = ProductPage(browser, link)
    page.open()
    page.add_to_basket()
    page.solve_quiz_and_get_code()
    assert page.is_not_element_present(By.CSS_SELECTOR, ".alert-success"), \
        "Success message is presented, but should not be"


def test_guest_cant_see_success_message(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0"
    page = ProductPage(browser, link)
    page.open()
    assert page.is_not_element_present(By.CSS_SELECTOR, ".alert-success"), \
        "Success message is presented, but should not be"


def test_message_disappeared_after_adding_product_to_basket(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0"
    page = ProductPage(browser, link)
    page.open()
    page.add_to_basket()
    page.solve_quiz_and_get_code()
    assert page.is_disappeared(By.CSS_SELECTOR, ".alert-success"), \
        "Success message did not disappear"



