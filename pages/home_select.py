from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import HOME_SELECT_URL


class HomeSelectPage:
    URL = HOME_SELECT_URL
    CARD_SELECTOR = "div.login-cards > div.home-card"
    KITCHEN_CARD_SELECTOR = "div.login-cards > div.home-card"

    OPTIONS = (
        "Admin",
        "Kitchens",
        "HRMS",
        "Audit",
        "Learning and Development",
    )
    KITCHEN_OPTIONS = ("CK", "SK")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def get_options(self):
        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            self.CARD_SELECTOR
        )
        return [card.text.strip() for card in cards]

    def wait_until_loaded(self):
        WebDriverWait(self.driver, 20).until(
            lambda current_driver: (
                current_driver.current_url.rstrip("/")
                == self.URL.rstrip("/")
                and len(
                    current_driver.find_elements(
                        By.CSS_SELECTOR,
                        self.CARD_SELECTOR
                    )
                ) == len(self.OPTIONS)
            )
        )

    def select_option(self, option_name):
        if option_name not in self.OPTIONS:
            raise ValueError(
                f"Unknown home option: {option_name}. "
                f"Expected one of: {', '.join(self.OPTIONS)}"
            )

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            self.CARD_SELECTOR
        )

        for card in cards:
            if card.text.strip() == option_name:
                card.click()
                return

        raise AssertionError(
            f"Home option was not found: {option_name}"
        )

    def validate_kitchen_option(self, kitchen_option):
        kitchen_option = kitchen_option.strip().upper()
        if kitchen_option not in self.KITCHEN_OPTIONS:
            raise ValueError(
                f"Unknown Kitchens option: {kitchen_option}. "
                f"Expected one of: {', '.join(self.KITCHEN_OPTIONS)}"
            )
        return kitchen_option

    def validate_backend_selection(self, backend_data, option_name, kitchen_option=None):
        permissions = {
            permission.lower()
            for permission in backend_data.get("user_perm", [])
        }

        required_permission = (
            kitchen_option.lower()
            if option_name == "Kitchens" and kitchen_option
            else option_name.lower()
        )

        if required_permission not in permissions:
            raise AssertionError(
                f"Backend does not grant permission for {required_permission}. "
                f"Backend permissions: {sorted(permissions)}"
            )

    def select_kitchen_option(self, kitchen_option):
        kitchen_option = self.validate_kitchen_option(kitchen_option)
        WebDriverWait(self.driver, 20).until(
            lambda current_driver: len(
                current_driver.find_elements(
                    By.CSS_SELECTOR,
                    self.KITCHEN_CARD_SELECTOR
                )
            ) == len(self.KITCHEN_OPTIONS)
        )

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            self.KITCHEN_CARD_SELECTOR
        )
        for card in cards:
            if card.text.strip().upper() == kitchen_option:
                card.click()
                return

        raise AssertionError(
            f"Kitchens option was not found in browser: {kitchen_option}"
        )

    def wait_until_option_selected(self, previous_url):
        WebDriverWait(self.driver, 20).until(
            lambda current_driver: (
                current_driver.current_url != previous_url
                or not any(
                    card.text.strip() in self.OPTIONS
                    for card in current_driver.find_elements(
                        By.CSS_SELECTOR,
                        self.CARD_SELECTOR
                    )
                )
            )
        )