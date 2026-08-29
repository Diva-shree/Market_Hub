import time

from locators.search_results_locators import SearchResultsLocators


class SearchResultsPage:

    def __init__(self, driver):
        self.driver = driver

    def select_first_product(self):

        self.driver.find_element(*SearchResultsLocators.FIRST_PRODUCT).click()

        time.sleep(2)
