from biit_server.rating import Rating
from biit_server.notification import AssetType, Notification
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from biit_server.meeting import Meeting
import json
import pytest
from biit_server.app import create_app


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


def test_notification_get_past_unrated_meetup(client):
    """
    Tests that getting all notifications for past unrated meetups works correctly
    """
    with patch("biit_server.db_accessor.Database") as mock_meeting_database, patch(
        "biit_server.db_accessor.Meeting"
    ) as mock_meeting, patch(
        "biit_server.notification_handler.Notification"
    ) as mock_notification, patch(
        "biit_server.notification_handler.Database"
    ) as mock_notification_database, patch(
        "biit_server.db_accessor.Rating"
    ) as mock_rating:
        meeting_db_instance = mock_meeting_database.return_value
        meeting_db_instance.collection_ref.get.return_value = [1]

        notification_db_instance = mock_notification_database.return_value
        notification_db_instance.collection_ref.get.return_value = []

        query_data = {"email": "beidou@purdue.edu", "token": "dabonem"}

        test_json = {
            "id": "random_meeting",
            "user_list": {"beidou@purdue.edu": 1, "another@purdue.edu": 1},
            "duration": 110,
            "location": "Li Yue",
            "meettype": "Gacha",
            "timestamp": datetime.now().replace(tzinfo=timezone.utc).timestamp() - 100,
        }

        mock_meeting.return_value = Meeting(
            id=test_json["id"],
            user_list=test_json["user_list"],
            duration=test_json["duration"],
            location=test_json["location"],
            meeting_type=test_json["meettype"],
            timestamp=test_json["timestamp"],
        )

        mock_notification.return_value = Notification(
            id="randomid",
            user_id="beidou@purdue.edu",
            timestamp=datetime.now(),
            asset_id=test_json["id"],
            asset_type=AssetType.UNRATED_MEETUP,
            message="Rate your meetup with another@purdue.edu",
            dismissed=False,
        )

        mock_rating.return_value = Rating(
            meeting_id="random_meeting",
            rating_dict={"beidou@purdue.edu": -1, "another@purdue.edu": -1},
            community="cooomunity",
        )

        rv = client.get(
            "/notifications",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        notification_db_instance.delete.assert_not_called()
        notification_db_instance.add.assert_called_once()
        assert return_data["access_token"] == "AccessToken"
        assert len(return_data["data"]) == 1
        assert return_data["data"]["random_meeting"]["asset"]["id"] == test_json["id"]
        assert return_data["message"] == "Successfully got notifications"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200


def test_notification_get_reconnect(client):
    """
    Tests that getting all notifications for past unrated meetups works correctly
    """
    with patch("biit_server.db_accessor.Database") as mock_meeting_database, patch(
        "biit_server.db_accessor.Meeting"
    ) as mock_meeting, patch(
        "biit_server.notification_handler.Notification"
    ) as mock_notification, patch(
        "biit_server.notification_handler.Database"
    ) as mock_notification_database, patch(
        "biit_server.db_accessor.Rating"
    ) as mock_rating:
        meeting_db_instance = mock_meeting_database.return_value
        meeting_db_instance.collection_ref.get.return_value = [1]

        notification_db_instance = mock_notification_database.return_value
        notification_db_instance.collection_ref.get.return_value = []

        query_data = {"email": "beidou@purdue.edu", "token": "dabonem"}

        test_json = {
            "id": "random_meeting",
            "user_list": {"beidou@purdue.edu": 1, "another@purdue.edu": 1},
            "duration": 110,
            "location": "Li Yue",
            "meettype": "Gacha",
            "timestamp": datetime.now().replace(tzinfo=timezone.utc).timestamp()
            - 3592000,
        }

        mock_meeting.return_value = Meeting(
            id=test_json["id"],
            user_list=test_json["user_list"],
            duration=test_json["duration"],
            location=test_json["location"],
            meeting_type=test_json["meettype"],
            timestamp=test_json["timestamp"],
        )

        mock_notification.return_value = Notification(
            id="randomid",
            user_id="beidou@purdue.edu",
            timestamp=datetime.now(),
            asset_id=test_json["id"],
            asset_type=AssetType.RECONNECT,
            message="Reconnect with another@purdue.edu",
            dismissed=False,
        )

        mock_rating.return_value = Rating(
            meeting_id="random_meeting",
            rating_dict={"beidou@purdue.edu": 1, "another@purdue.edu": -1},
            community="cooomunity",
        )

        rv = client.get(
            "/notifications",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        notification_db_instance.delete.assert_not_called()
        notification_db_instance.add.assert_called_once()
        assert return_data["access_token"] == "AccessToken"
        assert len(return_data["data"]) == 1
        assert return_data["data"]["random_meeting"]["asset"]["id"] == test_json["id"]
        assert return_data["message"] == "Successfully got notifications"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200


def test_notification_get_unrated_meetup_none(client):
    """
    Tests that getting all notifications for past unrated meetups works correctly
    """
    with patch("biit_server.db_accessor.Database") as mock_meeting_database, patch(
        "biit_server.db_accessor.Meeting"
    ) as mock_meeting, patch(
        "biit_server.notification_handler.Notification"
    ) as mock_notification, patch(
        "biit_server.notification_handler.Database"
    ) as mock_notification_database, patch(
        "biit_server.db_accessor.Rating"
    ) as mock_rating:

        meeting_db_instance = mock_meeting_database.return_value
        meeting_db_instance.collection_ref.get.return_value = [1]

        notification_db_instance = mock_notification_database.return_value
        notification_db_instance.collection_ref.get.return_value = []

        query_data = {"email": "beidou@purdue.edu", "token": "dabonem"}

        test_json = {
            "id": "random_meeting",
            "user_list": {"beidou@purdue.edu": 1, "another@purdue.edu": 1},
            "duration": 110,
            "location": "Li Yue",
            "meettype": "Gacha",
            "timestamp": datetime.now().replace(tzinfo=timezone.utc).timestamp() + 100,
        }

        mock_meeting.return_value = Meeting(
            id=test_json["id"],
            user_list=test_json["user_list"],
            duration=test_json["duration"],
            location=test_json["location"],
            meeting_type=test_json["meettype"],
            timestamp=test_json["timestamp"],
        )

        mock_notification.return_value = Notification(
            id="randomid",
            user_id="beidou@purdue.edu",
            timestamp=datetime.now(),
            asset_id=test_json["id"],
            asset_type=AssetType.UNRATED_MEETUP,
            message="Rate your meetup with another@purdue.edu",
            dismissed=False,
        )

        mock_rating.return_value = Rating(
            meeting_id="random_meeting",
            rating_dict={"beidou@purdue.edu": 1, "another@purdue.edu": -1},
            community="cooomunity",
        )

        rv = client.get(
            "/notifications",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        notification_db_instance.delete.assert_not_called()
        notification_db_instance.add.assert_not_called()
        assert return_data["access_token"] == "AccessToken"
        assert len(return_data["data"]) == 0
        assert return_data["message"] == "Successfully got notifications"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200


def test_notification_get_unrated_meetup_delete_outdated(client):
    """
    Tests that getting all notifications for past unrated meetups works correctly
    """
    with patch("biit_server.db_accessor.Database") as mock_meeting_database, patch(
        "biit_server.db_accessor.Meeting"
    ) as mock_meeting, patch(
        "biit_server.notification_handler.Notification"
    ) as mock_notification, patch(
        "biit_server.notification_handler.Database"
    ) as mock_notification_database, patch(
        "biit_server.db_accessor.Rating"
    ) as mock_rating:
        meeting_db_instance = mock_meeting_database.return_value
        meeting_db_instance.collection_ref.get.return_value = []

        notification_db_instance = mock_notification_database.return_value
        notification_db_instance.collection_ref.get.return_value = [1]

        query_data = {"email": "beidou@purdue.edu", "token": "dabonem"}

        test_json = {
            "id": "random_meeting",
            "user_list": {"beidou@purdue.edu": 1, "another@purdue.edu": 1},
            "duration": 110,
            "location": "Li Yue",
            "meettype": "Gacha",
            "timestamp": datetime.now().replace(tzinfo=timezone.utc).timestamp() + 100,
        }

        mock_meeting.return_value = Meeting(
            id=test_json["id"],
            user_list=test_json["user_list"],
            duration=test_json["duration"],
            location=test_json["location"],
            meeting_type=test_json["meettype"],
            timestamp=test_json["timestamp"],
        )

        mock_notification.return_value = Notification(
            id="randomid",
            user_id="beidou@purdue.edu",
            timestamp=datetime.now(),
            asset_id=test_json["id"],
            asset_type=AssetType.UNRATED_MEETUP,
            message="Rate your meetup with another@purdue.edu",
            dismissed=False,
        )

        mock_rating.return_value = Rating(
            meeting_id="random_meeting",
            rating_dict={"beidou@purdue.edu": 1, "another@purdue.edu": -1},
            community="cooomunity",
        )

        rv = client.get(
            "/notifications",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        notification_db_instance.delete.assert_called_once()
        notification_db_instance.add.assert_not_called()
        assert return_data["access_token"] == "AccessToken"
        assert len(return_data["data"]) == 0
        assert return_data["message"] == "Successfully got notifications"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200


def test_notification_post(client):
    """
    Tests that rating post works correctly
    """
    with patch("biit_server.notification_handler.Database") as mock_database:
        test_json = {
            "email": "steve@apple.com",
            "token": "token",
            "notification_id": "anid",
        }

        instance = mock_database.return_value

        rv = client.post(
            "/notifications",
            json=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "AccessToken"
        assert return_data["data"] == True
        assert return_data["message"] == "Successfully dismissed notification"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200

        instance.update.assert_called_once_with("anid", {"dismissed": True})
