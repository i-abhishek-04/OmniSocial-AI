"""
Shared response envelope helpers.

Every API response follows: {success, message, data} on success or
{success, message, errors} on failure, so the frontend axios layer can
handle every endpoint uniformly.
"""
from typing import Any


def success_response(data: Any = None, message: str = "OK") -> dict:
    return {"success": True, "message": message, "data": data}


def error_response(message: str, errors: Any = None) -> dict:
    return {"success": False, "message": message, "errors": errors}
