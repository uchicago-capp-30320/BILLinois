import re


def normalize_bill_number(number: str) -> str:
    """
    Normalize a bill number by inserting a space between the prefix and the suffix.

    Handles examples like:
        'hb1234'   -> 'HB 1234'
        'hjr45'    -> 'HJR 45'
        'sr1a'     -> 'SR 1A'
        'hb12s4'   -> 'HB 12S4'

    Falls back to inserting a space after the first 2 characters if no match.
    """
    number = number.upper()

    match = re.match(r"^([A-z]+)(\d+[A-z0-9]*)$", number)
    if match:
        return f"{match.group(1)} {match.group(2)}"

    # Fallback: insert space after first 2 characters
    return number[:2] + " " + number[2:]


def bill_number_for_url(number: str) -> str:
    """Remove spaces and lowercase bill number for URL use."""
    if not number:
        raise ValueError("Bill number must not be None or empty")
    return number.replace(" ", "").lower()
