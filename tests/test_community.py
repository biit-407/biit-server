import json
import pytest
from biit_server import create_app, community_handler
from unittest.mock import patch

# Waiting on DB before adding tests


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


class MockCollectionLeave:
    def __init__(self, test_data):
        """Helper class to simulate a collection"""
        self.name = "mock"
        self.members = [test_data]

    def to_json(self):
        """Returns a mock collection entry"""
        return {"name": self.name, "Members": self.members}


def test_community_post(client):
    """
    Tests that community post works correctly
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.community_handler.Database"
    ) as mock_database:
        instance = mock_database.return_value
        instance.add.return_value = True

        test_json = {
            "name": "Cool Community",
            "codeofconduct": "Eatmyshorts",
            "Admins": "Me,John,Jeff",
            "Members": "Me,John,Adam",
            "mpm": "Here",
            "meettype": "Here",
            "token": "TestToken",
        }

        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.post(
            "/community",
            json=test_json,
            follow_redirects=True,
        )
        assert (
            b'{"access_token":"RefreshToken","message":"Community Created","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )

        instance.add.assert_called_once_with(test_json, id=test_json["name"])


def test_community_get(client):
    """
    Tests that community get works correctly
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.community_handler.Database"
    ) as mock_database:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")

        instance = mock_database.return_value

        query_data = {
            "name": "TestCommunity",
        }

        instance.get.return_value = query_data

        rv = client.get(
            "/community",
            query_string={"name": "TestCommunity", "token": "dabonem"},
            follow_redirects=True,
        )

        assert (
            b'{"access_token":"RefreshToken","data":{"name":"TestCommunity"},"message":"Community Received","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )

        instance.get.assert_called_once_with("TestCommunity")


def test_community_put(client):
    """
    Tests that community put works correctly
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.community_handler.Database"
    ) as mock_database:
        instance = mock_database.return_value
        instance.update.return_value = True

        test_json = {
            "name": "TestCommunity",
            "token": "TestToken",
            "email": "Testemail@gmail.com",
            "updateFields": {"name": "lanes"},
        }

        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.put(
            "/community",
            query_string=test_json,
            follow_redirects=True,
        )
        assert (
            b'{"access_token":"RefreshToken","message":"Community Updated","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )

        instance.update.assert_called_once_with(
            test_json["name"], test_json["updateFields"]
        )


def test_community_delete(client):
    """
    Tests that community delete works correctly
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.community_handler.Database"
    ) as mock_database:
        instance = mock_database.return_value
        instance.delete.return_value = True
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.delete(
            "/community",
            query_string={
                "name": "TestCommunity",
                "token": "TestToken",
                "email": "Testemail@gmail.com",
            },
            follow_redirects=True,
        )
        assert (
            b'{"access_token":"RefreshToken","message":"Community Deleted","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )

        instance.delete.assert_called_once_with("TestCommunity")


def test_community_join_post(client):
    """
    Tests that community post works correctly
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.community_handler.Database"
    ) as mock_database:
        instance = mock_database.return_value
        instance.get.return_value = MockCollection()
        instance.update.return_value = True

        test_data = {"name": "Jeffery", "token": "Toke", "email": "Testemail@gmail.com"}
        test_id = 1

        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.post(
            f"/community/{test_id}/join",
            json=test_data,
            follow_redirects=True,
        )
        assert (
            b'{"access_token":"RefreshToken","message":"Community Joined","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )

        instance.get.assert_called_once_with(test_id)
        instance.update.assert_called_once_with(test_id, {"Members": [test_data]})


def test_community_leave_post(client):
    """
    Tests that community post works correctly
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.community_handler.Database"
    ) as mock_database:
        test_data = {"name": "Jeffery", "token": "Toke", "email": "Testemail@gmail.com"}
        test_id = 1

        instance = mock_database.return_value
        instance.get.return_value = MockCollectionLeave(test_data)
        instance.update.return_value = True

        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.post(
            f"/community/{test_id}/leave",
            json=test_data,
            follow_redirects=True,
        )

        assert (
            b'{"access_token":"RefreshToken","message":"Community Left","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )

        instance.get.assert_called_once_with(test_id)
        instance.update.assert_called_once_with(test_id, {"Members": []})
