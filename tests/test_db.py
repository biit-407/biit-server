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

    test_db = Database(test_collection_name, firestore_client=mock_db)

    test_db.add(test_data, id=test_data["id"])

    doc_ref = mock_db.collection(test_collection_name).document(test_data["id"])
    doc = doc_ref.get()

    assert doc.exists

    doc_json = doc.to_dict()

    assert doc_json["name"] == test_data["name"]
    assert doc_json["id"] == test_data["id"]


def test_database_get():
    """
    Tests that database library can accurately fetch from database given ID.
    """
    mock_db = MockFirestore()

    test_data = {"name": "Leroy", "id": 1337}

    test_collection_name = "users"

    mock_db.collection(test_collection_name).document(test_data["id"]).set(test_data)

    test_db = Database(test_collection_name, firestore_client=mock_db)

    doc = test_db.get(test_data["id"])

    assert doc.exists

    doc_json = doc.to_dict()

    assert doc_json["name"] == test_data["name"]
    assert doc_json["id"] == test_data["id"]


def test_database_query():
    """
    Tests that database library can accurately query database.
    """
    mock_db = MockFirestore()

    test_data_1 = {"name": "Leroy", "id": 1337}
    test_data_2 = {"name": "Julia", "id": 7}
    test_data_3 = {"name": "Adrian", "id": 2000}

    test_collection_name = "users"

    mock_db.collection(test_collection_name).document(test_data_1["id"]).set(
        test_data_1
    )
    mock_db.collection(test_collection_name).document(test_data_2["id"]).set(
        test_data_2
    )
    mock_db.collection(test_collection_name).document(test_data_3["id"]).set(
        test_data_3
    )

    test_db = Database(test_collection_name, firestore_client=mock_db)

    query_results = test_db.query("id", "==", test_data_1["id"])

    assert len(query_results) == 1

    doc = query_results[0]

    assert doc.exists

    doc_json = doc.to_dict()

    assert doc_json["name"] == test_data_1["name"]
    assert doc_json["id"] == test_data_1["id"]


def test_database_update():
    """
    Tests that database library can accurately query database.
    """
    mock_db = MockFirestore()

    test_data = {"name": "Leroy", "id": "1337"}
    test_update_data = {"name": "Olivia"}

    test_collection_name = "users"

    mock_db.collection(test_collection_name).document(test_data["id"]).set(test_data)

    test_db = Database(test_collection_name, firestore_client=mock_db)

    update_results = test_db.update(test_data["id"], test_update_data)

    assert update_results

    doc = mock_db.collection(test_collection_name).document(test_data["id"]).get()

    assert doc.exists

    doc_json = doc.to_dict()

    assert doc_json["id"] == test_data["id"]
    assert doc_json["name"] == test_update_data["name"]


def test_database_delete():
    """
    Tests that database library can delete documents from database.
    """
    mock_db = MockFirestore()

    test_data = {"name": "Leroy", "id": "1337"}

    test_collection_name = "users"

    mock_db.collection(test_collection_name).document(test_data["id"]).set(test_data)

    test_db = Database(test_collection_name, firestore_client=mock_db)

    update_results = test_db.delete(test_data["id"])

    assert update_results

    doc = mock_db.collection(test_collection_name).document(test_data["id"]).get()

    assert not doc.exists
