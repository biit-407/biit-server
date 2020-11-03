from biit_server.utils import send_discord_message
from google.cloud import storage
import base64


class Storage:
    def __init__(self, bucket, storage_client=None) -> None:
        """The constructor for the Storage class. Used to instantiate a Bucket reference object.

        Args:
            bucket (str): the name of the bucket
            storage (google.cloud.storage.client): A storage client object

        Returns:
            None
        """
        super().__init__()
        self.name = bucket
        self.storage = storage_client if storage_client != None else storage.Client()
        self.bucket = self.storage.get_bucket(self.name)

    def add(self, file, name: str) -> bool:
        """Helper function to add file into the storage bucket.

        Args:
            file (file): A File-like object to be uploaded to the bucket
            name (str): Naming for the blob object

        Returns:
            boolean, True if the document is successfully added, False if there was an error.
        """
        blob = self.bucket.blob(name)
        blob.upload_from_string(file)
        return True

    def get(self, name):
        """Helper function to get documents from the database.

        Args:
            name (str): The name of the blob to be found

        Returns:
            File if the document is successfully returned. Boolean value of False if there was an error.
        """
        try:
            blob = self.bucket.get_blob(name)
            if blob == None:
                send_discord_message(
                    f"Could not find profile picture for filename {name}"
                )
            file_obj = blob.download_as_string()
            byte_file = base64.b64encode(file_obj)
            return byte_file.decode("ascii")
        except Exception:
            return False

    def delete(self, name):
        """Helper function to delete documents from the database.

        Args:
            name (str): The name of the blob to be found

        Returns:
            True if deleted
        """
        blob = self.bucket.get_blob(name)

        if blob:
            file_obj = blob.delete()
        return True
