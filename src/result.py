import dataclasses
from typing import List

from event import Event
from time_range import TimeRange


@dataclasses.dataclass
class Result:
    candidate_time_range_list: List[TimeRange]
    candidate_time_range_list_30min: List[TimeRange]
    event_list: List[Event]
    result_time_range_list: List[TimeRange]