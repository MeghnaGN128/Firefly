import base64
import getpass
import json
from pathlib import Path

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import BASE_URL
from pages.login import enter_phone, enter_password, click_get_otp
from pages.otp import enter_otp, click_verify
from pages.home_select import HomeSelectPage
from utils.api_clients import authenticate, verify_otp
from utils.otp_validate import validate_otp
from utils.validate import validate_phone


def _browser_credentials_cache():
    return Path("/tmp/firefly-browser-credentials.json")


@pytest.fixture(scope="session")
def browser_credentials():
    cache_file = _browser_credentials_cache()

    try:
        credentials = json.loads(
            cache_file.read_text(encoding="utf-8")
        )
        username = credentials["username"]
        password = credentials["password"]

    except (
        FileNotFoundError,
        KeyError,
        TypeError,
        ValueError,
        OSError
    ):
        username = input("Enter browser username: ")
        password = getpass.getpass("Enter browser password: ")

        cache_file.write_text(
            json.dumps(
                {
                    "username": username,
                    "password": password
                }
            ),
            encoding="utf-8"
        )

        cache_file.chmod(0o600)

    return username, password


@pytest.fixture(scope="session")
def driver(browser_credentials):
    username, password = browser_credentials

    chrome_options = Options()

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.set_capability(
        "goog:loggingPrefs",
        {
            "performance": "ALL"
        }
    )

    driver = webdriver.Chrome(
        options=chrome_options
    )

    driver.execute_cdp_cmd(
        "Network.enable",
        {}
    )

    driver.execute_cdp_cmd(
        "Network.setCacheDisabled",
        {
            "cacheDisabled": True
        }
    )

    credentials = f"{username}:{password}"

    encoded_credentials = base64.b64encode(
        credentials.encode()
    ).decode()

    driver.execute_cdp_cmd(
        "Network.setExtraHTTPHeaders",
        {
            "headers": {
                "Authorization": f"Basic {encoded_credentials}"
            }
        }
    )

    driver.get(BASE_URL)

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def authenticated_driver(driver):
    phone = input("Enter phone number: ")
    password = getpass.getpass(
        "Enter application password: "
    )

    if not validate_phone(phone):
        raise AssertionError(
            "Phone number must contain exactly 10 digits"
        )

    response = authenticate(
        phone,
        password
    )

    if not response.ok:
        raise AssertionError(
            f"Login API failed\n"
            f"Status: {response.status_code}\n"
            f"Response: {response.text}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise AssertionError(
            "Login API returned non-JSON response\n"
            f"Status: {response.status_code}\n"
            f"Response: {response.text}"
        ) from exc

    message = data.get(
        "message",
        ""
    )

    if message != "OTP sent successfully":
        raise AssertionError(
            f"Login failed: {message}"
        )

    enter_phone(
        driver,
        phone
    )

    enter_password(
        driver,
        password
    )

    click_get_otp(
        driver
    )

    otp = input("Enter OTP: ")

    errors = validate_otp(otp)

    if errors:
        raise AssertionError(
            "\n".join(errors)
        )

    otp_response = verify_otp(
        phone,
        otp
    )

    if not otp_response.ok:
        raise AssertionError(
            f"OTP verification request failed\n"
            f"Status: {otp_response.status_code}\n"
            f"Response: {otp_response.text}"
        )

    try:
        otp_data = otp_response.json()
    except ValueError as exc:
        raise AssertionError(
            "OTP verification returned non-JSON response\n"
            f"Status: {otp_response.status_code}\n"
            f"Response: {otp_response.text}"
        ) from exc

    message = otp_data.get(
        "message",
        ""
    ).lower()

    if message != "login successful":
        raise AssertionError(
            f"Backend OTP validation failed\n"
            f"Message: {message}"
        )

    enter_otp(
        driver,
        otp
    )

    click_verify(
        driver
    )

    home_page = HomeSelectPage(
        driver
    )

    home_page.wait_until_loaded()

    return driver


@pytest.fixture
def login_to_otp(driver):
    phone = input("Enter phone number: ")
    password = getpass.getpass(
        "Enter application password: "
    )

    if not validate_phone(phone):
        raise AssertionError(
            "Phone number must contain exactly 10 digits"
        )

    response = authenticate(
        phone,
        password
    )

    if not response.ok:
        raise AssertionError(
            f"Login API failed\n"
            f"Status: {response.status_code}\n"
            f"Response: {response.text}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise AssertionError(
            "Login API returned non-JSON response\n"
            f"Status: {response.status_code}\n"
            f"Response: {response.text}"
        ) from exc

    message = data.get(
        "message",
        ""
    )

    if message != "OTP sent successfully":
        raise AssertionError(
            f"Login failed: {message}"
        )

    enter_phone(
        driver,
        phone
    )

    enter_password(
        driver,
        password
    )

    click_get_otp(
        driver
    )

    return driver, phone