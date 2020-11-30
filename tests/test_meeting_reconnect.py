from datetime import timezone, datetime
import json
import pytest
from biit_server import create_app
from unittest.mock import patch

from biit_server.meeting import Meeting
from biit_server import meeting_handler


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
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return self.data


class MockUser:
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return self.data


def test_meeting_reconnect(client):
    """
    Tests that meeting reconnect works correctly
    """
    with patch("biit_server.meeting_handler.Database") as mock_database:
        test_json = {
            "email": "ryan@purdue.edu",
            "community": "Purdue Exponent",
            "token": "weareanewspaper",
            "user": "stephen@purdue.edu",
        }

        mock_json_db = {
            "ryan@purdue.edu": MockUser(
                {
                    "optIn": 1,
                    "covid": "gloves",
                    "meetType": "inperson",
                    "fname": "ryan",
                    "lname": "chen",
                    "email": "ryan@purdue.edu",
                }
            ),
            "stephen@purdue.edu": MockUser(
                {
                    "optIn": 1,
                    "covid": "gloves",
                    "meetType": "inperson",
                    "fname": "alisa",
                    "lname": "reynya",
                    "email": "stephen@purdue.edu",
                }
            ),
            "Purdue Exponent": MockCommunity(
                {
                    "id": "Purdue Exponent",
                    "Admins": ["ryan@purdue.edu"],
                    "Members": ["ryan@purdue.edu", "stephen@purdue.edu"],
                }
            ),
        }

        def mock_get(key):
            return mock_json_db.get(key)

        instance = mock_database.return_value
        instance.add.return_value = True
        instance.get = mock_get

        rv = client.post(
            "/meeting/reconnect",
            json=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())
        assert return_data["access_token"] == "AccessToken"
        assert return_data["data"]["community"] == "Purdue Exponent"
        assert return_data["data"]["user_list"] == {
            "ryan@purdue.edu": 0,
            "stephen@purdue.edu": 0,
        }
