from selenium.webdriver.common.by import By


class CartLocators:

    CHECKOUT_BUTTON = (
        By.XPATH,
        '//*[@id="main"]/div/div[2]/div[1]/div[2]/div/a'
    )
