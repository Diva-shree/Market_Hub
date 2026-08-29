from selenium.webdriver.common.by import By


class HomePageLocators:

    SIGNIN_LINK = (
        By.XPATH,
        '//*[@id="_desktop_user_info"]/div/a/span'
    )

    SEARCH_BOX = (
        By.NAME,
        "s"
    )

    CART_ICON = (
        By.XPATH,
        '//*[@id="_desktop_cart"]/div/div/a/i'
    )
