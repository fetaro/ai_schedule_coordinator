import datetime
from typing import List

from pydantic import BaseModel

from google_calender_service import TZ_JST


class TimeRange(BaseModel):
    start: str
    end: str

    def start_dt(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.start, "%Y/%m/%d %H:%M").astimezone(TZ_JST)

    def end_dt(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.end, "%Y/%m/%d %H:%M").astimezone(TZ_JST)

    def __str__(self):
        # 曜日の計算
        week = ["月", "火", "水", "木", "金", "土", "日"]
        start_day_of_week = week[self.start_dt().weekday()]
        return (f'{self.start_dt().strftime("%m/%d")}({start_day_of_week}) {self.start_dt().strftime("%H:%M")}'
                f'〜'
                f'{self.end_dt().strftime("%H:%M")}')


class TimeRangeList(BaseModel):
    time_range_list: List[TimeRange]
