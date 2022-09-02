"""Functions for providing clean output."""


def strip_decimal(value: float, places: int = 1) -> str:
    """Remove a decimal if it is zero and returns the value rounded.

    Args:
        value (float): The value to be rounded.
        places (float): Number of places to round. Default is 1.

    Returns:
        (str): Rounded value with decimal stripped if equal to zero.
    """
    rounded_value = round(value, places)
    if (int(rounded_value) - rounded_value) == 0:
        return f"{int(rounded_value)}"
    return f"{rounded_value}"
