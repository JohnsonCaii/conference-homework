# -*- coding: utf-8 -*-

from track import (
    get_track_count_by_total_talk_time,
)

import logging

logger = logging.getLogger(__name__)


def test_get_track_count_by_total_talk_time():
    from talk import (
        get_total_talk_time,
        read_talks_from_file,
    )
    assert get_track_count_by_total_talk_time(get_total_talk_time(read_talks_from_file())) == 2

