import secrets
import string


def generate_otp(length=6, alphanumeric=True):
    """
    Generate a One-Time Password (OTP).

    Args:
        `length (int)`: Length of the OTP. Default is 6.
        `alphanumeric (bool)`: If True, generate an alphanumeric OTP. Default is False.

    Returns:
        `str`: The generated OTP.
    """
    if alphanumeric:
        characters = string.ascii_letters + string.digits
    else:
        characters = string.digits

    otp = "".join(secrets.choice(characters) for _ in range(length))
    return otp
