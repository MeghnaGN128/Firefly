from selenium.webdriver.common.by import By


def enter_phone(driver, phone):
    driver.find_element(
        By.CSS_SELECTOR,
        "input.phone"
    ).send_keys(phone)


def enter_password(driver, password):
    driver.find_element(
        By.CSS_SELECTOR,
        "input.user-password"
    ).send_keys(password)


def click_get_otp(driver):
    driver.find_element(
        By.CSS_SELECTOR,
        "button.otp-button"
    ).click()