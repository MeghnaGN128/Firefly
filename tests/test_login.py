from pages.login import enter_phone, enter_password, click_get_otp
from utils.validate import validate_phone, check_password_rules
from utils.api_clients import authenticate


def test_login(driver):

    phone = input("Enter phone number: ")
    application_password = input("Enter application password: ")

    if not validate_phone(phone):
        raise AssertionError(
            "❌ Phone number must contain exactly 10 digits"
        )

    response = authenticate(phone, application_password)

    data = response.json()
    message = data.get("message", "")

    if message != "OTP sent successfully":
        raise AssertionError(
            f"❌ Login failed\n"
            f"Phone: {phone}\n"
            f"Reason: {message}"
        )

    print("\nBackend authentication:")
    print("Phone + Password    ✅ LOGIN SUCCESS")

    results = check_password_rules(application_password)

    print("\nPassword rules:")

    for rule, passed in results.items():
        if passed:
            print(f"{rule:<20}")
        else:
            print(f"{rule:<20}")

    failed_rules = [
        rule for rule, passed in results.items()
        if not passed
    ]

    if failed_rules:
        print("\n⚠ Login successful, but password is not strong")
        print("⚠ Password does not follow all required rules")

    else:
        print("\n Password follows all required rules")

    enter_phone(driver, phone)
    enter_password(driver, application_password)
    click_get_otp(driver)