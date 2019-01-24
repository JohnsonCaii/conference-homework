# -*- coding: utf-8 -*-
import logging

from conference import (
    transform_datetime_to_hour_minutes_format,
    schedule_conference,
)

logger = logging.getLogger(__name__)


def test_transform_datetime_to_hour_minutes_format():
    from datetime import datetime
    time = transform_datetime_to_hour_minutes_format(datetime.now().replace(hour=9, minute=10))
    assert isinstance(time, str)
    assert time == '09:10AM'


def test_schedule_conference():
    from track import get_track_count_by_total_talk_time
    from talk import (
        read_talks_from_file,
        get_total_talk_time,
    )
    conference = schedule_conference()
    talks = read_talks_from_file()
    track_count: int = get_track_count_by_total_talk_time(get_total_talk_time(talks))
    assert conference
    assert len(conference.tracks) == track_count

    len_talks = 0
    for track in conference.tracks:
        assert track.talks
        len_talks += len(track.talks)
    assert len_talks == len(talks) + track_count * 2
