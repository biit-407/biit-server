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


def test_meeting_algo(client):
    """
    Tests that meeting algorithm works correctly
    """
    with patch("biit_server.meeting_handler.Database") as mock_database:
        test_json = {
            "email": "ryan@purdue.edu",
            "community": "Purdue Exponent",
            "token": "weareanewspaper",
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
            "alisa@purdue.edu": MockUser(
                {
                    "optIn": 1,
                    "covid": "gloves",
                    "meetType": "inperson",
                    "fname": "alisa",
                    "lname": "reynya",
                    "email": "alisa@purdue.edu",
                }
            ),
            "Purdue Exponent": MockCommunity(
                {
                    "id": "Purdue Exponent",
                    "Admins": ["ryan@purdue.edu"],
                    "Members": ["ryan@purdue.edu", "alisa@purdue.edu"],
                }
            ),
        }

        def mock_get(key):
            return mock_json_db.get(key)

        instance = mock_database.return_value
        instance.add.return_value = True
        instance.get = mock_get

        rv = client.get(
            "/matchup",
            query_string=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())
        print(return_data.get("data"))
        assert return_data["access_token"] == "AccessToken"
        assert len(return_data.get("data")) == 1


def test_meeting_algo_filter_opt_out(client):
    """
    Tests that meeting algorithm works correctly
    """
    with patch("biit_server.meeting_handler.Database") as mock_database:
        test_json = {
            "email": "ryan@purdue.edu",
            "community": "Purdue Exponent",
            "token": "weareanewspaper",
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
            "alisa@purdue.edu": MockUser(
                {
                    "optIn": 1,
                    "covid": "gloves",
                    "meetType": "inperson",
                    "fname": "alisa",
                    "lname": "reynya",
                    "email": "alisa@purdue.edu",
                }
            ),
            "alex@purdue.edu": MockUser(
                {
                    "optIn": 0,
                    "covid": "gloves",
                    "meetType": "inperson",
                    "fname": "alex",
                    "lname": "weliever",
                    "email": "alex@purdue.edu",
                }
            ),
            "jordan@purdue.edu": MockUser(
                {
                    "optIn": 0,
                    "covid": "gloves",
                    "meetType": "inperson",
                    "fname": "jordan",
                    "lname": "smith",
                    "email": "jordan@purdue.edu",
                }
            ),
            "Purdue Exponent": MockCommunity(
                {
                    "id": "Purdue Exponent",
                    "Admins": ["ryan@purdue.edu"],
                    "Members": [
                        "ryan@purdue.edu",
                        "alisa@purdue.edu",
                        "alex@purdue.edu",
                        "jordan@purdue.edu",
                    ],
                }
            ),
        }

        def mock_get(key):
            return mock_json_db.get(key)

        instance = mock_database.return_value
        instance.add.return_value = True
        instance.get = mock_get

        rv = client.get(
            "/matchup",
            query_string=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())
        print(return_data.get("data"))
        assert return_data["access_token"] == "AccessToken"
        assert len(return_data.get("data")) == 1


def test_meeting_algo_different_preferences(client):
    """
    Tests that meeting algorithm works correctly
    """
    with patch("biit_server.meeting_handler.Database") as mock_database:
        test_json = {
            "email": "ryan@purdue.edu",
            "community": "Purdue Exponent",
            "token": "weareanewspaper",
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
            "alisa@purdue.edu": MockUser(
                {
                    "optIn": 1,
                    "covid": "gloves",
                    "meetType": "inperson",
                    "fname": "alisa",
                    "lname": "reynya",
                    "email": "alisa@purdue.edu",
                }
            ),
            "alex@purdue.edu": MockUser(
                {
                    "optIn": 1,
                    "covid": "mask",
                    "meetType": "zoom",
                    "fname": "alex",
                    "lname": "weliever",
                    "email": "alex@purdue.edu",
                }
            ),
            "jordan@purdue.edu": MockUser(
                {
                    "optIn": 1,
                    "covid": "mask",
                    "meetType": "zoom",
                    "fname": "jordan",
                    "lname": "smith",
                    "email": "jordan@purdue.edu",
                }
            ),
            "Purdue Exponent": MockCommunity(
                {
                    "id": "Purdue Exponent",
                    "Admins": ["ryan@purdue.edu"],
                    "Members": [
                        "ryan@purdue.edu",
                        "alisa@purdue.edu",
                        "alex@purdue.edu",
                        "jordan@purdue.edu",
                    ],
                }
            ),
        }

        def mock_get(key):
            return mock_json_db.get(key)

        instance = mock_database.return_value
        instance.add.return_value = True
        instance.get = mock_get

        rv = client.get(
            "/matchup",
            query_string=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())
        print(return_data.get("data"))
        assert return_data["access_token"] == "AccessToken"
        assert len(return_data.get("data")) == 2


def test_meeting_algo_not_enough_users(client):
    """
    Tests that meeting algorithm works correctly
    """
    with patch("biit_server.meeting_handler.Database") as mock_database:
        test_json = {
            "email": "ryan@purdue.edu",
            "community": "Purdue Exponent",
            "token": "weareanewspaper",
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
            "alisa@purdue.edu": MockUser(
                {
                    "optIn": 1,
                    "covid": "gloves",
                    "meetType": "inperson",
                    "fname": "alisa",
                    "lname": "reynya",
                    "email": "alisa@purdue.edu",
                }
            ),
            "alex@purdue.edu": MockUser(
                {
                    "optIn": 1,
                    "covid": "mask",
                    "meetType": "zoom",
                    "fname": "alex",
                    "lname": "weliever",
                    "email": "alex@purdue.edu",
                }
            ),
            "jordan@purdue.edu": MockUser(
                {
                    "optIn": 1,
                    "covid": "mask",
                    "meetType": "zoom",
                    "fname": "jordan",
                    "lname": "smith",
                    "email": "jordan@purdue.edu",
                }
            ),
            "Purdue Exponent": MockCommunity(
                {
                    "Admins": ["ryan@purdue.edu"],
                    "Members": [
                        "ryan@purdue.edu",
                    ],
                }
            ),
        }

        def mock_get(key):
            return mock_json_db.get(key)

        instance = mock_database.return_value
        instance.add.return_value = True
        instance.get = mock_get

        rv = client.get(
            "/matchup",
            query_string=test_json,
            follow_redirects=True,
        )

        assert (
            rv.data.decode()
            == "Internal Server Error: Not enough users in this community: 1. Need at least two."
        )
