from flask import jsonify
from typing import Dict, Any


def http405():
    return "Method not allowed", 405


def http400(description: str):
    return f"Bad Request: {description}", 400


def http500(description: str):
    return f"Internal Server Error: {description}", 500


def http200(description: str = ""):
    if description == "":
        return "OK", 200
    return f"OK: {description}", 200


def jsonHttp200(message: str, data: Dict[str, Any]):
    """Http 200 response with json as data

    Args:
        message (str): Message to be sent
        data: Data to be sent

    Returns:
        str: Json combination of data and message
    """
    response = data
    response["message"] = message
    response["status_code"] = 200
    return jsonify(response)
