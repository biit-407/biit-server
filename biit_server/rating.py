from typing import Dict


class RatingAlreadySetException(Exception):
    def __init__(self, user: str):
        super().__init__(f"Rating for {user} has already been set!")


class Rating:
    def __init__(
        self, meeting_id=None, document_snapshot=None, rating_dict=None, community=None
    ):
        """
        Args:
            meeting_id: int -> the ID of the meetup
            rating_dict: Dict[str, int] -> user is key, number of stars is value
            community: str -> the ID of the community that generated this rating
            document_snapshot: google.cloud.firestore_v1.document.DocumentSnapshot ->
                Just in case it is easier to send in the document snapshot
                from Firestore

        """
        if document_snapshot != None:
            document_data = document_snapshot.to_dict()
            meeting_id = document_data.get("meeting_id")
            rating_dict = document_data.get("rating_dict")
            community = document_data.get("community")

        self.meeting_id = meeting_id
        self.rating_dict = {} if rating_dict == None else rating_dict
        self.community = community

    def to_dict(self):
        return {
            "meeting_id": self.meeting_id,
            "rating_dict": self.rating_dict,
            "community": self.community,
        }

    def set_rating(self, user: str, rating: int) -> Dict[str, int]:
        self.rating_dict[user] = rating

        return self.rating_dict

    def get_ratings(self) -> Dict[str, int]:
        return self.rating_dict

    def get_meeting_id(self) -> Dict[str, int]:
        return self.meeting_id

    def get_commnuity(self) -> str:
        return self.community
