from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locator.Locate import Locator


class ForgotPassword:
    def __init__(self, driver):
        self.driver = driver
        self.lc = Locator()

    def get_forgot_password_link(self):
        self.driver.implicitly_wait(10)
        return self.driver.find_element(By.LINK_TEXT, self.lc.link_forgot_password_text)

    def click_forgot_password_link(self):
        self.get_forgot_password_link().click()

    def get_email_field(self):
        self.driver.implicitly_wait(10)
        return self.driver.find_element(By.ID, self.lc.txt_email_id)

    def enter_email(self, email):
        self.get_email_field().send_keys(email)

    def get_submit_button(self):
        return self.driver.find_element(By.ID, self.lc.btn_submit_id)

    def click_submit_button(self):
        self.get_submit_button().click()

    def request_password_reset(self, email):
        self.click_forgot_password_link()
        self.enter_email(email)
        self.click_submit_button()

    def get_confirmation_message(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.lc.lbl_confirmation_class))
        ).text

    def get_error_message(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.lc.lbl_error_class))
        ).text
