from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import KITCHENS_SELECT_URL


class KitchenSelectPage:
    URL = KITCHENS_SELECT_URL
    CARD_SELECTOR = "div.login-cards > div.home-card"
    CENTRAL_IMAGE_SELECTOR = "div.home-card img.ckimg"
    SATELLITE_IMAGE_SELECTOR = "div.home-card img.skimg"

    OPTIONS = {
        "CK": "Central Kitchen",
        "SK": "Satellite Kitchen",
    }

    def __init__(self, driver):
        self.driver = driver

    def get_options(self):
        cards = self.driver.find_elements(By.CSS_SELECTOR, self.CARD_SELECTOR)
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

    def select_option(self, option_code):
        option_code = option_code.strip().upper()
        if option_code not in self.OPTIONS:
            raise ValueError(
                f"Unknown Kitchens option: {option_code}. "
                f"Expected one of: {', '.join(self.OPTIONS)}"
            )

        expected_label = self.OPTIONS[option_code]
        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            self.CARD_SELECTOR
        )
        for card in cards:
            if card.text.strip() == expected_label:
                card.click()
                return

        raise AssertionError(
            f"Kitchens option was not found in browser: {expected_label}"
        )

    def wait_until_option_selected(self, previous_url):
        WebDriverWait(self.driver, 20).until(
            lambda current_driver: (
                current_driver.current_url != previous_url
                or not any(
                    card.text.strip() in self.OPTIONS.values()
                    for card in current_driver.find_elements(
                        By.CSS_SELECTOR,
                        self.CARD_SELECTOR
                    )
                )
            )
        )
