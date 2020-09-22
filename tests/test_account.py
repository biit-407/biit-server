import pytest
from biit_server import create_app


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


def test_account_post(client):
    """
    Tests that account post works correctly

    TODO this test needs to be modified when the database is connected
    """
    rv = client.post(
        "/account",
        json={"fname": "first", "lname": "last", "email": "test@email.com"},
        follow_redirects=True,
    )
    assert b"OK: Account Created" == rv.data


def test_account_get(client):
    """
    Tests that account get works correctly

    TODO this test needs to be modified when the database is connected
    """
    rv = client.get(
        "/account",
        query_string={"email": "test@email.com"},
        follow_redirects=True,
    )
    assert b"OK: Account Returned" == rv.data


def test_account_put(client):
    """
    Tests that account put works correctly

    TODO this test needs to be modified when the database is connected
    """
    rv = client.put(
        "/account",
        query_string={"email": "test@email.com"},
        follow_redirects=True,
    )
    assert b"OK: Account Updated" == rv.data


def test_account_delete(client):
    """
    Tests that account delete works correctly

    TODO this test needs to be modified when the database is connected
    """
    rv = client.delete(
        "/account",
        query_string={"email": "test@email.com"},
        follow_redirects=True,
    )
    assert b"OK: Account Deleted" == rv.data
