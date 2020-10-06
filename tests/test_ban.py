import pytest
from biit_server import create_app, ban_handler
from unittest.mock import patch
from mockfirestore import MockFirestore


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


class MockBanEmpty:
    def __init__(self):
        self.bans = []

    def to_dict(self):
        return {"bans": self.bans}


class MockBan:
    def __init__(self, member):
        self.bans = [member]

    def to_dict(self):
        return {"bans": self.bans}


def test_ban_post(client):
    """
    Tests that account post works correctly

    TODO this test needs to be modified when the database is connected
    """
    with patch.object(
        ban_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.ban_handler.Database"
    ) as mock_database:
        instance = mock_database.return_value
        instance.get.return_value = MockBanEmpty()
        instance.update.return_value = True

        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.post(
            "/ban",
            json={
                "banner": "first",
                "bannee": "last",
                "community": "com",
                "token": "test",
            },
            follow_redirects=True,
        )
        assert (
            b'{"access_token":"RefreshToken","message":"last has been banned","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )


def test_ban_put(client):
    """
    Tests that account get works correctly

    TODO this test needs to be modified when the database is connected
    """
    with patch.object(
        ban_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.ban_handler.Database"
    ) as mock_database:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")

        test_data = {
            "banner": "first",
            "bannee": "last",
            "community": "com",
            "token": "test",
        }

        instance = mock_database.return_value
        instance.get.return_value = MockBan({"name": "last", "ordered_by": "first"})
        instance.update.return_value = True
        rv = client.put(
            "/ban",
            query_string={
                "banner": "first",
                "bannee": "last",
                "community": "com",
                "token": "test",
            },
            follow_redirects=True,
        )
        assert (
            b'{"access_token":"RefreshToken","message":"last has been unbanned","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )
