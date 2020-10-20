from flask import Flask, request
import json
from .account_handler import (
    account_post,
    account_get,
    account_put,
    account_delete,
    profile_get,
    profile_post,
)
from .ban_handler import ban_post, ban_put
from .community_handler import (
    community_delete,
    community_get,
    community_post,
    community_put,
    community_join_post,
    community_leave_post,
)

from .rating_handler import rating_get, rating_post

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

    @app.route("/community/<id>/join", methods=["POST"])
    def join_route(id):
        if request.method == "POST":
            return community_join_post(request, id)

    @app.route("/community/<id>/leave", methods=["POST"])
    def leave_route(id):
        if request.method == "POST":
            return community_leave_post(request, id)

    @app.route("/ban", methods=["POST", "PUT"])
    def ban_route():
        if request.method == "POST":
            return ban_post(request)

        elif request.method == "PUT":
            return ban_put(request)

    @app.route("/profile", methods=["POST", "GET"])
    def profile_route():
        if request.method == "POST":
            return profile_post(request)

        elif request.method == "GET":
            return profile_get(request)

    @app.route("/rating", methods=["POST", "GET"])
    def rating_route():
        if request.method == "POST":
            return rating_post(request)

        elif request.method == "GET":
            return rating_get(request)

    return app
