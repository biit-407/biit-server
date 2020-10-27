from enum import Enum
from typing import Any, Dict
from fastcore.utils import store_attr
from datetime import datetime


class FeedbackType(Enum):
    BUG = 0
    SUGESTION = 1


class FeedbackStatus(Enum):
    NONE = 0
    NOT_RESOLVED = 1
    WILL_BE_RESOLVED = 2
    WILL_NOT_BE_RESOLVED = 3
    RESOLVED = 4


class Feedback:
    def __init__(
        self,
        id: str = "",
        email: str = "",
        timestamp: str = datetime.today().isoformat(),
        title: str = "",
        text: str = "",
        feedback_type: FeedbackType = FeedbackType.SUGESTION,
        feedback_status: FeedbackStatus = FeedbackStatus.NOT_RESOLVED,
        document_snapshot=None,
    ):
        if document_snapshot:
            self.id = document_snapshot.get("id")
            self.email = document_snapshot.get("email")
            self.timestamp = document_snapshot.get("timestamp")
            self.title = document_snapshot.get("title")
            self.text = document_snapshot.get("text")
            self.feedback_type = document_snapshot.get("feedback_type")
            self.feedback_status = document_snapshot.get("feedback_status")
        else:
            store_attr(
                "id,email,timestamp,title,text,feedback_type,feedback_status", cast=True
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "timestamp": self.timestamp,
            "title": self.title,
            "text": self.text,
            "feedback_type": int(self.feedback_type.value),
            "feedback_status": int(self.feedback_status.value),
        }
