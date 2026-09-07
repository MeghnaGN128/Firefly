import re


def validate_phone(phone):
    return bool(re.fullmatch(r"\d{10}", phone))


def check_password_rules(password):
    return {
        "8+ characters": len(password) >= 8,
        "Uppercase": bool(re.search(r"[A-Z]", password)),
        "Lowercase": bool(re.search(r"[a-z]", password)),
        "Number": bool(re.search(r"\d", password)),
        "Special character": bool(re.search(r"[^A-Za-z0-9]", password))
    }