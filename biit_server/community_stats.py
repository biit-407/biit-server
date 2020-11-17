from enum import Enum
from typing import Any, Dict, List


class CommunityStats:
    def __init__(
        self,
        user_list={},
        community=None,
        # this is defined as a meetup where at least
        # 2 of the participants accepted.
        accepted_meetups=None,
        total_meetups=None,
        total_sessions=None,
        document_snapshot=None,
    ):
        if document_snapshot != None:
            document_dict = document_snapshot.to_dict()
            community = document_dict["community"]
            accepted_meetups = document_dict["accepted_meetups"]
            total_meetups = document_dict["total_meetups"]
            total_sessions = document_dict["total_sessions"]

        self.user_list = user_list
        self.community = community
        self.accepted_meetups = accepted_meetups
        self.total_meetups = total_meetups
        self.total_sessions = total_sessions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "community": self.community,
            "accepted_meetups": self.accepted_meetups,
            "total_meetups": self.total_meetups,
            "total_sessions": self.total_sessions,
        }
