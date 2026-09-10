from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def enter_otp(driver, otp):

    if not otp.isdigit():
        raise AssertionError("OTP must contain only numbers")

    if len(otp) != 6:
        raise AssertionError("OTP must contain exactly 6 digits")

    otp_inputs = WebDriverWait(driver, 20).until(
        lambda current_driver: current_driver.find_elements(
            By.CSS_SELECTOR,
            "input.otp"
        )
    )

    if len(otp_inputs) != 6:
        raise AssertionError(
            f"Expected 6 OTP fields but found {len(otp_inputs)}"
        )

    for i in range(6):
        otp_inputs[i].clear()
        otp_inputs[i].send_keys(otp[i])


def click_verify(driver):
    driver.find_element(
        By.CSS_SELECTOR,
        "button.verify"
    ).click()


def wait_for_login_success(driver, previous_url):
    WebDriverWait(driver, 20).until(
        lambda current_driver: (
            current_driver.current_url != previous_url
            and not current_driver.find_elements(
                By.CSS_SELECTOR,
                "input.otp"
            )
        )
    )


def click_resend_otp(driver):
    driver.find_element(
        By.CSS_SELECTOR,
        "a.resend-otp"
    ).click()