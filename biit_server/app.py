from flask import Flask
import json


# This runs on Firebase/Cloud Run!

app = Flask(__name__)


@app.route("/test")
def test_route():
    return "Ok!"


@app.route("/account", methods=["POST", "GET", "PUT", "DELETE"])
def account_route():
    if request.method == "POST":
        data = json.loads(request.get_json())
        if "token" not in data or not data["token"]:
            return "Token not found", 400
        
        if account.create(data):
            return "Account Created", 200
        return "Failed to create account", 400

    elif request.method == "GET":
        return "OK!"
    elif request.method == "PUT":
        return "OK!"
    elif request.method == "DELETE":
        return "OK!"
