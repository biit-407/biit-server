from flask import Flask
import json


# This runs on Firebase/Cloud Run!

app = Flask(__name__)

def missing_data(missedParam, response):
    return "Missing Parameter "+ missedParam, response


@app.route("/test")
def test_route():
    return "Ok!"


@app.route("/account", methods=["POST", "GET", "PUT", "DELETE"])
def account_route():
    if request.method == "POST":
        data = ""
        try:
            data = json.loads(request.get_json())
        except:
            return "Failed to load account JSON", 400
        if "token" not in data or not data["token"]:
            return missing_data("token",400)
        if "fname" not in data or not data["fname"]:
            return missing_data("fname",400)
        if "lname" not in data or not data["lname"]:
            return missing_data("lname",400)
        if "email" not in data or not data["email"]:
            return missing_data("email",400)
        #TODO @Ryan Create the DB stuff
        if account.create(data):
            return "Account Created", 200
        return "Failed to create account", 400

    elif request.method == "GET":
        return "OK!"
    elif request.method == "PUT":
        return "OK!"
    elif request.method == "DELETE":
        return "OK!"
