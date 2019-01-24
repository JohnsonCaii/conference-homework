# -*- coding: utf-8 -*-
import logging
from datetime import timedelta, datetime
from typing import List

from dataclasses import dataclass

from talk import (
    read_talks_from_file,
    Talk,
    get_total_talk_time,
    get_min_unscheduled_talk_time,
)
from track import (
    Track,
    SessionType,
)

logging.basicConfig(level=logging.INFO,
                    format='[%(name)s]:%(asctime)s:%(filename)s:%(lineno)d %(levelname)s/%(processName)s %(message)s')

logger = logging.getLogger(__name__)


@dataclass
class Conference:
    tracks: List[Track]


def main():
    conference: Conference = schedule_conference()

    for index, track in enumerate(conference.tracks):
        print(f'Track {index + 1}')

        for talk in track.talks:
            print(f'{talk.start_time} {talk.title} {talk.duration_time}')

        print()


def schedule_conference() -> Conference:
    from track import (
        get_track_count_by_total_talk_time,
        morning_session_duration_time,
        morning_session_start_time,
        afternoon_session_start_time,
        afternoon_session_duration_time,
    )
    talks: List[Talk] = read_talks_from_file()
    total_talk_time: int = get_total_talk_time(talks)
    track_count = get_track_count_by_total_talk_time(total_talk_time)

    conference = Conference(tracks=[])

    for i in range(track_count):
        track = arrange_track(morning_session_start_time=morning_session_start_time,
                              morning_session_duration_time=morning_session_duration_time,
                              talks=talks,
                              afternoon_session_duration_time=afternoon_session_duration_time,
                              afternoon_session_start_time=afternoon_session_start_time,
                              )
        conference.tracks.append(track)
    return conference


def arrange_track(*, morning_session_start_time: int,
                  morning_session_duration_time: int,
                  talks: List[Talk],
                  afternoon_session_start_time: int,
                  afternoon_session_duration_time: int) -> Track:
    track = Track(talks=[])
    arrange_talk_by_session_time(session_start_time=morning_session_start_time,
                                 session_duration_time=morning_session_duration_time,
                                 talks=talks,
                                 default_talk_between_gap=Talk(title='Lunch', start_time='12:00PM'),
                                 session_type=SessionType.morning,
                                 track=track)
    arrange_talk_by_session_time(session_start_time=afternoon_session_start_time,
                                 session_duration_time=afternoon_session_duration_time,
                                 talks=talks,
                                 default_talk_between_gap=Talk(title='Networking Event', start_time='05:00PM'),
                                 session_type=SessionType.afternoon,
                                 track=track)
    return track


def arrange_talk_by_session_time(*, session_start_time: int,
                                 session_duration_time: int,
                                 talks: List[Talk],
                                 default_talk_between_gap: Talk,
                                 session_type: SessionType,
                                 track: Track):
    next_talk_start_time = session_start_time
    for talk in talks:
        if session_duration_time - talk.cost_time >= 0 and talk.start_time is None:
            talk.start_time = transform_datetime_to_hour_minutes_format(next_talk_start_time)
            session_duration_time -= talk.cost_time
            track.talks.append(talk)
            next_talk_start_time = next_talk_start_time + timedelta(minutes=talk.cost_time)
        if session_duration_time == 0:  # no time remaining
            track.talks.append(default_talk_between_gap)
            break
        if session_type == SessionType.afternoon and get_min_unscheduled_talk_time(talks) == 0 \
                and session_duration_time <= 60:  # afternoon no talk remaining
            track.talks.append(default_talk_between_gap)
            break


def transform_datetime_to_hour_minutes_format(source_datetime: datetime) -> str:
    return source_datetime.strftime('%I:%M%p')


if __name__ == '__main__':
    main()
