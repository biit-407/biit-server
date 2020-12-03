from biit_server.notification_handler import notification_get, notification_post
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
    community_get_all,
    community_post,
    community_put,
    community_join_post,
    community_leave_post,
)

from .rating_handler import rating_get, rating_get_pending, rating_post

from .meeting_handler import (
    generate_reconnect_meeting,
    matchup,
    meeting_get,
    meeting_post,
    meeting_put,
    meeting_delete,
    meeting_set_venue,
    meeting_user_put,
    meeting_accept,
    meeting_decline,
    meetings_get_all,
    meetings_get_past_users,
    meetings_get_pending,
    meetings_get_upcoming,
    meetings_get_past,
    reschedule,
    reschedule,
)

from .feedback_handler import feedback_delete, feedback_get, feedback_post
from .community_stats_handler import community_stats_get

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

    @app.route("/community/<id>/stats", methods=["GET"])
    def stat_route(id):
        if request.method == "GET":
            return community_stats_get(request, id)

    @app.route("/community/all", methods=["GET"])
    def community_all():
        if request.method == "GET":
            return community_get_all(request)

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

    @app.route("/rating/pending", methods=["GET"])
    def rating_pending_route():
        if request.method == "GET":
            return rating_get_pending(request)

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

    @app.route("/meeting/<user>", methods=["GET"])
    def meeting_user_fetch_route(user):
        if request.method == "GET":
            return meetings_get_all(request)

    @app.route("/meeting/pending", methods=["GET"])
    def meeting_user_pending_fetch_route():
        if request.method == "GET":
            return meetings_get_pending(request)

    @app.route("/meeting/upcoming", methods=["GET"])
    def meeting_user_upcoming_fetch_route():
        if request.method == "GET":
            return meetings_get_upcoming(request)

    @app.route("/meeting/past", methods=["GET"])
    def meeting_user_past_fetch_route():
        if request.method == "GET":
            return meetings_get_past(request)

    @app.route("/meeting/past/users", methods=["GET"])
    def meeting_get_past_users_route():
        if request.method == "GET":
            return meetings_get_past_users(request)

    @app.route("/meeting/reschedule", methods=["POST"])
    def meeting_reschedule_route():
        if request.method == "POST":
            return reschedule(request)

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

    @app.route("/meeting/<id>/venue", methods=["PUT"])
    def venue_route(id):
        if request.method == "PUT":
            return meeting_set_venue(request, id)

    @app.route("/meeting/<id>/decline", methods=["PUT"])
    def decline_route(id):
        if request.method == "PUT":
            return meeting_decline(request, id)

    @app.route("/matchup", methods=["GET"])
    def meeting_matching():
        if request.method == "GET":
            return matchup(request)

    @app.route("/notifications", methods=["GET", "POST"])
    def notifications_route():
        if request.method == "GET":
            return notification_get(request)
        if request.method == "POST":
            return notification_post(request)

    @app.route("/meeting/reconnect", methods=["POST"])
    def meeting_reconnect():
        if request.method == "POST":
            return generate_reconnect_meeting(request)

    return app
