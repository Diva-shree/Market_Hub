import unittest

from selenium import webdriver
from ddt import ddt, data, unpack

from utilities.ReadCSVData import ReadCSVData
from pages.ForgotPasswordPage import ForgotPassword


@ddt()
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://qah.bishalkarki.com/password-recovery")
        self.fp = ForgotPassword(self.driver)

    @data(*ReadCSVData.read_data_from_csv("ForgotPasswordData.csv"))
    @unpack
    def test_forgot_password(self, email):
        try:
            self.fp.enter_email(email)
            self.fp.click_submit_button()
            expectedresult = f"If this email address has been registered in our store, you will receive a link to reset your password at {email}."
            actualresult = self.fp.get_confirmation_message()
            self.assertEqual(expectedresult, actualresult, msg="Confirmation message is incorrect")
        except Exception as e:
            self.fail(f"Test failed due to an exception: {e}")

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
