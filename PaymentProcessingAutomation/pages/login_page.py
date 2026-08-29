import time

from locators.login_page_locators import LoginPageLocators


class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    def enter_email(self, email):

        self.driver.find_element(*LoginPageLocators.EMAIL_FIELD).send_keys(email)

    def enter_password(self, password):

        self.driver.find_element(*LoginPageLocators.PASSWORD_FIELD).send_keys(password)

    def click_login(self):

        self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

        time.sleep(3)

    def login(self, username, password):

        self.enter_email(username)
        self.enter_password(password)
        self.click_login()
