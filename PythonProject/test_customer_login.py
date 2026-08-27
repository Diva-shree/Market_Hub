import pytest

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from login_page import LoginPage


# ============================================================
# Test Setup
# ============================================================

@pytest.fixture
def driver():

    driver = webdriver.Chrome()

    driver.maximize_window()

    yield driver

    driver.quit()


# ============================================================
# TC-01
# Login with valid email and valid password
# ============================================================

def test_valid_login(driver):

    login_page = LoginPage(driver)

    # Step 1: Open Login page
    login_page.open_login_page()

    # Step 2: Enter valid email and password
    login_page.login(
        "divashreerana@gmail.com",
        "NewPass@123!"
    )

    # Step 3: Wait for successful login
    WebDriverWait(driver, 10).until(
        lambda d: "/my-account" in d.current_url.lower()
    )

    # Verify redirection to My Account
    assert "/my-account" in driver.current_url.lower()

    print(
        "TC-01 PASSED: Login with valid credentials successful"
    )


# ============================================================
# TC-02
# Login with incorrect password
# ============================================================

def test_invalid_password(driver):

    login_page = LoginPage(driver)

    # Step 1: Open Login page
    login_page.open_login_page()

    # Step 2: Enter valid email and incorrect password
    login_page.login(
        "divashreerana@gmail.com",
        "Test!123@"
    )

    # Step 3: Get error message
    error_message = login_page.get_error_message()

    print(
        "Error message:",
        error_message
    )

    # Verify appropriate error message
    assert "Authentication failed" in error_message

    # Verify login failed
    assert "/my-account" not in driver.current_url.lower()

    print(
        "TC-02 PASSED: Incorrect password rejected"
    )


# ============================================================
# TC-03
# Login with unregistered email
# ============================================================

def test_unregistered_email(driver):

    login_page = LoginPage(driver)

    # Step 1: Open Login page
    login_page.open_login_page()

    # Step 2: Enter unregistered email and password
    login_page.login(
        "test@gmail.com",
        "NewPass@123!"
    )

    # Step 3: Get error message
    error_message = login_page.get_error_message()

    print(
        "Error message:",
        error_message
    )

    # Verify appropriate error message
    assert "Authentication failed" in error_message

    # Verify login failed
    assert "/my-account" not in driver.current_url.lower()

    print(
        "TC-03 PASSED: Unregistered email rejected"
    )


# ============================================================
# TC-04
# Access My Account without login
# ============================================================

def test_access_my_account_without_login(driver):

    # Open My Account directly without logging in
    driver.get(
        "https://qah.bishalkarki.com/my-account"
    )

    # Wait for page to finish loading
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    print(
        "Current URL:",
        driver.current_url
    )

    # Expected:
    # Customer should be redirected to login page
    assert "/login" in driver.current_url.lower()

    print(
        "TC-04 PASSED: Unauthenticated user redirected to login"
    )


# ============================================================
# TC-06
# Check session after successful login,
# refresh and navigation
# ============================================================

def test_session_after_login_refresh_and_navigation(driver):

    login_page = LoginPage(driver)

    # --------------------------------------------------------
    # Step 1: Open Login page
    # --------------------------------------------------------

    login_page.open_login_page()

    # --------------------------------------------------------
    # Step 2: Login successfully
    # --------------------------------------------------------

    login_page.login(
        "divashreerana@gmail.com",
        "NewPass@123!"
    )

    # Wait for successful login
    WebDriverWait(driver, 10).until(
        lambda d: "/my-account" in d.current_url.lower()
    )

    # Verify successful login
    assert "/my-account" in driver.current_url.lower()

    print(
        "User logged in successfully"
    )

    # --------------------------------------------------------
    # Step 3: Refresh the page
    # --------------------------------------------------------

    driver.refresh()

    # Wait for refresh to finish
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    # Verify session is still active
    assert "/my-account" in driver.current_url.lower()

    print(
        "Session maintained after refresh"
    )

    # --------------------------------------------------------
    # Step 4: Navigate to another page
    # --------------------------------------------------------

    driver.get(
        "https://qah.bishalkarki.com/"
    )

    # Wait for home page
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    print(
        "Navigated to home page"
    )

    # --------------------------------------------------------
    # Step 5: Return to My Account
    # --------------------------------------------------------

    driver.get(
        "https://qah.bishalkarki.com/my-account"
    )

    # Wait for My Account
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    # Verify session is still active
    assert "/my-account" in driver.current_url.lower()

    print(
        "TC-06 PASSED: Session maintained after "
        "refresh and navigation"
    )


# ============================================================
# TC-07
# Check session after logout
# ============================================================

def test_logout(driver):

    login_page = LoginPage(driver)

    # --------------------------------------------------------
    # Step 1: Open Login page
    # --------------------------------------------------------

    login_page.open_login_page()

    # --------------------------------------------------------
    # Step 2: Login successfully
    # --------------------------------------------------------

    login_page.login(
        "divashreerana@gmail.com",
        "NewPass@123!"
    )

    # Wait for successful login
    WebDriverWait(driver, 10).until(
        lambda d: "/my-account" in d.current_url.lower()
    )

    # Verify customer is logged in
    assert "/my-account" in driver.current_url.lower()

    print(
        "User logged in successfully"
    )

    # --------------------------------------------------------
    # Step 3: Logout
    # --------------------------------------------------------

    login_page.logout()

    # Wait for logout
    WebDriverWait(driver, 10).until(
        lambda d: "/my-account" not in d.current_url.lower()
    )

    print(
        "URL after logout:",
        driver.current_url
    )

    # --------------------------------------------------------
    # Step 4: Verify user is logged out
    # --------------------------------------------------------

    assert "/my-account" not in driver.current_url.lower()

    print(
        "TC-07 PASSED: User logged out successfully"
    )