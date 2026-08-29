import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.product_detail_locators import ProductDetailLocators


class ProductDetailPage:

    def __init__(self, driver):
        self.driver = driver

    def add_to_cart(self):

        self.driver.find_element(*ProductDetailLocators.ADD_TO_CART_BUTTON).click()

        time.sleep(2)

    def close_added_to_cart_modal(self):

        # NOTE: the "Product added" modal renders via AJAX, so a
        # fixed sleep isn't reliable — wait for it to be clickable.
        close_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ProductDetailLocators.ADDED_TO_CART_MODAL_CLOSE)
        )

        close_button.click()

        time.sleep(1)
