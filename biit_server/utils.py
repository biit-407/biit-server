from datetime import date
import os
import json
from datetime import datetime
import calendar
from typing import List, Tuple


def mock_dev(return_value):
    """
    Decorator for mocking the return value of a function when
    in a dev environment

    Args:
        return_value (any): the value to have the function return
            when run from inside a dev environment
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            stage = os.getenv("STAGE", "dev")
            if stage == "dev":
                return return_value

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def utcToInt(availability):
    intTimes = []
    for s0, s1 in availability:
        s0datetime = datetime.fromtimestamp(s0)
        s1datetime = datetime.fromtimestamp(s1)
        s0time = s0datetime.hour + s0datetime.weekday() * 24
        s1time = s1datetime.hour + s1datetime.weekday() * 24
        intTimes += (s0time, s1time)
    return intTimes
