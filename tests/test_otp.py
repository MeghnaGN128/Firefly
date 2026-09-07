from pages.otp import enter_otp, click_verify
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

    data = response.json()
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

    print("\n OTP verified successfully")