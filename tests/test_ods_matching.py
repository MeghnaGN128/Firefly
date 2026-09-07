import json

from pages.ods_dispatch import ODSDispatchPage
from utils.matcher import compare_ck_and_ods


def test_ods_matches_ck(driver):

    with open(
        "ck_requisition_data.json",
        "r",
        encoding="utf-8"
    ) as file:
        ck_data = json.load(file)

    page = ODSDispatchPage(driver)

    page.open()

    print("\n==========================================")
    print("ODS DISPATCH")
    print("==========================================")
    print("Select the required date.")
    print("Wait until the CK requisition appears.")
    print("==========================================")

    input(
        "\nPress ENTER when ODS data is visible..."
    )

    ods_data = page.get_dispatch_items()

    if not ods_data:
        raise AssertionError(
            "No ODS dispatch data found."
        )

    results = compare_ck_and_ods(
        ck_data,
        ods_data
    )

    print("\n==========================================")
    print("CK VS ODS")
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
            "CK and ODS data mismatch found."
        )

    print("OVERALL RESULT: PASS")