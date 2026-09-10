from pages.home_select import HomeSelectPage


def test_home_select_page(driver):
    page = HomeSelectPage(driver)
    page.open()
    page.wait_until_loaded()

    assert page.get_options() == list(HomeSelectPage.OPTIONS)
