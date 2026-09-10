from pages.kitchen_select import KitchenSelectPage


def test_kitchen_select_page(driver):
    page = KitchenSelectPage(driver)
    page.open()
    page.wait_until_loaded()

    assert page.get_options() == list(KitchenSelectPage.OPTIONS.values())
