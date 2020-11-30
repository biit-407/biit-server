from biit_server.meeting import Meeting
import json
import pytest
from biit_server import create_app
from biit_server.rating import Rating
from unittest.mock import call, patch

# Waiting on DB before adding tests


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


class MockCommunity:
    def __init__(self):
        """
        Helper class to simulate a community
        """
        self.id = "communityid"

    def to_dict(self):
        """"""
        return {"id": self.id}


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


class MockRating:
    def __init__(self, meeting_id, ratings_dict):
        self.meeting_id = meeting_id
        self.ratings_dict = ratings_dict

    def to_json(self):
        return {"meeting_id": self.meeting_id, "rating_dict": self.ratings_dict}


def test_rating_post_empty(client):
    """
    Tests that rating post works correctly
    """
    with patch("biit_server.rating_handler.Database") as mock_database:
        test_json = {
            "meeting_id": "random_string",
            "user": "steve@apple.com",
            "rating": 5,
            "community": "jahnsens",
            "token": "token",
        }

        instance = mock_database.return_value
        instance.add.return_value = True
        instance.get.side_effect = (
            lambda x: MockCommunity() if x == "jahnsens" else False
        )

        rv = client.post(
            "/rating",
            json=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "AccessToken"
        assert return_data["data"] == {
            "meeting_id": test_json["meeting_id"],
            "rating_dict": {test_json["user"]: test_json["rating"]},
            "community": "communityid",
        }
        assert return_data["message"] == "Rating created"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200

        instance.get.assert_has_calls(
            [call(test_json["meeting_id"]), call("jahnsens")], any_order=True
        )
        instance.add.assert_called_once_with(
            {
                "meeting_id": test_json["meeting_id"],
                "rating_dict": {test_json["user"]: test_json["rating"]},
                "community": "communityid",
            },
            id=test_json["meeting_id"],
        )


def test_rating_post_not_empty(client):
    """
    Tests that rating post works correctly
    """
    with patch("biit_server.rating_handler.Database") as mock_database, patch(
        "biit_server.rating_handler.Rating"
    ) as mock_rating:
        test_json = {
            "meeting_id": "random_string",
            "user": "steve@apple.com",
            "rating": 5,
            "community": "jahnsens",
            "token": "token",
        }

        mock_rating.return_value = Rating(
            meeting_id=test_json["meeting_id"],
            rating_dict={"grr@purdue.edu": 3},
            community="communityid",
        )

        instance = mock_database.return_value
        instance.get.side_effect = (
            lambda x: MockCommunity() if x == "jahnsens" else True
        )
        instance.update.return_value = True

        rv = client.post(
            "/rating",
            json=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "AccessToken"
        assert return_data["data"] == {
            "meeting_id": test_json["meeting_id"],
            "rating_dict": {
                test_json["user"]: test_json["rating"],
                "grr@purdue.edu": 3,
            },
            "community": "communityid",
        }
        assert return_data["message"] == "Rating created"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200

        instance.get.assert_has_calls(
            [call(test_json["meeting_id"]), call("jahnsens")], any_order=True
        )
        instance.update.assert_called_once_with(
            test_json["meeting_id"],
            {
                "rating_dict": {
                    test_json["user"]: test_json["rating"],
                    "grr@purdue.edu": 3,
                },
            },
        )


def test_rating_get(client):
    """
    Tests that rating get works correctly
    """
    with patch("biit_server.rating_handler.Database") as mock_database, patch(
        "biit_server.rating_handler.Rating"
    ) as mock_rating:
        query_data = {"meeting_id": "test_meeting", "token": "dabonem"}

        test_rating = Rating(meeting_id=query_data["meeting_id"], community="jahnsens")

        mock_rating.return_value = test_rating

        instance = mock_database.return_value
        instance.get.return_value = True

        rv = client.get(
            "/rating",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "AccessToken"
        assert return_data["data"] == {
            "meeting_id": query_data["meeting_id"],
            "rating_dict": {},
            "community": "jahnsens",
        }
        assert return_data["message"] == "Rating Received"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200

        instance.get.assert_called_once_with(query_data["meeting_id"])


def test_rating_get_past(client):
    """
    Tests that getting past ratings works correctly
    """
    with patch("biit_server.rating_handler.Database") as mock_database, patch(
        "biit_server.rating_handler.Rating"
    ) as mock_rating, patch("biit_server.rating_handler.Meeting") as mock_meeting:
        query_data = {
            "email": "paimon@purdue.edu",
            "meeting_id": "test_meeting",
            "token": "dabonem",
        }

        mock_rating.return_value = Rating(
            meeting_id=query_data["meeting_id"], rating_dict={"paimon@purdue.edu": -1}
        )
        mock_meeting.return_value = Meeting(
            user_list={"paimon@purdue.edu": 1},
            id=query_data["meeting_id"],
            timestamp=0,
            duration=60,
            location="WALC",
            meeting_type="in-person",
        )

        instance = mock_database.return_value
        instance.collection_ref.get.return_value = [1, 1, 1]

        rv = client.get(
            "/rating/pending",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "AccessToken"
        assert len(return_data["data"])
        assert return_data["message"] == "Rating Received"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200
