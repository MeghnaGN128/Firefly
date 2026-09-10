from pages.resetpassword import ResetPasswordPage


def test_reset_password_flow(driver):
    page = ResetPasswordPage(driver)
    page.open()
    page.enter_phone("9741712973")
    page.click_send_otp()
    page.wait_for_success()
