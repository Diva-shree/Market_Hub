import time

from selenium.webdriver.common.keys import Keys

from locators.home_page_locators import HomePageLocators


class HomePage:

    def __init__(self, driver):
        self.driver = driver

    def click_signin(self):

        self.driver.find_element(*HomePageLocators.SIGNIN_LINK).click()

        time.sleep(2)

    def search_product(self, product_name):

        search_box = self.driver.find_element(*HomePageLocators.SEARCH_BOX)

        search_box.clear()
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.ENTER)

        time.sleep(2)

    def open_cart(self):

        self.driver.find_element(*HomePageLocators.CART_ICON).click()

        time.sleep(2)
