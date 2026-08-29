from selenium.webdriver.common.by import By


class LoginPageLocators:

    EMAIL_FIELD = (
        By.ID,
        "field-email"
    )

    PASSWORD_FIELD = (
        By.ID,
        "field-password"
    )

    LOGIN_BUTTON = (
        By.XPATH,
        '//*[@id="submit-login"]'
    )
