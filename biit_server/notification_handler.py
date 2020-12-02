from datetime import datetime, timezone
from biit_server.http_responses import jsonHttp200
from biit_server.query_helper import ValidateType, validate_fields
from biit_server.authentication import AuthenticatedType, authenticated
from biit_server.db_accessor import get_past_meetups, get_past_unrated_meetups
from biit_server.database import Database
from biit_server.notification import AssetType, Notification
import uuid


def generate_unrated_past_meeting_notifications(
    email, notifications_db, unrated_user_meetups, user_all_notifications
):
    # rate previous meetup
    user_unrated_meetup_notifications = {}
    for key, meeting in unrated_user_meetups.items():
        notification = user_all_notifications.get(key, None)
        if key not in user_all_notifications:
            # create new notification
            id = str(uuid.uuid4())
            notification = Notification(
                id,
                email,
                datetime.now(),
                key,
                AssetType.UNRATED_MEETUP,
                f"Rate your meetup with {','.join([user for user, value in meeting.user_list.items() if user != email and value == 1])}",
                False,
            ).to_dict()
            notifications_db.add(notification, id=id)
        user_unrated_meetup_notifications[key] = notification

    return user_unrated_meetup_notifications


def generate_reconnect_notifications(
    email, notifications_db, past_user_meetups, user_all_notifications
):
    reconnect_notifications = {}
    for key, meeting in past_user_meetups.items():
        notification = user_all_notifications.get(key, None)
        # 2,592,000 is 1 day in seconds
        if (
            key not in user_all_notifications
            and meeting.timestamp
            < datetime.now().replace(tzinfo=timezone.utc).timestamp() - 2592000
        ):
            # create new notification
            id = str(uuid.uuid4())
            notification = Notification(
                id,
                email,
                datetime.now().replace(tzinfo=timezone.utc).timestamp(),
                key,
                AssetType.RECONNECT,
                f"Reconnect with {','.join([user for user, value in meeting.user_list.items() if user != email and value == 1])}",
                False,
            ).to_dict()
            notifications_db.add(notification, id=id)
        reconnect_notifications[key] = notification

    return reconnect_notifications


@validate_fields(["email", "token"], ValidateType.QUERY)
@authenticated(AuthenticatedType.QUERY)
def notification_get(request, auth):
    """"""
    args = request.args

    notifications_db = Database("notifications")

    # query db for all notifications
    notifications_db_response = notifications_db.collection_ref.get()
    notifications = [
        Notification(document_snapshot=notification)
        for notification in notifications_db_response
    ]
    all_notifications = {
        notification.to_dict()["asset_id"]: notification.to_dict()
        for notification in notifications
    }

    # get all notifications for this user
    user_all_notifications = {}
    for key, value in all_notifications.items():
        if value["user_id"] == args["email"]:
            user_all_notifications[key] = value

    # generate notifications
    unrated_user_meetups = {
        item.id: item for item in get_past_unrated_meetups(args["email"])
    }

    user_unrated_meetup_notifications = generate_unrated_past_meeting_notifications(
        args["email"], notifications_db, unrated_user_meetups, user_all_notifications
    )

    past_user_meetups = {item.id: item for item in get_past_meetups(args["email"])}

    reconnect_notifications = generate_reconnect_notifications(
        args["email"], notifications_db, past_user_meetups, user_all_notifications
    )

    # add new notifications to working memory
    for key, value in user_unrated_meetup_notifications.items():
        if key not in user_all_notifications:
            user_all_notifications[key] = value

    for key, value in reconnect_notifications.items():
        if key not in user_all_notifications:
            user_all_notifications[key] = value

    # remove old rate previous meetup notifications
    current_user_all_notifications = {}
    for key, value in user_all_notifications.items():
        if (
            key not in unrated_user_meetups
            and value["asset_type"] == AssetType.UNRATED_MEETUP.value
        ):
            notifications_db.delete(value["id"])
        else:
            current_user_all_notifications[key] = value

    # filter only active notifications
    user_all_active_notifications = {}
    for key, value in current_user_all_notifications.items():
        if value["dismissed"] == False:
            user_all_active_notifications[key] = value

    # add the asset itself to the notification
    for key, value in user_all_active_notifications.items():
        if value["asset_type"] == AssetType.UNRATED_MEETUP.value:
            user_all_active_notifications[key]["asset"] = unrated_user_meetups[
                key
            ].to_dict()
        if value["asset_type"] == AssetType.RECONNECT.value:
            user_all_active_notifications[key]["asset"] = past_user_meetups[
                key
            ].to_dict()

    response = {
        "refresh_token": auth[1],
        "access_token": auth[0],
        "data": user_all_active_notifications,
    }

    return jsonHttp200("Successfully got notifications", response)


@validate_fields(["email", "token", "notification_id"], ValidateType.BODY)
@authenticated(AuthenticatedType.BODY)
def notification_post(request, auth):
    """"""
    body = request.get_json()

    notifications_db = Database("notifications")

    notifications_db.update(body["notification_id"], {"dismissed": True})

    response = {
        "refresh_token": auth[1],
        "access_token": auth[0],
        "data": True,
    }

    return jsonHttp200("Successfully dismissed notification", response)
