import json
import pytest
from biit_server import create_app, meeting_handler
from unittest.mock import patch

from biit_server.meeting import Meeting


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


class MockCollection:
    def __init__(self):
        """Helper class to simulate a collection"""
        self.name = "mock"

    def to_json(self):
        """Returns a mock collection entry"""
        return {"name": self.name, "Members": []}

    def to_dict(self):
        """Returns a mock collection entry"""
        return {"name": self.name, "Members": []}


class MockCollectionLeave:
    def __init__(self, test_data):
        """Helper class to simulate a collection"""
        self.name = "mock"
        self.members = [test_data]

    def to_json(self):
        """Returns a mock collection entry"""
        return {"name": self.name, "Members": self.members}

    def to_dict(self):
        """Returns a mock collection entry"""
        return {"name": self.name, "Members": self.members}


class MockCommunity:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {"name": self.name}


def test_meeting_post(client):
    """
    Tests that meeting post works correctly
    """
    with patch.object(
        meeting_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.meeting_handler.Database"
    ) as mock_database:
        test_json = {
            "timestamp": "noon",
            "location": "Mondstadt",
            "user_list": ["paimon@purdue.edu", "traveller@purdue.edu"],
            "meettype": "chance_meeting",
            "duration": 30,
            "token": "TestToken",
        }

        instance = mock_database.return_value
        instance.add.return_value = True

        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.post(
            "/meeting",
            json=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "RefreshToken"
        assert len(return_data["data"]["id"]) == 64
        assert return_data["data"]["timestamp"] == test_json["timestamp"]
        assert return_data["data"]["location"] == test_json["location"]
        assert return_data["data"]["meettype"] == test_json["meettype"]
        assert return_data["data"]["user_list"] == test_json["user_list"]
        assert return_data["message"] == "Meeting created"
        assert return_data["refresh_token"] == "AccessToken"
        assert return_data["status_code"] == 200


def test_meeting_get(client):
    """
    Tests that meeting get works correctly
    """
    with patch.object(
        meeting_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.meeting_handler.Database"
    ) as mock_database, patch(
        "biit_server.meeting_handler.Meeting"
    ) as mock_meeting:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")

        instance = mock_database.return_value
        instance.get.return_value = True

        query_data = {"id": "TestMeeting", "token": "dabonem"}

        test_json = {
            "id": query_data["id"],
            "user_list": ["beidou@purdue.edu"],
            "duration": 110,
            "location": "Li Yue",
            "meettype": "Gacha",
            "timestamp": "noon",
        }

        mock_meeting.return_value = Meeting(
            id=test_json["id"],
            user_list=test_json["user_list"],
            duration=test_json["duration"],
            location=test_json["location"],
            meeting_type=test_json["meettype"],
            timestamp=test_json["timestamp"],
        )

        rv = client.get(
            "/meeting",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "RefreshToken"
        assert return_data["data"]["timestamp"] == test_json["timestamp"]
        assert return_data["data"]["location"] == test_json["location"]
        assert return_data["data"]["meettype"] == test_json["meettype"]
        assert return_data["data"]["user_list"] == test_json["user_list"]
        assert return_data["message"] == "Meeting retrieved"
        assert return_data["refresh_token"] == "AccessToken"
        assert return_data["status_code"] == 200

        instance.get.assert_called_once_with("TestMeeting")


def test_meeting_put(client):
    """
    Tests that meeting put works correctly
    """
    with patch.object(
        meeting_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.meeting_handler.Database"
    ) as mock_database, patch(
        "biit_server.meeting_handler.Meeting"
    ) as mock_meeting:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")

        instance = mock_database.return_value
        instance.get.return_value = True
        instance.update.return_value = True

        query_data = {
            "id": "TestMeeting",
            "token": "dabonem",
            "updateFields": {"duration": 30},
        }

        test_json = {
            "id": query_data["id"],
            "user_list": ["beidou@purdue.edu"],
            "duration": query_data["updateFields"]["duration"],
            "location": "Li Yue",
            "meettype": "Gacha",
            "timestamp": "noon",
        }

        mock_meeting.return_value = Meeting(
            id=test_json["id"],
            user_list=test_json["user_list"],
            duration=query_data["updateFields"]["duration"],
            location=test_json["location"],
            meeting_type=test_json["meettype"],
            timestamp=test_json["timestamp"],
        )

        rv = client.put(
            "/meeting",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "RefreshToken"
        assert return_data["data"]["timestamp"] == test_json["timestamp"]
        assert return_data["data"]["location"] == test_json["location"]
        assert return_data["data"]["meettype"] == test_json["meettype"]
        assert return_data["data"]["user_list"] == test_json["user_list"]
        assert return_data["data"]["duration"] == query_data["updateFields"]["duration"]
        assert return_data["message"] == "Meeting updated"
        assert return_data["refresh_token"] == "AccessToken"
        assert return_data["status_code"] == 200


def test_community_delete(client):
    """
    Tests that community delete works correctly
    """
    with patch.object(
        meeting_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.meeting_handler.Database"
    ) as mock_database, patch(
        "biit_server.meeting_handler.Meeting"
    ) as mock_meeting:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")

        instance = mock_database.return_value
        instance.delete.return_value = True

        query_data = {
            "id": "TestMeeting",
            "token": "dabonem",
        }

        test_json = {
            "id": query_data["id"],
            "user_list": ["amber@purdue.edu"],
            "duration": 110,
            "location": "Mondstatd",
            "meettype": "LicenseTest",
            "timestamp": "noon",
        }

        mock_meeting.return_value = Meeting(
            id=test_json["id"],
            user_list=test_json["user_list"],
            duration=test_json["duration"],
            location=test_json["location"],
            meeting_type=test_json["meettype"],
            timestamp=test_json["timestamp"],
        )

        rv = client.delete(
            "/meeting",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["message"] == "Meeting deleted"
        assert return_data["refresh_token"] == "AccessToken"
        assert return_data["status_code"] == 200

        instance.delete.assert_called_once_with(query_data["id"])


def test_meeting_user_put_join(client):
    """
    Tests that community post works correctly
    """
    with patch.object(
        meeting_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.meeting_handler.Database"
    ) as mock_database, patch(
        "biit_server.meeting_handler.Meeting"
    ) as mock_meeting:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")

        instance = mock_database.return_value
        instance.delete.return_value = True

        query_data = {
            "id": "TestMeeting",
            "email": "traveller@purdue.edu",
            "token": "dabonem",
            "function": 1,
        }

        test_json = {
            "id": query_data["id"],
            "user_list": ["amber@purdue.edu"],
            "duration": 110,
            "location": "Mondstatd",
            "meettype": "LicenseTest",
            "timestamp": "noon",
        }

        mocked_meeting = Meeting(
            id=test_json["id"],
            user_list=test_json["user_list"],
            duration=test_json["duration"],
            location=test_json["location"],
            meeting_type=test_json["meettype"],
            timestamp=test_json["timestamp"],
        )

        mock_meeting.return_value = mocked_meeting

        rv = client.put(
            f"/meeting/user",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "RefreshToken"
        assert return_data["data"]["timestamp"] == test_json["timestamp"]
        assert return_data["data"]["location"] == test_json["location"]
        assert return_data["data"]["meettype"] == test_json["meettype"]
        assert return_data["data"]["user_list"] == test_json["user_list"]
        assert return_data["data"]["duration"] == test_json["duration"]
        assert return_data["message"] == "User added"
        assert return_data["refresh_token"] == "AccessToken"
        assert return_data["status_code"] == 200


# def test_community_leave_post(client):
#     """
#     Tests that community post works correctly
#     """
#     with patch.object(
#         community_handler, "azure_refresh_token"
#     ) as mock_azure_refresh_token, patch(
#         "biit_server.community_handler.Database"
#     ) as mock_database:
#         test_data = {"token": "Toke", "email": "Testemail@gmail.com"}
#         test_id = "Johnson"

#         instance = mock_database.return_value
#         instance.get.return_value = MockCollectionLeave(test_data["email"])
#         instance.update.return_value = True

#         mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
#         rv = client.post(
#             f"/community/{test_id}/leave",
#             json=test_data,
#             follow_redirects=True,
#         )

#         assert (
#             b'{"access_token":"RefreshToken","data":{"Members":["Testemail@gmail.com"],"name":"mock"},"message":"Community Left","refresh_token":"AccessToken","status_code":200}\n'
#             == rv.data
#         )

#         instance.get.assert_called_with(test_id)
#         instance.update.assert_called_once_with(test_id, {"Members": []})
