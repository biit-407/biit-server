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
        user_list={},
        id=None,
        timestamp=None,
        duration=0,
        location=None,
        meeting_type=None,
        document_snapshot=None,
    ):
        if document_snapshot != None:
            document_dict = document_snapshot.to_dict()
            user_list = document_dict["user_list"]
            id = document_dict["id"]
            timestamp = document_dict["timestamp"]
            duration = document_dict["duration"]
            location = document_dict["location"]
            meeting_type = document_dict["meettype"]

        self.user_list = user_list
        self.id = id
        self.timestamp = timestamp
        self.duration = duration
        self.location = location
        self.meeting_type = meeting_type

    def add_user(self, user) -> Dict[str, bool]:
        self.user_list[user] = None

    def accept_meeting(self, user) -> Dict[str, bool]:
        self.user_list[user] = True

    def decline_meeting(self, user) -> Dict[str, bool]:
        self.user_list[user] = False

    def remove_user(self, target_user) -> Dict[str, bool]:
        if target_user not in self.user_list.keys():
            raise UserNotInMeetingException

        self.user_list.pop(target_user)

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
