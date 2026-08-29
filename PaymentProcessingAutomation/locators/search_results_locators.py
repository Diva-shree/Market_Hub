from selenium.webdriver.common.by import By


class SearchResultsLocators:

    FIRST_PRODUCT = (
        By.XPATH,
        '//*[@id="js-product-list"]/div[1]/div/article/div/div[1]/a/picture/img'
    )
