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
        self.driver.get("https://qah.bishalkarki.com/login?back=https%3A%2F%2Fqah.bishalkarki.com%2F")
        self.fp = ForgotPassword(self.driver)

    @data(*ReadCSVData.read_data_from_csv("ForgetPasswordDatas.csv"))
    @unpack

    def test_forgot_password(self, email, type):
        try:
            self.fp.request_password_reset(email)
            if type == "p":
                expectedresult = f"If this email address has been registered in our store, you will receive a link to reset your password at {email}."
                actualresult = self.fp.get_confirmation_message()
                self.assertEqual(expectedresult, actualresult, msg="Reset confirmation message is incorrect")
            else:
                expectedresult = f"If this email address has been registered in our store, you will receive a link to reset your password at {email}."
                actualresult = self.fp.get_error_message()
                self.assertEqual(expectedresult, actualresult, msg="Error message is incorrect")
        except Exception as e:
            self.fail(f"Test failed due to an exception: {e}")

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
