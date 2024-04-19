from datetime import datetime
from web3 import Web3

web3 = Web3()

def format_duration(td: datetime) -> str:
    """
    Converts a timedelta object to a string representing the duration in hours and minutes.

    Args:
        td (timedelta): The time difference to format.

    Returns:
        str: A string representation of the duration in the format "XhYm ago".
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours}h{minutes}m ago"

def get_formatted_wei_amount(amount: int, comma_numbers: int = 2) -> float:
    """
    Converts a Wei amount to Ether and formats it to a specified number of decimal places.

    Args:
        amount (int): The amount in Wei to convert.
        comma_numbers (int): The number of decimal places for the returned value.

    Returns:
        float: The amount in Ether, formatted to the specified number of decimal places.
    """
    return round(web3.fromWei(amount, 'ether'), comma_numbers)
