import asyncio
import logging
import os
from datetime import datetime
from typing import List
import requests


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


def utcToInt(availability: List[List[str]]) -> List[List[int]]:
    """Converts POSIX time into int time

    Args:
        availability (List[List[str]]): List of POSIX times

    Returns:
        List[List[int]]: List of Int times
    """
    intTimes = []
    for s0, s1 in availability:
        s0datetime = datetime.utcfromtimestamp(s0)
        s1datetime = datetime.utcfromtimestamp(s1)
        s0time = s0datetime.hour + s0datetime.weekday() * 24
        s1time = s1datetime.hour + s1datetime.weekday() * 24
        intTimes += (s0time, s1time)
    return intTimes


def send_discord_message(message:str):
    """
    Sends a message to the discord 

    Args:
        message (str): the text to send to the discord channel
    """
    __WEBHOOK = os.getenv('DISCORD_BOT', 'awwgeezenotgonnaworkiguess')
    logging.critical(__WEBHOOK)
    if __WEBHOOK == 'awwgeezenotgonnaworkiguess':
        raise Exception('Failed to send discord message')
    requests.post(__WEBHOOK, json={'content': message})
