import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CKRequisitionPage:

    URL = "https://test-main.cloud-kitchen.in/ckRequisition"

    ADD_ITEM_SELECTOR = (
        "//div[contains(@class, 'add-req-item') or "
        "contains(normalize-space(string(.)), 'Add Item')]"
    )

    ITEM_MODE_SWITCH_SELECTOR = "div.react-switch-handle"
    ITEM_SEARCH_SELECTOR = "input.input-item-req[placeholder='Search Items']"
    OUTLET_DROPDOWN_SELECTOR = "div.outletsDiv > div"

    OPERATIONS_SELECTOR = (
        "//*[normalize-space(text())='Operations']"
    )

    CK_REQUISITION_SELECTOR = (
        "//*[normalize-space(text())='CK Requisition']"
    )

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def select_outlet(self, outlet_name):
        WebDriverWait(self.driver, 20).until(
            lambda d: any(
                outlet_name.lower() in option.text.lower()
                for option in d.find_elements(
                    By.CSS_SELECTOR,
                    self.OUTLET_DROPDOWN_SELECTOR
                )
            )
        )

        for option in self.driver.find_elements(
            By.CSS_SELECTOR,
            self.OUTLET_DROPDOWN_SELECTOR
        ):
            if outlet_name.lower() in option.text.lower():
                option.click()
                return

        raise AssertionError(
            f"Outlet not found: {outlet_name}"
        )

    def _find_visible_text_element(self, text_fragment):
        text_fragment = text_fragment.strip().lower()

        for element in self.driver.find_elements(By.XPATH, "//*"):
            try:
                if not element.is_displayed():
                    continue
                if text_fragment in (element.text or "").strip().lower():
                    return element
            except (StaleElementReferenceException, NoSuchElementException):
                continue

        return None

    def wait_for_menu_item(self, text_fragment, timeout=20):
        WebDriverWait(self.driver, timeout).until(
            lambda d: self._find_visible_text_element(text_fragment) is not None
        )

    def click_menu_item(self, text_fragment, timeout=20):
        end_time = time.time() + timeout

        while time.time() < end_time:
            element = self._find_visible_text_element(text_fragment)
            if element is None:
                time.sleep(0.2)
                continue

            try:
                element.click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException):
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    return
                except Exception:
                    time.sleep(0.2)

        raise AssertionError(f"Could not click menu item: {text_fragment}")

    def wait_for_operations(self):
        self.wait_for_menu_item("Operations")

    def click_operations(self):
        self.wait_for_operations()
        self.click_menu_item("Operations")

    def wait_for_ck_requisition(self):
        self.wait_for_menu_item("CK Requisition")

    def click_ck_requisition(self):
        self.wait_for_ck_requisition()
        self.click_menu_item("CK Requisition")

    def click_add_item(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, self.ADD_ITEM_SELECTOR)
            )
        ).click()

    def click_item_mode_switch(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, self.ITEM_MODE_SWITCH_SELECTOR)
            )
        ).click()

    def search_item(self, item_name):
        item_input = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.ITEM_SEARCH_SELECTOR)
            )
        )

        item_input.clear()
        item_input.send_keys(item_name)

    def get_requisition_items(self):
        item_elements = self.driver.find_elements(
            By.CSS_SELECTOR,
            "input.input-item-req"
        )

        quantity_elements = self.driver.find_elements(
            By.CSS_SELECTOR,
            "input.input-quantity"
        )

        data = []

        for item, quantity in zip(
            item_elements,
            quantity_elements
        ):
            item_name = item.get_attribute("value").strip()
            qty = quantity.get_attribute("value").strip()

            if item_name and qty:
                data.append({
                    "item": item_name,
                    "quantity": float(qty)
                })

        return data