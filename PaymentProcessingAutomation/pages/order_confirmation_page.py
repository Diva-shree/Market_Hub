from locators.order_confirmation_locators import OrderConfirmationLocators


class OrderConfirmationPage:

    def __init__(self, driver):
        self.driver = driver

    def get_confirmation_text(self):

        return self.driver.find_element(*OrderConfirmationLocators.CONFIRMATION_MESSAGE).text

    def get_order_number(self):

        return self.driver.find_element(*OrderConfirmationLocators.ORDER_NUMBER).text
