from typing import Any, Dict, List

from google.cloud import firestore


class Database:
    def __init__(self, collection, firestore_client=None) -> None:
        """The constructor for the Database class. Used to instantiate a Database reference object.

        Args:
            collection (str): the name of the collection
            firestore (google.cloud.firestore.client): A Firestore client object, or a mock test object.

        Returns:
            None
        """
        super().__init__()
        self.collection_name = collection
        self.firestore = firestore_client if firestore is not None else firestore.client()
        self.collection_ref = self.firestore.collection(self.collection_name)

    def add(self, obj, id=None) -> bool:
        """Helper function to add object into the database.

        Args:
            obj (Dict[str, Any]): A Dictionary containing the data you want to insert.
            id (int, str): An identifying string or int. Optional.

        Returns:
            boolean, True if the document is successfully added, False if there was an error.
        """
        try:
            self.collection_ref.add(obj, document_id=id)
            return True
        except Exception:
            return False

    def get(self, id) -> Dict[str, Any]:
        """Helper function to get documents from the database.

        Args:
            id (int, str): An identifying string or int.

        Returns:
            Dict[str, Any] if the document is successfully added. Boolean value of False if there was an error.
        """
        try:
            results = self.collection_ref.document(id).get()
            return results
        except Exception:
            return False

    def query(self, field, operation, value) -> List[Dict[str, Any]]:
        """Helper function to query documents based on parameters.

        Args:
            field (str): The field that you want to query on.
            operation (str): Can be "==", ">=", "<=". Find out more at this link: https://googleapis.dev/python/firestore/latest/query.html#google.cloud.firestore_v1.query.Query.where
            value (str): The value you are comparing to.
        Returns:
            List[Dict[str, Any]] if there are no errors. Boolean value of False if there is an error.
        """
        try:
            results = self.collection_ref.where(field, operation, value).stream()
            return [value for value in results]
        except Exception:
            return False

    def update(self, id, update_dict) -> bool:
        """Helper function to query documents based on parameters.

        Args:
            id (str, int): The id of the document you want (email for us).
            update_dict (Dict[str, Any]): A dictionary of the fields you want to update
        Returns:
            List[Dict[str, Any]] if there are no errors. Boolean value of False if there is an error.
        """
        
        try:
            results = self.collection_ref.document(id)
            results.update(update_dict)
            return True
        except Exception:
            return False
