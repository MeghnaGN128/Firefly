from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ResetPasswordPage:
    URL = "https://test-main.cloud-kitchen.in/resetPassword"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def enter_phone(self, phone):
        input_el = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Phone Number']"))
        )
        input_el.clear()
        input_el.send_keys(phone)

    def click_send_otp(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Send OTP')]"))
        ).click()

    def wait_for_success(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'OTP sent successfully')]"))
        )
