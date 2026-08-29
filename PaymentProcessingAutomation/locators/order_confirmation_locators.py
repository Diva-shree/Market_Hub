from selenium.webdriver.common.by import By


class OrderConfirmationLocators:

    CONFIRMATION_MESSAGE = (
        By.XPATH,
        '//*[@id="content-hook_order_confirmation"]/div/div/div/h3'
    )

    ORDER_NUMBER = (
        By.XPATH,
        '//*[@id="order-items"]/div[1]'
    )
