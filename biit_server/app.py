from biit_server.utils import send_discord_message
from biit_server.http_responses import http405
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

from .meeting_handler import (
    meeting_get,
    meeting_post,
    meeting_put,
    meeting_delete,
    meeting_user_put,
    meeting_accept,
    meeting_decline,
)

from .feedback_handler import feedback_delete, feedback_get, feedback_post

# This runs on Firebase/Cloud Run!


def create_app():
    app = Flask(__name__)

    @app.route("/account", methods=["POST", "GET", "PUT", "DELETE"])
    def account_route():
        send_discord_message('please man i just want it to work')
        if request.method == "POST":
            return account_post(request)

        elif request.method == "GET":
            return account_get(request)

        elif request.method == "PUT":
            return account_put(request)

        elif request.method == "DELETE":
            return account_delete(request)
        else:
            return http405(request.method)

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

    @app.route("/meeting", methods=["POST", "GET", "PUT", "DELETE"])
    def meeting_route():
        if request.method == "POST":
            return meeting_post(request)

        elif request.method == "GET":
            return meeting_get(request)

        elif request.method == "PUT":
            return meeting_put(request)

        elif request.method == "DELETE":
            return meeting_delete(request)

    @app.route("/meeting/user", methods=["PUT"])
    def meeting_user_update_route():
        if request.method == "PUT":
            return meeting_user_put(request)

    @app.route("/feedback", methods=["POST", "GET", "DELETE"])
    def feedback_route():
        if request.method == "POST":
            return feedback_post(request)
        if request.method == "GET":
            return feedback_get(request)
        if request.method == "DELETE":
            return feedback_delete(request)
        return http405()

    @app.route("/meeting/<id>/accept", methods=["PUT"])
    def accept_route(id):
        if request.method == "PUT":
            return meeting_accept(request, id)

    @app.route("/meeting/<id>/decline", methods=["PUT"])
    def decline_route(id):
        if request.method == "PUT":
            return meeting_decline(request, id)

    return app
