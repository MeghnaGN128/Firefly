from utils.otp_validate import validate_otp


def test_validate_otp_valid():
    assert validate_otp("123456") == []


def test_validate_otp_invalid_length():
    assert validate_otp("12345") == ["OTP must contain exactly 6 digits"]


def test_validate_otp_invalid_chars():
    assert validate_otp("12A456") == ["OTP must contain only numbers"]
