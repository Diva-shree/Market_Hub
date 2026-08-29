import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.checkout_locators import CheckoutLocators


class CheckoutPage:

    def __init__(self, driver):
        self.driver = driver

    # --------------------------------------------------------
    # Address step
    # --------------------------------------------------------

    def continue_address(self):

        self.driver.find_element(*CheckoutLocators.ADDRESS_CONTINUE_BUTTON).click()

        time.sleep(2)

    # --------------------------------------------------------
    # Shipping method step
    # --------------------------------------------------------

    def continue_shipping_method(self):

        self.driver.find_element(*CheckoutLocators.SHIPPING_CONTINUE_BUTTON).click()

        time.sleep(3)

    # --------------------------------------------------------
    # Payment step

    # --------------------------------------------------------

    def _click_with_fallback(self, locator):

        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )

        try:
            element.click()

        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def select_payment_method(self, payment_method_name):


        mapping = {
            "Cash on Delivery": CheckoutLocators.COD_PAYMENT,
            "Check": CheckoutLocators.CHECK_PAYMENT,
            "Bank Wire": CheckoutLocators.BANK_WIRE_PAYMENT,
        }

        locator = mapping.get(payment_method_name)

        if locator is None:
            raise ValueError(f"Unknown payment method: {payment_method_name}")

        self._click_with_fallback(locator)

    def is_payment_method_selected(self, payment_method_name):

        mapping = {
            "Cash on Delivery": CheckoutLocators.COD_PAYMENT,
            "Check": CheckoutLocators.CHECK_PAYMENT,
            "Bank Wire": CheckoutLocators.BANK_WIRE_PAYMENT,
        }

        locator = mapping[payment_method_name]

        return self.driver.find_element(*locator).is_selected()

    def is_payment_option_present(self, payment_method_name):

        mapping = {
            "Cash on Delivery": CheckoutLocators.COD_PAYMENT,
            "Check": CheckoutLocators.CHECK_PAYMENT,
            "Bank Wire": CheckoutLocators.BANK_WIRE_PAYMENT,
        }

        locator = mapping[payment_method_name]

        return len(self.driver.find_elements(*locator)) > 0

    def is_payment_section_displayed(self):

        return self.driver.find_element(*CheckoutLocators.PAYMENT_SECTION).is_displayed()

    def set_terms_accepted(self, accepted):

        """
        Ensures the Terms checkbox ends up in the requested state
        (True = checked, False = unchecked), regardless of
        whatever state a previous test left it in.
        """

        currently_checked = self.is_terms_selected()

        if currently_checked != accepted:
            self.driver.find_element(*CheckoutLocators.TERMS_CHECKBOX).click()
            time.sleep(1)

    def is_terms_selected(self):

        return self.driver.find_element(*CheckoutLocators.TERMS_CHECKBOX).is_selected()

    def click_place_order(self):

        self.driver.find_element(*CheckoutLocators.PLACE_ORDER_BUTTON).click()

        time.sleep(5)

    def is_place_order_enabled(self):

        return self.driver.find_element(*CheckoutLocators.PLACE_ORDER_BUTTON).is_enabled()

    def click_place_order_button_element(self):

        """
        Returns whether a second click on Place Order was possible
        (button still present + enabled) — used by the duplicate-
        submission test. Returns False if the button is gone/disabled
        or the click otherwise fails, meaning the app prevented it.
        """

        try:
            button = self.driver.find_element(*CheckoutLocators.PLACE_ORDER_BUTTON)

            if button.is_enabled():
                button.click()
                time.sleep(2)
                return True

            return False

        except Exception:
            return False
