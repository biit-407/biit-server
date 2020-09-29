import pytest
from biit_server import create_app

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
    rv = client.post(
        "/community",
        json={
            "name": "Cool Community",
            "codeofconduct": "Eatmyshorts",
            "Admins": "Me,John,Jeff",
            "Members": "Me,John,Adam",
            "mpm": "Here",
            "meettype": "Here",
        },
        follow_redirects=True,
    )
    assert b"OK: community Created" == rv.data


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
    assert b"OK: community Returned" == rv.data


def test_community_put(client):
    """
    Tests that community put works correctly

    TODO this test needs to be modified when the database is connected
    """
    rv = client.put(
        "/community",
        query_string={
            "name": "TestCommunity",
            "token": "TestToken",
            "email": "Testemail@gmail.com",
        },
        follow_redirects=True,
    )
    assert b"OK: community Updated" == rv.data


def test_community_delete(client):
    """
    Tests that community delete works correctly

    TODO this test needs to be modified when the database is connected
    """
    rv = client.delete(
        "/community",
        query_string={
            "name": "TestCommunity",
            "token": "TestToken",
            "email": "Testemail@gmail.com",
        },
        follow_redirects=True,
    )
    assert b"OK: community Deleted" == rv.data


def test_community_join_post(client):
    """
    Tests that community post works correctly

    TODO this test needs to be modified when the database is connected
    """
    rv = client.post(
        "/community/1/join",
        json={"name": "Jeffery"},
        follow_redirects=True,
    )
    assert b"OK: Community Joined" == rv.data


def test_community_leave_post(client):
    """
    Tests that community post works correctly

    TODO this test needs to be modified when the database is connected
    """
    rv = client.post(
        "/community/1/leave",
        json={"name": "Jeffery"},
        follow_redirects=True,
    )
    assert b"OK: Community Left" == rv.data
