# -*- coding: utf-8 -*-
import logging
from typing import List

from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Talk:
    title: str
    duration_time: str = ''
    cost_time: int = 0
    start_time: str = None


def read_talks_from_file() -> List[Talk]:
    with open('../input_data', 'r') as f:
        file_content = f.readlines()

    talks: List[Talk] = [build_talk_object(talk_name) for talk_name in file_content]
    return sorted(talks, key=lambda talk: talk.cost_time, reverse=True)
    # return [build_talk_object(talk_name) for talk_name in file_content]


def no_numbers_in_talk_title(talk_title: str) -> bool:
    return not any(each_str.isdigit() for each_str in talk_title)


def is_allow_talk_length_suffix(talk_length: str) -> bool:
    return talk_length.endswith('min') or talk_length == 'lightning'


def build_talk_object(talk_name: str) -> Talk:
    split_talk_name: List[str] = talk_name.strip().split(' ')
    duration_time = split_talk_name[-1]
    if not is_allow_talk_length_suffix(duration_time):
        raise RuntimeError('unknown duration_time')

    if duration_time.endswith('min'):
        cost_time = int(duration_time[0:-3])
    elif duration_time == 'lightning':
        cost_time = 5
    else:
        raise RuntimeError('unknown duration_time')

    title = ' '.join(split_talk_name[0:-1])
    if not no_numbers_in_talk_title(title):
        raise RuntimeError('invalid talk title')

    return Talk(title=title, duration_time=duration_time, cost_time=cost_time)


def get_total_talk_time(talks: List[Talk]) -> int:
    return sum([talk.cost_time for talk in talks])


def get_min_unscheduled_talk_time(talks: List[Talk]) -> int:
    unscheduled_talk_arr = [talk.cost_time for talk in talks if talk.start_time is None]
    if unscheduled_talk_arr:
        return min(unscheduled_talk_arr)
    else:
        return 0
