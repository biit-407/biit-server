from biit_server.app import create_app
from unittest.mock import patch
import pytest
from biit_server import community_stats_handler
import json


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


class MockCollection:
    def __init__(self):
        """Helper class to simulate a collection"""
        self.community = "Johnson"
        self.accepted_meetups = 0
        self.total_meetups = 0
        self.total_sessions = 0

    def to_dict(self):
        """Returns a mock collection entry"""
        return {
            "community": self.community,
            "accepted_meetups": self.accepted_meetups,
            "total_meetups": self.total_meetups,
            "total_sessions": self.total_sessions,
        }


def test_community_stats_get(client):
    """Tests that that get community stats endpoint works correctly"""
    with patch.object(
        community_stats_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.community_stats_handler.Database"
    ) as mock_database:
        instance = mock_database.return_value
        instance.get.return_value = MockCollection()
        instance.update.return_value = True

        test_json = {"token": "Toke", "email": "Testemail@gmail.com"}
        test_id = "Johnson"

        mock_azure_refresh_token.return_value = ("AccessToken", "RefreshToken")
        rv = client.get(
            f"/community/{test_id}/stats",
            query_string=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "AccessToken"
        assert return_data["data"]["community"] == "Johnson"
        assert return_data["data"]["accepted_meetups"] == 0
        assert return_data["data"]["total_meetups"] == 0
        assert return_data["data"]["total_sessions"] == 0
        assert return_data["message"] == "Community Stats Received"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200

        instance.get.assert_called_with(test_id)
