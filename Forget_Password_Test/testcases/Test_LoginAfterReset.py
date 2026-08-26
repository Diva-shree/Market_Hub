import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ddt import ddt, data, unpack
from utilities.ReadCSVData import ReadCSVData
from pages.LoginPage import Login

@ddt()
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://qah.bishalkarki.com/")
        self.lp = Login(self.driver)

    @data(*ReadCSVData.read_data_from_csv("PostResetLoginData.csv"))
    @unpack
    def test_login_after_reset(self, username, password, type, expectedname):
        try:
            self.lp.login(username, password)
            if type == "p":
                expectedresult = expectedname
                actualresult = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.lp.lc.lbl_welcome_selector))).text
                self.assertIn(expectedresult, actualresult, msg="Login with new password failed or welcome message is incorrect")
                print("User logged in successfully with valid credentials.")
            else:
                # Old password should be rejected - this site shows a page error, not a JS alert
                expectedresult = "Authentication failed."
                actualresult = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, self.lp.lc.lbl_login_error))).text
                self.assertIn(expectedresult, actualresult, msg="Error message is incorrect or not displayed")
                print("Old password correctly rejected after reset.")
        except Exception as e:
            self.fail(f"Test failed due to an exception: {e}")

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
