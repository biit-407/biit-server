"""
this file is designed to house functions that query, and
modify the db. this should save some file space in other 
handler functions
"""

from biit_server.http_responses import http500
from biit_server.rating import Rating
from biit_server.meeting import Meeting
from biit_server.database import Database
from datetime import datetime


def get_past_meetups(email: str):
    """"""
    meeting_db = Database("meetings")

    meeting_db_response = meeting_db.collection_ref.get()

    meetings = [
        Meeting(document_snapshot=meeting_snapshot)
        for meeting_snapshot in meeting_db_response
    ]

    past_meetings = [
        meeting
        for meeting in meetings
        if email in meeting.user_list
        and meeting.user_list[email] == 1
        and datetime.utcfromtimestamp(meeting.timestamp) < datetime.now()
    ]

    return past_meetings


def get_past_meetup_ids(email: str):
    """"""
    return [meeting.id for meeting in get_past_meetups(email)]


def get_past_unrated_ratings(email: str):
    """
    Returns a list of ratings for meetups that have not
    been rated by the given user
    """
    past_meeting_ids = get_past_meetup_ids(email)

    rating_db = Database("ratings")

    rating_db_response = rating_db.collection_ref.get()

    ratings = [
        Rating(document_snapshot=rating_snapshot)
        for rating_snapshot in rating_db_response
    ]

    # Identifies the ratings the user is a part of
    # and checks if the user has reviewed it.
    ratings = [
        rating.to_dict()
        for rating in ratings
        if email in rating.rating_dict
        and rating.rating_dict[email] == -1
        and rating.meeting_id in past_meeting_ids
    ]

    return ratings


def get_past_unrated_meetups(email):
    """"""

    past_meetings = get_past_meetups(email)

    rating_db = Database("ratings")

    rating_db_response = rating_db.collection_ref.get()

    ratings = [
        Rating(document_snapshot=rating_snapshot)
        for rating_snapshot in rating_db_response
    ]

    meeting_ids = [
        rating.meeting_id
        for rating in ratings
        if email in rating.rating_dict and rating.rating_dict[email] == -1
    ]

    # Identifies the ratings the user is a part of
    # and checks if the user has reviewed it.
    meetings = [meeting for meeting in past_meetings if meeting.id in meeting_ids]

    return meetings
