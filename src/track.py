from datetime import datetime
from typing import List

from dataclasses import dataclass

from talk import Talk
from enum import (
    Enum,
    auto,
)

morning_session_duration_time = 180
morning_session_start_time = datetime.now().replace(hour=9, minute=0, second=0)
morning_session_end_time = datetime.now().replace(hour=12, minute=0, second=0)

afternoon_session_duration_time = 240
afternoon_session_start_time = datetime.now().replace(hour=13, minute=0, second=0)
afternoon_session_end_time = datetime.now().replace(hour=17, minute=0, second=0)


@dataclass
class Track:
    talks: List[Talk]


def get_track_count_by_total_talk_time(total_talk_time: int) -> int:
    return round(total_talk_time / get_track_duration_time())


def get_track_duration_time() -> int:
    return morning_session_duration_time + afternoon_session_duration_time


class SessionType(Enum):
    morning = auto()
    afternoon = auto()
