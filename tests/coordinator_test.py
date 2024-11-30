import datetime

from coordinator import Coordinator
from event import Event
from event_parser import TZ_JST
from time_range import TimeRange


def test_calc():
    event_list = [
        Event(id='1',
              start=datetime.datetime(2024, 11, 25, 10, 0, tzinfo=TZ_JST),
              end=datetime.datetime(2024, 11, 25, 10, 30, tzinfo=TZ_JST),
              summary='s',
              color_code='#DC2127')
    ]
    result_time_range = [
        TimeRange(start="2024/11/25 10:00", end="2024/11/25 10:30"),
        TimeRange(start="2024/11/25 10:30", end="2024/11/25 11:00"),
        TimeRange(start="2024/11/25 11:00", end="2024/11/25 11:30"),
        TimeRange(start="2024/11/25 11:30", end="2024/11/25 12:00"),
    ]
    expected = [
        TimeRange(start="2024/11/25 10:30", end="2024/11/25 11:00"),
        TimeRange(start="2024/11/25 11:00", end="2024/11/25 11:30"),
        TimeRange(start="2024/11/25 11:30", end="2024/11/25 12:00"),
    ]
    actual = Coordinator.calc(result_time_range, event_list)
    assert actual == expected


def test_coordinate():
    user_prompt = '''
以下の時間の中で30分ほどご都合の良い時間はありませんでしょうか？
10月 28日 (月曜日)⋅10:00～14:00、15:00～16:00
10月 29日 (火曜日)⋅10:00～11:00
'''
    Coordinator.coordinate(user_prompt)
