import logging

import pytest

from talk import (
    read_talks_from_file,
    get_total_talk_time,
    get_min_unscheduled_talk_time,
    build_talk_object,
    Talk,
    no_numbers_in_talk_title,
    is_allow_talk_length_suffix,
)

logger = logging.getLogger(__name__)

talks = read_talks_from_file()


def test_build_talk_object():
    talk: Talk = build_talk_object("Writing Fast Tests Against Enterprise Rails 60min")
    assert talk
    assert talk.title == 'Writing Fast Tests Against Enterprise Rails'
    assert talk.duration_time == '60min'
    assert talk.cost_time == 60


def test_get_total_talk_time():
    assert get_total_talk_time(talks) == 785


def test_get_min_talk_time():
    assert get_min_unscheduled_talk_time(talks) == 5


def test_read_talks_from_file():
    assert talks
    assert type(talks) == list
    assert len(talks) == 19


@pytest.mark.parametrize('input_param, expected', [
    ('User Interface CSS in Rails Apps', True),
    ('1 Java Concurrency Programming Best Practice', False),
    ('___User Interface CSS in Rails Apps', True),
    ('Common Ruby Errors 22', False),
    ('Writing Fast Tests 666 Against Enterprise Rails', False)
])
def test_no_numbers_in_talk_title(input_param, expected):
    assert no_numbers_in_talk_title(input_param) == expected


@pytest.mark.parametrize('input_param, expected', [
    ('60min', True),
    ('lightning', True),
    ('60sec', False),
    ('5 lightning', False),
])
def test_is_talk_length_with_correct_suffix(input_param, expected):
    assert is_allow_talk_length_suffix(input_param) == expected
