from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def click_forgot_password(driver):
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'forgot password')]"
            )
        )
    ).click()


def enter_phone(driver, phone):
    phone_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input.phone")
        )
    )

    phone_input.clear()
    phone_input.send_keys(phone)


def click_reset_get_otp(driver):
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.resend-otp")
        )
    ).click()


def wait_for_reset_otp(driver):
    WebDriverWait(driver, 20).until(
        lambda d: len(
            d.find_elements(By.CSS_SELECTOR, "input.otp")
        ) == 6
    )


def enter_reset_otp(driver, otp):
    otp_inputs = WebDriverWait(driver, 20).until(
        lambda d: d.find_elements(By.CSS_SELECTOR, "input.otp")
    )

    if len(otp_inputs) != 6:
        raise AssertionError(
            f"Expected 6 OTP fields, found {len(otp_inputs)}"
        )

    for i, digit in enumerate(otp):
        otp_inputs[i].clear()
        otp_inputs[i].send_keys(digit)


def enter_new_password(driver, password):
    password_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='New Password']")
        )
    )

    password_input.clear()
    password_input.send_keys(password)


def enter_confirm_password(driver, password):
    confirm_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Confirm Password']")
        )
    )

    confirm_input.clear()
    confirm_input.send_keys(password)


def click_reset_password(driver):
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reset password') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit')]"
            )
        )
    ).click()