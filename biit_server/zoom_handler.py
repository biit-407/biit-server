import json
import os
import time
from typing import List

import requests

from .utils import send_discord_message

url = "https://api.zoom.us/v2/users/ryanjchen2@gmail.com/meetings"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f'Bearer {os.getenv("ZOOM_TOKEN")}',
}


def create_meeting(timestamp: str, duration: int, participants: List[str]):
    """Helper function to create a meeting.

    Params:
        timestamp (str): The timestamp for when the meeting should start
        duration (int): How long the meeting should last for
        participants (List[str]): The list of the users that are a part of the meeting

    Returns:
        The URL to start and join the meeting.
    """
    meeting_start_time = time.strftime("%m/%d/%YT%H:%M:%S", time.gmtime(int(timestamp)))

    request_data = {
        "topic": f"Biit meeting with " + ", ".join(participants),
        "type": 2,
        "start_time": meeting_start_time,
        "duration": duration,
        "timezone": "America/Indianapolis",
    }

    print(request_data)

    r = requests.post(url, headers=HEADERS, data=json.dumps(request_data))

    try:
        r.raise_for_status()
    except Exception as err:
        send_discord_message(err)
        return False

    response = r.json()

    return {"start_url": response.get("start_url"), "zoom_id": response.get("id")}


def reschedule_meeting(zoom_id: str, timestamp: str = None, duration: int = None):
    """Helper function to reschedule a meeting.

    Params:
        meeting_id (str): The meeting that will be changed
        timestamp (str): The timestamp for when the meeting should start
        duration (int): How long the meeting should last for
        participants (List[str]): The list of the users that are a part of the meeting

    Returns:
        Boolean True if the program succeeded.
    """

    request_data = {}

    if timestamp != None:
        new_meeting_time = time.strftime(
            "%m/%d/%YT%H:%M:%S", time.gmtime(int(timestamp))
        )
        request_data["start_time"] = new_meeting_time

    if duration != None:
        request_data["duration"] = duration

    r = requests.patch(
        f"https://api.zoom.us/v2/meetings/{zoom_id}",
        headers=HEADERS,
        data=json.dumps(request_data),
    )

    r.raise_for_status()

    return True


if __name__ == "__main__":
    res = create_meeting("1608845255000", 30, ["ryan"])
    print(res)
    print(
        reschedule_meeting(res.get("zoom_id"), timestamp="16088452551234", duration=60)
    )
