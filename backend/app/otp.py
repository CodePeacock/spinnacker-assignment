"""This module contains a function to generate a one-time password (OTP)."""

import secrets
import string


def generate_otp(length=6, alphanumeric=True):
    """
    Generate a one-time password (OTP) of specified length.
    Parameters:
    - length (int): The length of the OTP. Default is 6.
    - alphanumeric (bool): Whether the OTP should contain alphanumeric characters. Default is True.
    Returns:
    - otp (str): The generated OTP.

    Example usage:
    >>> generate_otp()
    '3aBcD4'
    >>> generate_otp(length=8, alphanumeric=False)
    '12345678'
    """
    if alphanumeric:
        characters = string.ascii_letters + string.digits
    else:
        characters = string.digits

    otp = "".join(secrets.choice(characters) for _ in range(length))
    return otp
