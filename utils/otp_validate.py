def validate_otp(otp):

    errors = []

    if not otp.isdigit():
        errors.append("OTP must contain only numbers")

    if len(otp) != 6:
        errors.append("OTP must contain exactly 6 digits")

    return errors