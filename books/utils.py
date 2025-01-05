from bson.objectid import ObjectId
from datetime import date, datetime


def validate_object_id(book_id):
    """
    Validates and converts a string to a MongoDB ObjectId.

    Args:
        book_id (str): The string representation of an ObjectId.

    Returns:
        ObjectId or None: The converted ObjectId or None if invalid.
    """
    try:
        return ObjectId(book_id)
    except Exception:
        return None


def convert_published_date(data):
    """
    Converts a 'published_date' field in a dictionary from a date object
    to a datetime object.

    Args:
        data (dict): A dictionary containing a 'published_date' key.

    Returns:
        dict: The modified dictionary with the converted 'published_date'.
    """
    if "published_date" in data and isinstance(data["published_date"], date):
        data["published_date"] = datetime.combine(
            data["published_date"], datetime.min.time()
        )
    return data


def error_message(message, status=400):
    """
    Creates a standard error message.

    Args:
        message (str): The error message to display.
        status (int): The HTTP status code. Default is 400.

    Returns:
        dict: The error message dictionary.
    """
    return {"message": message, "status": status}
