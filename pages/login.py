from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def enter_phone(driver, phone):
    phone_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input.phone"))
    )
    phone_input.clear()
    phone_input.send_keys(phone)


def enter_password(driver, password):
    password_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input.user-password"))
    )
    password_input.clear()
    password_input.send_keys(password)


def click_get_otp(driver):
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.otp-button"))
    ).click()

    WebDriverWait(driver, 20).until(
        lambda current_driver: current_driver.find_elements(By.CSS_SELECTOR, "input.otp")
    )