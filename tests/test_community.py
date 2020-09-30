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


def test_community_post(client):
    """
    Tests that community post works correctly

    TODO this test needs to be modified when the database is connected
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.post(
            "/community",
            json={
                "name": "Cool Community",
                "codeofconduct": "Eatmyshorts",
                "Admins": "Me,John,Jeff",
                "Members": "Me,John,Adam",
                "mpm": "Here",
                "meettype": "Here",
                "token": "TestToken",
            },
            follow_redirects=True,
        )
        assert b'["RefreshToken","AccessToken","Community Created"]\n' == rv.data


def test_community_get(client):
    """
    Tests that community get works correctly

    TODO this test needs to be modified when the database is connected
    """
    rv = client.get(
        "/community",
        query_string={"name": "TestCommunity"},
        follow_redirects=True,
    )
    assert b"OK: Community Returned" == rv.data


def test_community_put(client):
    """
    Tests that community put works correctly

    TODO this test needs to be modified when the database is connected
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.put(
            "/community",
            query_string={
                "name": "TestCommunity",
                "token": "TestToken",
                "email": "Testemail@gmail.com",
            },
            follow_redirects=True,
        )
        assert b'["RefreshToken","AccessToken","Community Updated"]\n' == rv.data


def test_community_delete(client):
    """
    Tests that community delete works correctly

    TODO this test needs to be modified when the database is connected
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token:
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
        assert b'["RefreshToken","AccessToken","Community Deleted"]\n' == rv.data


def test_community_join_post(client):
    """
    Tests that community post works correctly

    TODO this test needs to be modified when the database is connected
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.post(
            "/community/1/join",
            json={"name": "Jeffery", "token": "Toke"},
            follow_redirects=True,
        )
        assert b'["RefreshToken","AccessToken","Community Joined"]\n' == rv.data


def test_community_leave_post(client):
    """
    Tests that community post works correctly

    TODO this test needs to be modified when the database is connected
    """
    with patch.object(
        community_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token:
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.post(
            "/community/1/leave",
            json={"name": "Jeffery", "token": "Toke"},
            follow_redirects=True,
        )
        assert b'["RefreshToken","AccessToken","Community Left"]\n' == rv.data
