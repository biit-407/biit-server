from biit_server.feedback import Feedback
from datetime import datetime
import json
from fastcore.basics import store_attr
import pytest
from biit_server import create_app
from unittest.mock import patch


@pytest.fixture
def client():
    cli = create_app()
    cli.config["TESTING"] = True
    with cli.test_client() as client:
        yield client


def test_feedback_post(client):
    """
    Tests that feedback post works correctly
    """
    with patch("biit_server.feedback_handler.Database") as mock_database:
        timestamp = datetime.now()

        test_json = {
            "email": "email@email.com",
            "timestamp": timestamp.isoformat(),
            "title": "feedback-title",
            "text": "feedback-text",
            "feedback_type": 1,
            "feedback_status": 4,
            "token": "TestToken",
        }

        instance = mock_database.return_value
        instance.add.return_value = True

        rv = client.post(
            "/feedback",
            json=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "AccessToken"
        assert return_data["data"]["id"]
        assert return_data["data"]["email"] == test_json["email"]
        assert return_data["data"]["timestamp"] == test_json["timestamp"]
        assert return_data["data"]["title"] == test_json["title"]
        assert return_data["data"]["text"] == test_json["text"]
        assert return_data["data"]["feedback_type"] == test_json["feedback_type"]
        assert return_data["data"]["feedback_status"] == test_json["feedback_status"]
        assert return_data["message"] == "Feedback created"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200


def test_feedback_get(client):
    """
    Tests that feedback get works correctly
    """
    with patch("biit_server.feedback_handler.Database") as mock_database, patch(
        "biit_server.feedback_handler.Feedback"
    ) as mock_feedback:

        instance = mock_database.return_value
        instance.get.return_value = True

        query_data = {
            "id": "TestFeedback",
            "token": "dabonem",
            "email": "email@email.com",
        }
        timestamp = datetime.now()

        test_json = {
            "email": "email@email.com",
            "timestamp": timestamp.isoformat(),
            "title": "feedback-title",
            "text": "feedback-text",
            "feedback_type": 1,
            "feedback_status": 4,
            "token": "TestToken",
        }

        mock_feedback.return_value = Feedback(
            id="TestFeedback",
            email="email@email.com",
            timestamp=timestamp.isoformat(),
            title="feedback-title",
            text="feedback-text",
            feedback_type=1,
            feedback_status=4,
        )

        rv = client.get(
            "/feedback",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "AccessToken"
        assert return_data["data"]["id"]
        assert return_data["data"]["email"] == test_json["email"]
        assert return_data["data"]["timestamp"] == test_json["timestamp"]
        assert return_data["data"]["title"] == test_json["title"]
        assert return_data["data"]["text"] == test_json["text"]
        assert return_data["data"]["feedback_type"] == test_json["feedback_type"]
        assert return_data["data"]["feedback_status"] == test_json["feedback_status"]
        assert return_data["message"] == "Feedback retrieved"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200

        instance.get.assert_called_once_with("TestFeedback")


def test_feedback_delete(client):
    """
    Tests that feedback delete works correctly
    """
    with patch("biit_server.feedback_handler.Database") as mock_database, patch(
        "biit_server.feedback_handler.Feedback"
    ) as mock_feedback:

        instance = mock_database.return_value
        instance.delete.return_value = True
        timestamp = datetime.now()

        query_data = {
            "id": "TestFeedback",
            "token": "dabonem",
            "email": "email@email.com",
        }

        mock_feedback.return_value = Feedback(
            id="TestFeedback",
            email="email@email.com",
            timestamp=timestamp.isoformat(),
            title="feedback-title",
            text="feedback-text",
            feedback_type=1,
            feedback_status=4,
        )

        rv = client.delete(
            "/feedback",
            query_string=query_data,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["access_token"] == "AccessToken"
        assert return_data["message"] == "Feedback deleted"
        assert return_data["status_code"] == 200

        instance.delete.assert_called_once_with(query_data["id"])


def test_report_user(client):
    """
    Tests that feedback post works correctly
    """
    with patch("biit_server.feedback_handler.Database") as mock_database:
        timestamp = datetime.now()

        test_json = {
            "email": "email@email.com",
            "timestamp": timestamp.isoformat(),
            "title": "Reporting Test@test.com",
            "text": "He spilt coffee on me",
            "feedback_type": 2,
            "feedback_status": 4,
            "token": "TestToken",
        }

        instance = mock_database.return_value
        instance.add.return_value = True

        rv = client.post(
            "/feedback",
            json=test_json,
            follow_redirects=True,
        )

        return_data = json.loads(rv.data.decode())

        assert return_data["access_token"] == "AccessToken"
        assert return_data["data"]["id"]
        assert return_data["data"]["email"] == test_json["email"]
        assert return_data["data"]["timestamp"] == test_json["timestamp"]
        assert return_data["data"]["title"] == test_json["title"]
        assert return_data["data"]["text"] == test_json["text"]
        assert return_data["data"]["feedback_type"] == test_json["feedback_type"]
        assert return_data["data"]["feedback_status"] == test_json["feedback_status"]
        assert return_data["message"] == "Feedback created"
        assert return_data["refresh_token"] == "RefreshToken"
        assert return_data["status_code"] == 200
