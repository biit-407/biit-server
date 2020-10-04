from google.cloud import storage


class Storage:
    def __init__(self, bucket, storage_client=None) -> None:
        """The constructor for the Storage class. Used to instantiate a Bucket reference object.

        Args:
            bucket (str): the name of the bucket
            storage (google.cloud.storage.client): A storage client object, or a mock test object.

        Returns:
            None
        """
        super().__init__()
        self.name = bucket
        self.storage = storage_client if storage_client != None else storage.Client()
        self.bucket = self.storage.getbucket(self.name)

    def add(self, file, name: str) -> bool:
        """Helper function to add file into the storage bucket.

        Args:
            obj (Dict[str, Any]): A Dictionary containing the data you want to insert.
            name (str): An identifying string

        Returns:
            boolean, True if the document is successfully added, False if there was an error.
        """
        try:
            blob = self.bucket.blob(name)
            blob.upload_from_file(file)
            return True
        except Exception:
            return False

    def get(self, name):
        """Helper function to get documents from the database.

        Args:
            id (int, str): An identifying string or int.

        Returns:
            File if the document is successfully added. Boolean value of False if there was an error.
        """
        try:
            newfile = None
            blob = self.bucket.get_blob(name)
            blob.download_to_file(newfile)
            return newfile
        except Exception:
            return False
