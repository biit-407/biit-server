from flask import Flask, request
import json
from .account_handler import account_post, account_get, account_put, account_delete


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
            return account_post(request)

        elif request.method == "GET":
            return account_get(request)

        elif request.method == "PUT":
            return account_put(request)

        elif request.method == "DELETE":
            return account_delete(request)

    return app
