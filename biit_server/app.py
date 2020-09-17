from flask import Flask, request
import json


# This runs on Firebase/Cloud Run!
def create_app():
    app = Flask(__name__)

    def missing_data(missedParam, response):
        return "Missing Parameter " + missedParam, response

    @app.route("/test")
    def test_route():
        return "Ok!"

    @app.route("/account", methods=["POST", "GET", "PUT", "DELETE"])
    def account_route():
        if request.method == "POST":
            keys = ["token", "fname", "lname", "email"]
            data = ""
            try:
                data = json.loads(request.get_json())
            except:
                return "Failed to load account JSON", 400
            for key in keys:
                if key not in data or not data[key]:
                    return missing_data(key, 400)
            # TODO @Ryan Create the DB stuff
            if account.create(data):
                return "Account Created", 200
            return "Failed to create account", 400
        elif request.method == "GET":
            data = ""
            try:
                data = json.loads(request.get_json())
            except:
                return "Failed to load JSON object", 400
            if "email" not in data or not data["email"]:
                return missing_data("email", 400)
            return account.get(data)
        elif request.method == "PUT":
            keys = ["token", "email"]
            data = ""
            try:
                data = json.loads(request.get_json())
            except:
                return "Failed to load account JSON", 400
            for key in keys:
                if key not in data or not data[key]:
                    return missing_data(key, 400)
            account.update(data)
            return "Account Updated", 200
        elif request.method == "DELETE":
            keys = ["token", "email"]
            data = ""
            try:
                data = json.loads(request.get_json())
            except:
                return "Failed to load account JSON", 400
            for key in keys:
                if key not in data or not data[key]:
                    return missing_data(key, 400)
            return "Account Deleted", 200
    return app
