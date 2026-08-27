from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    # ============================================================
    # Website URL
    # ============================================================

    LOGIN_URL = "https://qah.bishalkarki.com/login"

    # ============================================================
    # Locators
    # ============================================================

    EMAIL_FIELD = (
        By.ID,
        "field-email"
    )

    PASSWORD_FIELD = (
        By.ID,
        "field-password"
    )

    SIGN_IN_BUTTON = (
        By.ID,
        "submit-login"
    )

    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        ".alert.alert-danger"
    )

    LOGOUT_LINK = (
        By.CSS_SELECTOR,
        'a[href*="mylogout"]'
    )

    # ============================================================
    # Constructor
    # ============================================================

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            10
        )

    # ============================================================
    # Open Login Page
    # ============================================================

    def open_login_page(self):

        self.driver.get(
            self.LOGIN_URL
        )

        self.wait.until(
            EC.visibility_of_element_located(
                self.EMAIL_FIELD
            )
        )

    # ============================================================
    # Enter Email
    # ============================================================

    def enter_email(self, email):

        email_field = self.wait.until(
            EC.visibility_of_element_located(
                self.EMAIL_FIELD
            )
        )

        email_field.clear()

        email_field.send_keys(
            email
        )

    # ============================================================
    # Enter Password
    # ============================================================

    def enter_password(self, password):

        password_field = self.wait.until(
            EC.visibility_of_element_located(
                self.PASSWORD_FIELD
            )
        )

        password_field.clear()

        password_field.send_keys(
            password
        )

    # ============================================================
    # Click Sign In
    # ============================================================

    def click_sign_in(self):

        sign_in_button = self.wait.until(
            EC.element_to_be_clickable(
                self.SIGN_IN_BUTTON
            )
        )

        sign_in_button.click()

    # ============================================================
    # Login
    # ============================================================

    def login(self, email, password):

        self.enter_email(email)

        self.enter_password(password)

        self.click_sign_in()

    # ============================================================
    # Get Error Message
    # ============================================================

    def get_error_message(self):

        error = self.wait.until(
            EC.visibility_of_element_located(
                self.ERROR_MESSAGE
            )
        )

        return error.text

    # ============================================================
    # Logout
    # ============================================================

    def logout(self):

        logout_button = self.wait.until(
            EC.element_to_be_clickable(
                self.LOGOUT_LINK
            )
        )

        logout_button.click()