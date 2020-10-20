from enum import Enum
from typing import Any, Dict, List


class UserNotInMeetingException(Exception):
    def __init__(self, user: str):
        super().__init__(f"{user} was not in meeting!")


class UserInMeetingException(Exception):
    def __init__(self, user: str):
        super().__init__(f"{user} is already in meeting!")


class MeetingType(Enum):
    IN_PERSON = 0
    VIRTUAL = 1


class MeetingFunction(Enum):
    REMOVE = 0
    ADD = 1


class Meeting:
    def __init__(
        self,
        user_list=[],
        id=None,
        timestamp=None,
        duration=0,
        location=None,
        meeting_type=None,
        document_snapshot=None,
    ):
        if document_snapshot != None:
            user_list = document_snapshot.get("user_list")
            id = document_snapshot.get("id")
            timestamp = document_snapshot.get("timestamp")
            duration = document_snapshot.get("duration")
            location = document_snapshot.get("location")
            meeting_type = document_snapshot.get("meeting_type")

        self.user_list = user_list
        self.id = id
        self.timestamp = timestamp
        self.duration = duration
        self.location = location
        self.meeting_type = meeting_type

    def add_user(self, user) -> List[str]:
        self.user_list.append(user)

    def remove_user(self, target_user) -> List[str]:
        if target_user not in self.user_list:
            raise UserNotInMeetingException

        self.user_list = [user for user in self.user_list if user != target_user]

        return self.user_list

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "duration": self.duration,
            "user_list": self.user_list,
            "location": self.location,
            "meettype": self.meeting_type,
        }
