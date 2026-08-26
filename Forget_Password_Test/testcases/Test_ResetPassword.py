import unittest

from selenium import webdriver
from ddt import ddt, data, unpack

from utilities.ReadCSVData import ReadCSVData
from pages.ResetPasswordPage import ResetPassword


@ddt()
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # service like Mailinator/Mailosaur, or a pre-generated test link) - Selenium
        # cannot read the reset email itself, only drive the browser once it has the link.
        self.driver.get("https://qah.bishalkarki.com/password-recovery?token=3e5a1629dbb35841326af065038023aa&id_customer=15&reset_token=5721126824501a879d7eac91ccec734f327c9708")
        self.rp = ResetPassword(self.driver)

    @data(*ReadCSVData.read_data_from_csv("ResetPasswordData.csv"))
    @unpack
    def test_reset_password(self, newpassword, confirmpassword, type):
        try:
            self.rp.reset_password(newpassword, confirmpassword)
            if type == "p":
                expectedresult = "Your password has been successfully reset"
                actualresult = self.rp.get_success_message()
                self.assertIn(expectedresult, actualresult, msg="Success message is incorrect")
            else:

                expectedresult = "The confirmation password doesn't match"
                actualresult = self.rp.get_error_message()
                self.assertIn(expectedresult, actualresult, msg="Error message is incorrect")
        except Exception as e:
            self.fail(f"Test failed due to an exception: {e}")

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
