from typing import Any, Dict


class Account:
    def __init__(
        self,
        email=None,
        fname=None,
        lname=None,
        age=20,
        agePref="",
        birthday="",
        covid=None,
        meetLength=None,
        meetType=None,
        optIn=None,
        schedule=None,
        meetGroup=None,
        document_snapshot=None,
    ):
        if document_snapshot != None:
            data = document_snapshot.to_dict()
            self.email = data.get("email")
            self.fname = data.get("fname")
            self.lname = data.get("lname")
            self.age = data.get("age")
            self.agePref = data.get("agePref")
            self.birthday = data.get("birthday")
            self.covid = data.get("covid")
            self.meetLength = data.get("meetLength")
            self.meetType = data.get("meetType")
            self.optIn = data.get("optIn", 0)
            self.schedule = data.get("schedule")
            self.meetGroup = data.get("meetGroup")
            return

        self.email = email
        self.fname = fname
        self.lname = lname
        self.age = age
        self.agePref = agePref
        self.birthday = birthday
        self.covid = covid
        self.meetLength = meetLength
        self.meetType = meetType
        self.optIn = optIn
        self.schedule = schedule
        self.meetGroup = meetGroup

    def set_property(self, property, value):
        value = self.__dict__.get("property")

        if value != None:
            self.__dict__[property] = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "fname": self.fname,
            "lname": self.lname,
            "age": self.age,
            "agePref": self.agePref,
            "birthday": self.birthday,
            "covid": self.covid,
            "meetLength": self.meetLength,
            "meetType": self.meetType,
            "optIn": self.optIn,
            "schedule": self.schedule,
            "meetGroup": self.meetGroup,
        }
