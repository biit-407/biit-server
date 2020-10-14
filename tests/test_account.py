import json

import pytest
from biit_server import create_app, account_handler
from unittest.mock import patch
from io import BytesIO
import biit_server


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


class MockAccount:
    def __init__(self, email):
        self.email = email

    def to_dict(self):
        return {"email": self.email}


def test_account_post(client):
    """
    Tests that account post works correctly


    """

    with patch.object(
        account_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.account_handler.Database"
    ) as mock_database:
        instance = mock_database.return_value
        instance.add.return_value = True
        mock_azure_refresh_token.return_value = (
            "yessir a new access token",
            "yes a new refresh token",
        )
        rv = client.post(
            "/account",
            json={
                "fname": "first",
                "lname": "last",
                "email": "test@email.com",
                "token": "ah a testing refresh token",
            },
            follow_redirects=True,
        )
        assert (
            b'{"access_token":"yessir a new access token","email":"test@email.com","fname":"first","lname":"last","message":"Account Created","refresh_token":"yes a new refresh token","status_code":200}\n'
            == rv.data
        )


def test_account_get(client):
    """
    Tests that account get works correctly


    """
    with patch.object(
        account_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.account_handler.Database"
    ) as mock_database:

        instance = mock_database.return_value

        query_data = {"email": "test@email.com", "token": "henlo"}
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")

        instance.get.return_value = MockAccount(query_data["email"])

        rv = client.get(
            "/account",
            query_string=query_data,
            follow_redirects=True,
        )

        assert (
            b'{"access_token":"RefreshToken","data":{"email":"test@email.com"},"message":"Account returned","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )


def test_account_put(client):
    """
    Tests that account put works correctly


    """
    with patch.object(
        account_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.account_handler.Database"
    ) as mock_database:
        instance = mock_database.return_value
        instance.update.return_value = True
        query_data = {"email": "test@email.com"}
        instance.get.return_value = MockAccount(query_data["email"])
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.put(
            "/account",
            query_string={
                "email": "test@email.com",
                "token": "TestToken",
                "updateFields": {"email": "e@mail.in.gov"},
            },
            follow_redirects=True,
        )
        assert (
            b'{"access_token":"RefreshToken","email":"test@email.com","message":"Account Updated","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )


def test_account_delete(client):
    """
    Tests that account delete works correctly


    """
    with patch.object(
        account_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.account_handler.Database"
    ) as mock_database, patch(
        "biit_server.account_handler.Storage"
    ) as mock_storage:
        instance = mock_database.return_value
        instance.delete.return_value = True
        inst_storage = mock_storage.return_value
        inst_storage.delete.return_value = True
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.delete(
            "/account",
            query_string={"email": "test@email.com", "token": "TestToken"},
            follow_redirects=True,
        )
        assert b"OK: Account deleted" == rv.data


def test_profile_post(client):
    """
    Tests that account delete works correctly


    """
    with patch.object(
        account_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.account_handler.Storage"
    ) as mock_storage:
        instance = mock_storage.return_value
        instance.add.return_value = True
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.post(
            "/profile",
            content_type="multipart/form-data",
            data={
                "email": "test@email.com",
                "token": "ah a testing refresh token",
                "file": b"garbage",
                "filename": "file.jpg",
            },
            follow_redirects=True,
        )
        assert (
            b'{"access_token":"RefreshToken","message":"File Uploaded","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )


def test_profile_get(client):
    """
    Tests that account delete works correctly


    """
    with patch.object(
        account_handler, "azure_refresh_token"
    ) as mock_azure_refresh_token, patch(
        "biit_server.account_handler.Storage"
    ) as mock_storage:
        instance = mock_storage.return_value
        instance.get.return_value = "hello"
        mock_azure_refresh_token.return_value = ("RefreshToken", "AccessToken")
        rv = client.get(
            "/profile",
            query_string={
                "email": "test@email.com",
                "token": "toke",
                "filename": "test.jpg",
            },
            follow_redirects=True,
        )
        assert (
            b'{"access_token":"RefreshToken","data":"hello","message":"File Received","refresh_token":"AccessToken","status_code":200}\n'
            == rv.data
        )
