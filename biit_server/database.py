from google.cloud import firestore


class Database:
    def __init__(self, collection, firestore=None):
        super().__init__()
        self.collection_name = collection
        self.firestore = firestore if firestore is not None else firestore.client()
        self.collection_ref = self.firestore.collection(self.collection_name)

    def add(self, obj, id=None) -> True:
        """Helper function to add object into database"""
        try:
            self.collection_ref.add(obj, id)
            return True
        except Exception:
            return False

    def get(self, id):
        """Helper function to get documents from the database"""
        try:
            results = self.collection_ref.document(id).get()
            return results
        except Exception:
            return False

    def query(self, attr, operation, value):
        """Helper function to query documents based on parameters"""
        try:
            results = self.collection_ref.where(attr, operation, value).stream()
            return [value for value in results]
        except Exception:
            return False
