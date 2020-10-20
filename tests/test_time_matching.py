from biit_server.time_matcher import find_meeting_time


def test_match_2_possible():
    """
    Tests that matching 2 participants with possible meeting time
    """

    person_1 = [(9, 17)]
    person_2 = [(9, 17)]

    assert (9, 17) == find_meeting_time(person_1, person_2)


def test_match_2_not_possible():
    """
    Tests that matching 2 participants with no potential meeting times
    """

    person_1 = [(9, 12)]
    person_2 = [(13, 17)]

    assert None == find_meeting_time(person_1, person_2)


def test_match_3_possible():
    """
    Tests that matching 3 participants with potential meeting times
    """

    person_1 = [(9, 15)]
    person_2 = [(13, 17)]
    person_3 = [(12, 14)]

    assert (13, 14) == find_meeting_time(person_1, person_2, person_3)


def test_match_3_not_possible():
    """
    Tests that matching 3 participants with no potential meeting times
    """

    person_1 = [(9, 15)]
    person_2 = [(13, 17)]
    person_3 = [(11, 12)]

    assert None == find_meeting_time(person_1, person_2, person_3)


def test_match_no_zero_length_meeting():
    """
    Tests that matching will not generate a meeting time of 0 length
    """

    person_1 = [(13, 17)]
    person_2 = [(12, 13)]

    assert None == find_meeting_time(person_1, person_2)


def test_match_2_with_multiple_times():
    """
    Tests that matching people with multiple times
    works correctly
    """

    person_1 = [(9, 10), (11, 14)]
    person_2 = [(11, 15), (16, 17)]

    assert (11, 14) == find_meeting_time(person_1, person_2)


def test_match_3_with_multiple_times():
    """
    Tests that matching people with multiple times
    works correctly, also asserts that the first
    potential meeting time is selected
    """

    person_1 = [(9, 10), (11, 14)]
    person_2 = [(11, 15), (16, 17)]
    person_3 = [(12, 13), (13, 15)]

    assert (12, 13) == find_meeting_time(person_1, person_2, person_3)


def test_match_2_with_meeting_length():
    """
    Tests that matching with a given meeting length will
    shrink the meeting time to exact length specified
    """

    meeting_length = 2
    person_1 = [(9, 10), (11, 14)]
    person_2 = [(11, 15), (16, 17)]

    assert (11, 13) == find_meeting_time(
        person_1, person_2, meeting_length=meeting_length
    )


def test_match_2_with_meeting_length_not_possible():
    """
    Tests that matching with a given meeting length will
    return None if the time frame is not possible
    """

    meeting_length = 4
    person_1 = [(9, 10), (11, 14)]
    person_2 = [(11, 15), (16, 17)]

    assert None == find_meeting_time(person_1, person_2, meeting_length=meeting_length)


def test_match_2_different_days():
    """
    Tests that matching still works across different days
    """

    person_1 = [(9, 12), (33, 37)]
    person_2 = [(13, 14), (34, 35)]

    assert (34, 35) == find_meeting_time(person_1, person_2)
