import json

from pages.ck_requisition import CKRequisitionPage


def test_capture_ck_requisition(driver):

    page = CKRequisitionPage(driver)

    page.open()

    print("\n==========================================")
    print("CK REQUISITION")
    print("==========================================")
    print("Select the outlet.")
    print("Add all required items.")
    print("Enter quantities.")
    print("Do NOT submit yet.")
    print("Press ENTER after entering all items.")
    print("==========================================")

    input()

    data = page.get_requisition_items()

    if not data:
        raise AssertionError(
            "No CK requisition items found."
        )

    with open(
        "ck_requisition_data.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )

    print("\nCK REQUISITION DATA")

    for row in data:
        print(
            f"{row['item']} -> {row['quantity']}"
        )

    print("\nCK data captured successfully.")