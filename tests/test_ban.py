import pytest
from biit_server import create_app, ban_handler
from unittest.mock import patch


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


def test_ban_post(client):
    """
    Tests that account post works correctly

    TODO this test needs to be modified when the database is connected
    """
    with patch.object(ban_handler, "azure_refresh_token") as mock_azure_refresh_token:
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
        assert b'["RefreshToken","AccessToken","last has been banned"]\n' == rv.data


def test_ban_put(client):
    """
    Tests that account get works correctly

    TODO this test needs to be modified when the database is connected
    """
    with patch.object(ban_handler, "azure_refresh_token") as mock_azure_refresh_token:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
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
        assert b'["RefreshToken","AccessToken","last has been unbanned"]\n' == rv.data
