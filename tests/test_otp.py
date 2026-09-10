from pages.otp import enter_otp, click_verify
from pages.home_select import HomeSelectPage
from pages.kitchen_select import KitchenSelectPage
from utils.otp_validate import validate_otp
from utils.api_clients import verify_otp


def test_otp(login_to_otp):
    driver, phone = login_to_otp

    otp = input("Enter OTP: ")

    errors = validate_otp(otp)

    if errors:
        raise AssertionError(
            "\n".join(
                f"{error}"
                for error in errors
            )
        )

    print("\nOTP validation:")
    print("6 digits           PASS")
    print("Numbers only       PASS")

    response = verify_otp(phone, otp)

    if not response.ok:
        raise AssertionError(
            f"OTP verification request failed\n"
            f"Phone number: {phone}\n"
            f"Backend status: {response.status_code}\n"
            f"Response: {response.text}"
        )

    try:
        data = response.json()
    except ValueError as error:
        raise AssertionError(
            "OTP verification returned a non-JSON response\n"
            f"Backend status: {response.status_code}\n"
            f"Response: {response.text}"
        ) from error

    message = data.get("message", "")

    if message.lower() != "login successful":
        raise AssertionError(
            f"OTP verification failed\n"
            f"Phone number: {phone}\n"
            f"Reason: {message}\n"
            f"Backend status: {response.status_code}"
        )

    print("\nBackend OTP verification:")
    print("OTP matched       PASS")
    print("Login successful  PASS")

    enter_otp(driver, otp)
    click_verify(driver)

    home_page = HomeSelectPage(driver)
    home_page.wait_until_loaded()

    expected_url = home_page.URL

    if driver.current_url.rstrip("/") != expected_url.rstrip("/"):
        raise AssertionError(
            f"Browser login did not reach Home Select page\n"
            f"Expected URL: {expected_url}\n"
            f"Actual URL: {driver.current_url}"
        )

    options = home_page.get_options()

    if options != list(HomeSelectPage.OPTIONS):
        raise AssertionError(
            f"Home Select page did not load correctly\n"
            f"Expected options: {list(HomeSelectPage.OPTIONS)}\n"
            f"Actual options: {options}"
        )

    # The actual page option is selected in the browser by clicking the UI card,
    # not by asking the terminal which card should be chosen.
    selected_option = "Kitchens"
    kitchen_option = "CK"

    if selected_option not in HomeSelectPage.OPTIONS:
        raise ValueError(
            f"Unknown home option: {selected_option}. "
            f"Expected one of: {', '.join(HomeSelectPage.OPTIONS)}"
        )

    if selected_option == "Kitchens":
        kitchen_option = home_page.validate_kitchen_option(kitchen_option)

    home_page.validate_backend_selection(
        data,
        selected_option,
        kitchen_option
    )

    home_previous_url = driver.current_url
    home_page.select_option(selected_option)
    home_page.wait_until_option_selected(home_previous_url)

    if kitchen_option:
        kitchen_page = KitchenSelectPage(driver)
        kitchen_page.wait_until_loaded()

        kitchen_options = kitchen_page.get_options()
        expected_kitchen_options = list(KitchenSelectPage.OPTIONS.values())
        if kitchen_options != expected_kitchen_options:
            raise AssertionError(
                "Kitchens selection page did not load correctly\n"
                f"Expected options: {expected_kitchen_options}\n"
                f"Actual options: {kitchen_options}"
            )

        kitchen_previous_url = driver.current_url
        kitchen_page.select_option(kitchen_option)
        kitchen_page.wait_until_option_selected(kitchen_previous_url)

    print("\nBrowser login verification:")
    print("OTP entered          PASS")
    print("Verify button clicked PASS")
    print("Home page loaded      PASS")
    print(f"{selected_option} selected     PASS")
    if kitchen_option:
        print(f"{kitchen_option} selected          PASS")
    print("Browser login         PASS")