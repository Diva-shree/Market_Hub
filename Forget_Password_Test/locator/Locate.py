class Locator:
    # ---- Login page locators (existing) ----
    login_nav = "Sign in"
    txt_uname_id = "field-email"
    txt_pswd_id = "field-password"
    btn_login_xpath = '//*[@id="submit-login"]'
    lbl_welcome_selector = "#_desktop_user_info .account span.hidden-sm-down"
    lbl_login_error = "alert-danger"

    # ---- Forgot Password page locators ----
    link_forgot_password_text = "Forgot your password?"
    txt_email_id = "email"
    btn_submit_id = "send-reset-link"
    lbl_confirmation_class = "ps-alert-success"
    lbl_error_class = "ps-alert-error"


    # ---- Reset Password page locators ----
    txt_new_password_name = "passwd"
    txt_confirm_password_name = "confirmation"
    btn_reset_password_name = "submit"
    lbl_reset_success_class = "alert-success"
    lbl_reset_error_class = "ps-alert-error"
