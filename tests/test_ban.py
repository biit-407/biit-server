import pytest
from biit_server import create_app


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
    rv = client.post(
        "/ban",
        json={"banner": "first", "bannee": "last", "community": "com", "token": "test"},
        follow_redirects=True,
    )
    assert b"OK: last has been banned" == rv.data


def test_ban_put(client):
    """
    Tests that account get works correctly

    TODO this test needs to be modified when the database is connected
    """
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
    assert b"OK: last has been unbanned" == rv.data
