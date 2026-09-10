from typing import Any

from conftest import driver
from pages.otp import enter_otp, click_verify
from pages.home_select import HomeSelectPage
from pages.kitchen_select import KitchenSelectPage
from pages.ck_requisition import CKRequisitionPage
from utils.otp_validate import validate_otp
from utils.api_clients import verify_otp


def test_ck_requisition_flow(login_to_otp: tuple[Any, str]):
    driver, phone = login_to_otp

    otp = input("Enter OTP: ")

    errors = validate_otp(otp)

    if errors:
        raise AssertionError(
            "\n".join(errors)
        )

    print("\nOTP validation:")
    print("6 digits           PASS")
    print("Numbers only       PASS")

    response = verify_otp(phone, otp)

    if not response.ok:
        raise AssertionError(
            f"OTP verification request failed\n"
            f"Phone: {phone}\n"
            f"Status: {response.status_code}\n"
            f"Response: {response.text}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise AssertionError(
            "OTP verification returned non-JSON response\n"
            f"Status: {response.status_code}\n"
            f"Response: {response.text}"
        ) from exc

    message = data.get("message", "").lower()

    if message != "login successful":
        raise AssertionError(
            f"Backend OTP validation failed\n"
            f"Phone: {phone}\n"
            f"Message: {message}"
        )

    print("\nBackend OTP verification:")
    print("OTP matched       PASS")
    print("Login successful  PASS")

    enter_otp(driver, otp)
    click_verify(driver)

    home_page = HomeSelectPage(driver)

    home_page.wait_until_loaded()

    assert driver.current_url.rstrip("/") == (
        home_page.URL.rstrip("/")
    )

    assert home_page.get_options() == list(
        HomeSelectPage.OPTIONS
    )

    print("\nHome page verification:")
    print("Home page loaded   PASS")

    previous_url = driver.current_url

    home_page.select_option("Kitchens")
    home_page.wait_until_option_selected(previous_url)

    kitchen_page = KitchenSelectPage(driver)

    kitchen_page.wait_until_loaded()

    assert kitchen_page.get_options() == list(
        KitchenSelectPage.OPTIONS.values()
    )

    print("\nKitchens verification:")
    print("Kitchens page loaded   PASS")

    previous_url = driver.current_url

    kitchen_page.select_option("CK")
    kitchen_page.wait_until_option_selected(previous_url)

    print("CK selected             PASS")

    ck_page = CKRequisitionPage(driver)

    outlet_name = "Central Kitchen MCC bangalore"

    ck_page.select_outlet(outlet_name)

    print(f"Outlet selected         PASS: {outlet_name}")

    ck_page.click_operations()

    print("Operations opened       PASS")
    print("Window handles:", driver.window_handles)
    print("Current window:", driver.current_window_handle)
    print("Current URL:", driver.current_url)

    ck_page.click_ck_requisition()

    print("CK Requisition opened   PASS")

    ck_page.click_add_item()

    print("Add Item opened         PASS")

    print("\nOTP + Home + Kitchens + CK + Outlet + Operations + CK Requisition flow completed successfully")