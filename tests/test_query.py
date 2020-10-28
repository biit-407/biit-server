from biit_server.utils import utcToInt
import time
import pytest
from biit_server.query_helper import validate_update_field


def test_valid_fields():
    valid = {"updateFields": '{"test": "test", "Good": "Good"}'}
    testfields = ["test", "Good"]
    assert validate_update_field(valid, testfields)


def test_invalid_fields():
    valid = {"updateFields": '{"test": "test", "Good": "Good"}'}
    testfields = ["test", "Bad"]
    assert (
        validate_update_field(valid, testfields)[0]
        == "Bad Request: Not a valid update field: Good"
    )


def test_empty_updatefields():
    valid = {"updateFields": ""}
    testfields = ["test", "Bad"]
    assert (
        validate_update_field(valid, testfields)[0] == "Bad Request: Update Field empty"
    )


def test_empty_fields():
    valid = {"updateFields": '{"test": "test", "Good": "Good"}'}
    testfields = []
    assert (
        validate_update_field(valid, testfields)[0]
        == "Bad Request: Fields not being set"
    )


def test_schedule():
    temptime = 1603300716
    valid = [(temptime, temptime)]
    assert utcToInt(valid) == [65, 65]
