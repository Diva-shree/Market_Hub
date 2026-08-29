from selenium.webdriver.common.by import By


class CheckoutLocators:

    # --------------------------------------------------------
    # Address step
    # --------------------------------------------------------

    ADDRESS_CONTINUE_BUTTON = (
        By.XPATH,
        '//*[@id="checkout-addresses-step"]/div/div/form/div[2]/button'
    )

    # --------------------------------------------------------
    # Shipping method step
    # --------------------------------------------------------

    SHIPPING_CONTINUE_BUTTON = (
        By.XPATH,
        '//*[@id="js-delivery"]/button'
    )

    # --------------------------------------------------------
    # Payment step
    #
    # NOTE: PrestaShop's checkout is a single page with several
    # steps stacked on it (address / shipping / payment) — there
    # is no separate "Payment" page/URL, so its locators live
    # here in CheckoutLocators rather than in their own file.
    #
    # Confirmed correct IDs (verified in DevTools):
    #   payment-option-2 = Cash on Delivery
    #   payment-option-3 = Check
    #   payment-option-1 = Bank Wire
    # --------------------------------------------------------

    PAYMENT_SECTION = (
        By.XPATH,
        '//*[@id="checkout-payment-step"]'
    )

    COD_PAYMENT = (
        By.XPATH,
        '//*[@id="payment-option-2"]'
    )

    CHECK_PAYMENT = (
        By.XPATH,
        '//*[@id="payment-option-3"]'
    )

    BANK_WIRE_PAYMENT = (
        By.XPATH,
        '//*[@id="payment-option-1"]'
    )

    TERMS_CHECKBOX = (
        By.XPATH,
        '//*[@id="conditions_to_approve[terms-and-conditions]"]'
    )

    PLACE_ORDER_BUTTON = (
        By.XPATH,
        '//*[@id="payment-confirmation"]/div[1]/button'
    )
