import base64
import getpass
import pytest

from selenium import webdriver

from config import BASE_URL
from pages.login import enter_phone, enter_password, click_get_otp
from utils.api_clients import authenticate
from utils.validate import validate_phone


@pytest.fixture(scope="session")
def browser_credentials():
    username = input("Enter browser username: ")
    password = getpass.getpass("Enter browser password: ")

    return username, password


@pytest.fixture(scope="session")
def driver(browser_credentials):
    username, password = browser_credentials

    driver = webdriver.Chrome()

    credentials = f"{username}:{password}"

    encoded_credentials = base64.b64encode(
        credentials.encode()
    ).decode()

    driver.execute_cdp_cmd("Network.enable", {})

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


@pytest.fixture
def login_to_otp(driver):
    phone = input("Enter phone number: ")
    password = getpass.getpass("Enter application password: ")

    if not validate_phone(phone):
        raise AssertionError("Phone number must contain exactly 10 digits")

    response = authenticate(phone, password)
    message = response.json().get("message", "")

    if message != "OTP sent successfully":
        raise AssertionError(f"Login failed: {message}")

    enter_phone(driver, phone)
    enter_password(driver, password)
    click_get_otp(driver)

    return driver, phone