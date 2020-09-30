from flask import jsonify


def http405():
    return "Method not allowed", 405


def http400(description: str):
    return f"Bad Request: {description}", 400


def http200(description: str = ""):
    if description == "":
        return "OK", 200
    return f"OK: {description}", 200


def jsonHttp200(message: str, data):
    json = list(data)
    json.append(message)
    return jsonify(json)
