from selenium.webdriver.common.by import By


class CKRequisitionPage:

    URL = "https://test-main.cloud-kitchen.in/ckRequisition"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

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

        for item, quantity in zip(item_elements, quantity_elements):
            item_name = item.get_attribute("value").strip()
            qty = quantity.get_attribute("value").strip()

            if item_name and qty:
                data.append({
                    "item": item_name,
                    "quantity": float(qty)
                })

        return data