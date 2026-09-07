from pages.resetpassword import (
    click_forgot_password,
    enter_phone,
    click_reset_get_otp,
    wait_for_reset_otp,
    enter_reset_otp,
    enter_new_password,
    enter_confirm_password,
    click_reset_password
)


def test_reset_password(driver):

    phone = input("Enter phone number: ")
    new_password = input("Enter new password: ")
    confirm_password = input("Enter confirm password: ")

    if not phone.isdigit() or len(phone) != 10:
        raise AssertionError(
            "Phone number must contain exactly 10 digits"
        )

    if new_password != confirm_password:
        raise AssertionError(
            "Confirm password does not match new password"
        )

    print("\nOpening Forgot Password...")

    click_forgot_password(driver)

    print("Entering phone number...")

    enter_phone(driver, phone)

    print("Requesting reset OTP...")

    click_reset_get_otp(driver)

    print("Waiting for OTP screen...")

    wait_for_reset_otp(driver)

    print("OTP screen opened successfully.")

    reset_otp = input(
        "Enter reset OTP when you receive it: "
    ).strip()

    if not reset_otp.isdigit() or len(reset_otp) != 6:
        raise AssertionError(
            "OTP must contain exactly 6 digits"
        )

    print("Entering reset OTP...")

    enter_reset_otp(driver, reset_otp)

    print("Entering new password...")

    enter_new_password(driver, new_password)

    enter_confirm_password(driver, confirm_password)

    print("Submitting password reset...")

    click_reset_password(driver)

    print("\nPassword reset submitted successfully.")