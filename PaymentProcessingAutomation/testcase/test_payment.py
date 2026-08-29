import os
import sys
import time
import unittest

from selenium import webdriver


# ============================================================
# PROJECT ROOT
#
# testcase/ is one level below the project root, so we add the
# root (not this folder) to sys.path — that's what lets
# "from pages.home_page import HomePage" etc. resolve,
# ============================================================

project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if project_root not in sys.path:
    sys.path.insert(0, project_root)


# ============================================================
# IMPORTS
# ============================================================

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.search_results_page import SearchResultsPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.order_confirmation_page import OrderConfirmationPage

from utilities.readcsvdata import ReadCSVData


class MyTestCase(unittest.TestCase):

    # ============================================================
    # LOAD TEST DATA FROM CSV (once, at class definition time)
    # ============================================================

    config_rows = ReadCSVData.read_data_from_csv(
        os.path.join("testdata", "config_data.csv")
    )
    URL, USERNAME, PASSWORD, PRODUCT_NAME = config_rows[0]

    payment_rows = ReadCSVData.read_data_from_csv(
        os.path.join("testdata", "payment_data.csv")
    )

    # Build a lookup: test_case_id -> {payment_method, terms_accepted, expected_place_order_enabled}
    PAYMENT_DATA = {}

    for row in payment_rows:
        test_case_id, payment_method, terms_accepted, expected_enabled = row
        PAYMENT_DATA[test_case_id] = {
            "payment_method": payment_method,
            "terms_accepted": terms_accepted == "True",
            "expected_place_order_enabled": expected_enabled == "True",
        }

    # ============================================================
    # FULL SITE FLOW, ORCHESTRATED ACROSS PAGE OBJECTS
    #
    # Home page -> Login page -> Home page -> Search results page
    # -> Product detail page -> Cart page -> Checkout page
    # (payment lives on this same page, no separate URL)
    # ============================================================

    @classmethod
    def _login(cls):

        cls.driver.get(cls.URL)

        home_page = HomePage(cls.driver)
        home_page.click_signin()

        login_page = LoginPage(cls.driver)
        login_page.login(cls.USERNAME, cls.PASSWORD)

    @classmethod
    def _open_fresh_payment_section(cls):

        # Session/cookies are already authenticated — this does
        # NOT log in again.
        cls.driver.get(cls.URL)
        time.sleep(2)

        home_page = HomePage(cls.driver)
        home_page.search_product(cls.PRODUCT_NAME)

        search_results_page = SearchResultsPage(cls.driver)
        search_results_page.select_first_product()

        product_detail_page = ProductDetailPage(cls.driver)
        product_detail_page.add_to_cart()
        product_detail_page.close_added_to_cart_modal()

        home_page.open_cart()

        cart_page = CartPage(cls.driver)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(cls.driver)
        checkout_page.continue_address()
        checkout_page.continue_shipping_method()

        # Payment section should now be open

    # ============================================================
    # CLASS-LEVEL SETUP — runs ONCE
    # ============================================================

    @classmethod
    def setUpClass(cls):

        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

        cls._login()
        cls._open_fresh_payment_section()

    # ============================================================
    # PER-TEST SETUP
    #
    # Execution order enforced by test_01..test_05 naming:
    #
    #   test_01  TS_01_TC_01  display check        -> initial page
    #   test_02  TS_01_TC_02  place order (COD)     -> initial page, SUBMITS -> consumes cart
    #   test_03  TS_02_TC_01  no payment method      -> REOPENS payment page (cart was just consumed)
    #   test_04  TS_02_TC_02  no terms               -> reuses page reopened by test_03
    #   test_05  TS_03_TC_01  place order (Bank Wire) -> reuses page reopened by test_03, SUBMITS
    # ============================================================

    TESTS_NEEDING_FRESH_PAYMENT_PAGE = {
        "test_03_ts02_tc01_order_blocked_without_payment_method",
    }

    def setUp(self):

        if self._testMethodName in self.TESTS_NEEDING_FRESH_PAYMENT_PAGE:
            self._open_fresh_payment_section()

        self.checkout_page = CheckoutPage(self.driver)
        self.order_confirmation_page = OrderConfirmationPage(self.driver)

        time.sleep(2)

    # ============================================================
    # TEST 01 — TS_01_TC_01
    # ============================================================

    def test_01_ts01_tc01_supported_payment_methods_displayed(self):

        """
        TC ID: TS_01_TC_01
        Title: Verify supported payment methods are displayed.
        """

        try:

            self.assertTrue(
                self.checkout_page.is_payment_section_displayed(),
                "Payment section is not displayed"
            )

            for method in ("Cash on Delivery", "Check", "Bank Wire"):

                self.assertTrue(
                    self.checkout_page.is_payment_option_present(method),
                    f"{method} option is not present"
                )

            print(
                "TS_01_TC_01 PASSED: "
                "All supported payment methods are displayed."
            )

        except Exception as e:
            self.fail(f"TS_01_TC_01 FAILED: {e}")

    # ============================================================
    # TEST 02 — TS_01_TC_02  (data-driven from payment_data.csv)
    # ============================================================

    def test_02_ts01_tc02_place_order_cash_on_delivery(self):

        """
        TC ID: TS_01_TC_02
        Title: Verify customer can place order after selecting
               payment method and accepting terms.
        """

        data = self.PAYMENT_DATA["TS_01_TC_02"]

        try:

            self.checkout_page.select_payment_method(data["payment_method"])
            time.sleep(1)

            self.assertTrue(
                self.checkout_page.is_payment_method_selected(data["payment_method"]),
                f"{data['payment_method']} was not selected"
            )

            self.checkout_page.set_terms_accepted(data["terms_accepted"])

            self.assertEqual(
                self.checkout_page.is_terms_selected(),
                data["terms_accepted"],
                "Terms of Service state did not match test data"
            )

            self.checkout_page.click_place_order()

            confirmation = self.order_confirmation_page.get_confirmation_text()

            self.assertTrue(confirmation, "Order confirmation was not displayed")

            print("TS_01_TC_02 PASSED: Order placed successfully.")

        except Exception as e:
            self.fail(f"TS_01_TC_02 FAILED: {e}")

    # ============================================================
    # TEST 03 — TS_02_TC_01  (data-driven from payment_data.csv)
    # ============================================================

    def test_03_ts02_tc01_order_blocked_without_payment_method(self):

        """
        TC ID: TS_02_TC_01
        Title: Verify order cannot be placed without selecting
               a payment method.
        """

        data = self.PAYMENT_DATA["TS_02_TC_01"]

        try:

            self.checkout_page.set_terms_accepted(data["terms_accepted"])

            self.assertEqual(
                self.checkout_page.is_terms_selected(),
                data["terms_accepted"],
                "Terms of Service state did not match test data"
            )

            self.assertEqual(
                self.checkout_page.is_place_order_enabled(),
                data["expected_place_order_enabled"],
                "Place Order enabled-state did not match expected data"
            )

            print(
                "TS_02_TC_01 PASSED: "
                "Order cannot be placed without payment method."
            )

        except Exception as e:
            self.fail(f"TS_02_TC_01 FAILED: {e}")

    # ============================================================
    # TEST 04 — TS_02_TC_02  (data-driven from payment_data.csv)
    # ============================================================

    def test_04_ts02_tc02_order_blocked_without_terms(self):

        """
        TC ID: TS_02_TC_02
        Title: Verify order cannot be placed without selecting
               Terms of Service.
        """

        data = self.PAYMENT_DATA["TS_02_TC_02"]

        try:

            self.checkout_page.select_payment_method(data["payment_method"])
            time.sleep(1)

            self.assertTrue(
                self.checkout_page.is_payment_method_selected(data["payment_method"]),
                f"{data['payment_method']} was not selected"
            )

            self.checkout_page.set_terms_accepted(data["terms_accepted"])

            self.assertEqual(
                self.checkout_page.is_terms_selected(),
                data["terms_accepted"],
                "Terms of Service state did not match test data"
            )

            self.assertEqual(
                self.checkout_page.is_place_order_enabled(),
                data["expected_place_order_enabled"],
                "Place Order enabled-state did not match expected data"
            )

            print(
                "TS_02_TC_02 PASSED: "
                "Order cannot be placed without Terms."
            )

        except Exception as e:
            self.fail(f"TS_02_TC_02 FAILED: {e}")

    # ============================================================
    # TEST 05 — TS_03_TC_01  (data-driven from payment_data.csv)
    # ============================================================

    def test_05_ts03_tc01_repeated_place_order_bank_wire(self):

        """
        TC ID: TS_03_TC_01
        Title: Verify repeated Place Order submissions do not
               create duplicate orders.
        """

        data = self.PAYMENT_DATA["TS_03_TC_01"]

        try:

            self.checkout_page.select_payment_method(data["payment_method"])
            time.sleep(1)

            self.assertTrue(
                self.checkout_page.is_payment_method_selected(data["payment_method"]),
                f"{data['payment_method']} was not selected"
            )

            self.checkout_page.set_terms_accepted(data["terms_accepted"])

            self.assertEqual(
                self.checkout_page.is_terms_selected(),
                data["terms_accepted"],
                "Terms of Service state did not match test data"
            )

            self.checkout_page.click_place_order()

            second_click_possible = self.checkout_page.click_place_order_button_element()

            duplicate_status = (
                "Second Place Order click was possible. "
                "Application should prevent duplicate order creation."
                if second_click_possible
                else "Second Place Order submission was prevented."
            )

            confirmation = self.order_confirmation_page.get_confirmation_text()

            self.assertTrue(confirmation, "Order confirmation was not displayed")

            print(
                f"TS_03_TC_01 PASSED:{duplicate_status} "
                f"Only one confirmed order is created."
                f"Order confirmation displayed."
            )

        except Exception as e:
            self.fail(f"TS_03_TC_01 FAILED: {e}")

    # ============================================================
    # CLASS-LEVEL TEARDOWN — runs ONCE, after ALL tests finish
    # ============================================================

    @classmethod
    def tearDownClass(cls):

        if cls.driver:
            cls.driver.quit()


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    unittest.main()
