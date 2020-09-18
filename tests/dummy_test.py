import pytest

from biit_server import create_app


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


def test(client):
    rv = client.get("/account")
    print(rv.data)
    assert b"Failed to load JSON object" == rv.data
