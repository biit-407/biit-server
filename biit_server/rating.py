from typing import Dict

class RatingAlreadySetException(Exception):
    def __init__(self, user: str):
        super().__init__(f"Rating for {user} has already been set!")

class Rating:
    def __init__(self, meeting_id=None, document_snapshot=None, rating_dict=None):
        """
        Args: 
            meeting_id: int -> the ID of the meetup
            rating_dict: Dict[str, int] -> user is key, number of stars is value
            document_snapshot: google.cloud.firestore_v1.document.DocumentSnapshot ->
                Just in case it is easier to send in the document snapshot
                from Firestore
            
        """
        if document_snapshot != None:
            meeting_id = document_snapshot.get("meeting_id")
            rating_dict = document_snapshot.get("rating_dict")

        self.meeting_id = meeting_id
        self.rating_dict = rating_dict

    def to_dict(self):
        return {
            "meeting_id": self.meeting_id,
            "rating_dict": self.rating_dict
        }
    
    def set_rating(self, user: str, rating: int) -> Dict[str, int]:
        if user in self.rating_dict:
            raise RatingAlreadySetException

        self.rating_dict[user] = rating

        return self.rating_dict
    

    def get_ratings(self) -> Dict[str, int]:
        return self.rating_dict
    
    def get_meeting_id(self) -> Dict[str, int]:
        return self.meeting_id