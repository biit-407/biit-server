from flask import Flask, request
import json
from .account_handler import account_post, account_get, account_put, account_delete
from .ban_handler import ban_post, ban_put
from .community_handler import (
    community_delete,
    community_get,
    community_post,
    community_put,
)

# This runs on Firebase/Cloud Run!
def create_app():
    app = Flask(__name__)

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

    @app.route("/community", methods=["POST", "GET", "PUT", "DELETE"])
    def community_route():
        if request.method == "POST":
            return community_post(request)

        elif request.method == "GET":
            return community_get(request)

        elif request.method == "PUT":
            return community_put(request)

        elif request.method == "DELETE":
            return community_delete(request)

    @app.route("/ban", methods=["POST", "PUT"])
    def ban_route():
        if request.method == "POST":
            return ban_post(request)

        elif request.method == "PUT":
            return ban_put(request)

    return app
