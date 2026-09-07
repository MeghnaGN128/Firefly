import requests

from config import AUTH_URL, OTP_URL


def authenticate(phone, password):
    response = requests.post(
        AUTH_URL,
        json={
            "phone_number": phone,
            "password": password
        }
    )

    print("Backend status:", response.status_code)
    print("Backend response:", response.text)

    return response


def verify_otp(phone, otp):
    response = requests.post(
        OTP_URL,
        json={
            "phone_number": phone,
            "OTP": otp,
            "device_type": "web_token"
        }
    )

    print("OTP backend status:", response.status_code)
    print("OTP backend response:", response.text)

    return response


def forgot_password(phone):
    response = requests.post(
        "https://api-test.cloud-kitchen.in/itc_nbd/v1/forgot-password/",
        json={
            "phone_number": phone
        }
    )

    print("Forgot password status:", response.status_code)
    print("Forgot password response:", response.text)

    return response