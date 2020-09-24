from mockfirestore import MockFirestore
import pytest

from biit_server.database import Database


def test_database_add():
    """
    Tests that database library can accurately add to database.
    """
    mock_db = MockFirestore()

    test_data = {"name": "Leroy", "id": 1337}

    test_collection_name = "users"

    test_db = Database(test_collection_name, firestore=mock_db)

    test_db.add(test_data, id=test_data["id"])

    doc_ref = mock_db.collection(test_collection_name).document(test_data["id"])
    doc = doc_ref.get()

    assert doc.exists

    doc_json = doc.to_dict()

    assert doc_json["name"] == test_data["name"]
    assert doc_json["id"] == test_data["id"]


def test_database_get():
    """
    Tests that database library can accurately add to database.
    """
    mock_db = MockFirestore()

    test_data = {"name": "Leroy", "id": 1337}

    test_collection_name = "users"

    mock_db.collection(test_collection_name).document(test_data["id"]).set(test_data)

    test_db = Database(test_collection_name, firestore=mock_db)

    doc = test_db.get(test_data["id"])

    assert doc.exists

    doc_json = doc.to_dict()

    assert doc_json["name"] == test_data["name"]
    assert doc_json["id"] == test_data["id"]
