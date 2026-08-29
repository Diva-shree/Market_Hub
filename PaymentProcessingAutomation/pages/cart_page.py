import time

from locators.cart_locators import CartLocators


class CartPage:

    def __init__(self, driver):
        self.driver = driver

    def click_checkout(self):

        self.driver.find_element(*CartLocators.CHECKOUT_BUTTON).click()

        time.sleep(2)
