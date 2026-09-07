from selenium.webdriver.common.by import By


class ODSDispatchPage:

    URL = "https://test-main.cloud-kitchen.in/odsDispatch"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def get_dispatch_items(self):
        rows = self.driver.find_elements(
            By.CSS_SELECTOR,
            "table tbody tr"
        )

        data = []

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 2:
                item = cells[0].text.strip()
                quantity = cells[1].text.strip()

                if item and quantity:
                    try:
                        quantity = float(quantity)

                        data.append({
                            "item": item,
                            "quantity": quantity
                        })

                    except ValueError:
                        pass

        return data