from selenium.webdriver.common.by import By


class ProductDetailLocators:

    ADD_TO_CART_BUTTON = (
        By.XPATH,
        '//*[@id="add-to-cart-or-refresh"]/div[2]/div/div[2]/button'
    )

    ADDED_TO_CART_MODAL_CLOSE = (
        By.XPATH,
        '//*[@id="blockcart-modal"]//button[contains(@class,"close")]'
    )
