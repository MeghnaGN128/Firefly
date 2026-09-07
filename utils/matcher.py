def normalize_item_name(name):
    return " ".join(name.lower().strip().split())


def build_item_totals(data):
    totals = {}

    for row in data:
        item = normalize_item_name(row["item"])
        quantity = float(row["quantity"])

        totals[item] = totals.get(item, 0) + quantity

    return totals


def compare_ck_and_ods(ck_data, ods_data):

    ck = build_item_totals(ck_data)
    ods = build_item_totals(ods_data)

    all_items = sorted(set(ck) | set(ods))

    results = []

    for item in all_items:

        ck_quantity = ck.get(item, 0)
        ods_quantity = ods.get(item, 0)

        if item not in ck:
            status = "EXTRA IN ODS"
        elif item not in ods:
            status = "MISSING IN ODS"
        elif ck_quantity == ods_quantity:
            status = "MATCH"
        else:
            status = "QUANTITY MISMATCH"

        results.append({
            "item": item,
            "ck_quantity": ck_quantity,
            "ods_quantity": ods_quantity,
            "status": status
        })

    return results