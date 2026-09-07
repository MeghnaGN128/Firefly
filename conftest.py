import base64
import getpass
import pytest

from selenium import webdriver

from config import BASE_URL


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