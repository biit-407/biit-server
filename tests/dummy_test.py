import pytest

from biit_server import create_app


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


def test_client_fixture(client):
    """
    Meta testcase, asserts that the client fixture works
    """
    assert client
