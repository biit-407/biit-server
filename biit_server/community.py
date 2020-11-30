from typing import Any, Dict, List

from .utils import send_discord_message, utcToInt


class community:
    def __init__(
        self,
        Admins=[],
        name="",
        bans=[],
        Members=None,
        codeofconduct="",
        meettype=None,
        mpm=None,
        document_snapshot=None,
    ):
        if document_snapshot != None:
            document_dict = document_snapshot.to_dict()
            Admins = document_dict["Admins"]
            Members = document_dict["Members"]
            bans = document_dict["bans"]
            codeofconduct = document_dict["codeofconduct"]
            meettype = document_dict["meettype"]
            mpm = document_dict["mpm"]
            name = document_dict["name"]
            return

        if Admins == None or name == None or bans == None or codeofconduct == None:
            send_discord_message(
                f"Slightly concerning: Admins, name, bans and/or codeofconduct in community {name} is set to None."
            )

        self.Admins = Admins
        self.Members = Members
        self.bans = bans
        self.codeofconduct = codeofconduct
        self.meettype = meettype
        self.mpm = mpm
        self.name = name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "Admins": self.Admins,
            "Members": self.Members,
            "CodeofConduct": self.codeofconduct,
            "mpm": self.mpm,
            "meettype": self.meettype,
        }
