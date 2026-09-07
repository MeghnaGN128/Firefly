import json
import os

from pages.ck_requisition import CKRequisitionPage
from pages.ods_dispatch import ODSDispatchPage
from utils.matcher import compare_ck_and_ods


CK_DATA_FILE = "ck_requisition_data.json"


def save_ck_data(data):
    with open(CK_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_ck_data():
    if not os.path.exists(CK_DATA_FILE):
        raise FileNotFoundError(
            "CK requisition data not found. Capture CK data first."
        )

    with open(CK_DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def test_ck_to_ods_matching(driver):

    ck_page = CKRequisitionPage(driver)

    ck_page.open()

    print("\n")
    print("==========================================")
    print("CK REQUISITION")
    print("==========================================")
    print("Please select outlet and add your items.")
    print("Enter quantities for all required items.")
    print("Do NOT submit yet.")
    print("After entering all items, press ENTER here.")
    print("==========================================")

    input()

    ck_data = ck_page.get_requisition_items()

    if not ck_data:
        raise AssertionError(
            "No CK requisition items found."
        )

    print("\nCK DATA")

    for row in ck_data:
        print(
            f"{row['item']} -> {row['quantity']}"
        )

    save_ck_data(ck_data)

    print("\nCK data saved.")

    print("\n==========================================")
    print("Now submit the CK requisition manually.")
    print("Complete the required CK process.")
    print("Then change permissions from CK to ODS.")
    print("Open ODS Dispatch.")
    print("Select the required date.")
    print("Wait until the indent appears.")
    print("==========================================")

    input("\nPress ENTER when ODS data is visible...")

    ods_page = ODSDispatchPage(driver)

    ods_page.open()

    input(
        "\nIf required, select the ODS date manually. "
        "Press ENTER after the ODS data is visible..."
    )

    ods_data = ods_page.get_dispatch_items()

    if not ods_data:
        raise AssertionError(
            "No ODS dispatch items found."
        )

    print("\nODS DATA")

    for row in ods_data:
        print(
            f"{row['item']} -> {row['quantity']}"
        )

    results = compare_ck_and_ods(
        ck_data,
        ods_data
    )

    print("\n")
    print("==========================================")
    print("CK vs ODS RESULT")
    print("==========================================")

    failed = False

    for result in results:

        print(
            f"{result['item']} | "
            f"CK: {result['ck_quantity']} | "
            f"ODS: {result['ods_quantity']} | "
            f"{result['status']}"
        )

        if result["status"] != "MATCH":
            failed = True

    print("==========================================")

    if failed:
        raise AssertionError(
            "CK Requisition and ODS Dispatch data do not match."
        )

    print("OVERALL RESULT: PASS")