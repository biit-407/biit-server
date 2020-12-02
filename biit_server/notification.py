from enum import Enum
from typing import Any, Dict


class AssetType(Enum):
    NONE = 0
    UNRATED_MEETUP = 1
    RECONNECT = 2


class Notification:
    def __init__(
        self,
        id="",
        user_id="",
        timestamp=0,
        asset_id="",
        asset_type=AssetType.NONE,
        message="",
        dismissed=False,
        document_snapshot=None,
    ):
        if document_snapshot != None:
            document_dict = document_snapshot.to_dict()
            id = document_dict["id"]
            user_id = document_dict["user_id"]
            timestamp = document_dict["timestamp"]
            asset_id = document_dict["asset_id"]
            asset_type = document_dict["asset_type"]
            message = document_dict["message"]
            dismissed = document_dict["dismissed"]

        self.id = id
        self.user_id = user_id
        self.timestamp = timestamp
        self.asset_id = asset_id
        self.asset_type = asset_type if type(asset_type) == int else asset_type.value
        self.message = message
        self.dismissed = dismissed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "message": self.message,
            "dismissed": self.dismissed,
        }
