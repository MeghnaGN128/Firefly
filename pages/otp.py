from selenium.webdriver.common.by import By


def enter_otp(driver, otp):

    otp_inputs = driver.find_elements(By.CSS_SELECTOR, "input.otp")

    if len(otp_inputs) != 6:
        raise AssertionError(
            f"Expected 6 OTP fields but found {len(otp_inputs)}"
        )

    if not otp.isdigit():
        raise AssertionError("OTP must contain only numbers")

    if len(otp) != 6:
        raise AssertionError("OTP must contain exactly 6 digits")

    for i in range(6):
        otp_inputs[i].send_keys(otp[i])


def click_verify(driver):
    driver.find_element(
        By.CSS_SELECTOR,
        "button.verify"
    ).click()


def click_resend_otp(driver):
    driver.find_element(
        By.CSS_SELECTOR,
        "a.resend-otp"
    ).click()