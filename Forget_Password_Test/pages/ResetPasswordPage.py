from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locator.Locate import Locator


class ResetPassword:
    def __init__(self, driver):
        self.driver = driver
        self.lc = Locator()

    def get_new_password_field(self):
        self.driver.implicitly_wait(10)
        return self.driver.find_element(By.NAME, self.lc.txt_new_password_name)

    def enter_new_password(self, password):
        self.get_new_password_field().send_keys(password)

    def get_confirm_password_field(self):
        return self.driver.find_element(By.NAME, self.lc.txt_confirm_password_name)

    def enter_confirm_password(self, password):
        self.get_confirm_password_field().send_keys(password)

    def get_reset_button(self):
        return self.driver.find_element(By.NAME, self.lc.btn_reset_password_name)

    def click_reset_button(self):
        self.get_reset_button().click()

    def reset_password(self, new_password, confirm_password):
        self.enter_new_password(new_password)
        self.enter_confirm_password(confirm_password)
        self.click_reset_button()

    def get_success_message(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.lc.lbl_reset_success_class))
        ).text

    def get_error_message(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, self.lc.lbl_reset_error_class))
        ).text
