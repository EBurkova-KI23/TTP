from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
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

@pytest.mark.parametrize('link', [
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer1",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer2",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer3",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer4",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer5",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer6",
    pytest.param("http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7", 
                 marks=pytest.mark.xfail(reason="Known bug with this promo")),
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer8",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer9"
])
def test_guest_can_add_product_to_basket(browser, link):
    page = ProductPage(browser, link)
    page.open()

    product_name = page.get_product_name()
    product_price = page.get_product_price()
    page.add_to_basket()
    page.solve_quiz_and_get_code()

    assert page.get_basket_message() == product_name, "Product name does not match!"
    assert page.get_basket_value() == product_price, "Basket value does not match!"


