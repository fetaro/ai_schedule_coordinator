import datetime
from typing import List

from pydantic import BaseModel

from google_calender_service import TZ_JST


class TimeRange(BaseModel):
    start_str: str
    end_str: str

    def start_dt(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.start_str, "%Y/%m/%d %H:%M").astimezone(TZ_JST)

    def end_dt(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.end_str, "%Y/%m/%d %H:%M").astimezone(TZ_JST)

    def __str__(self):
        # 曜日の計算
        week = ["月", "火", "水", "木", "金", "土", "日"]
        start_day_of_week = week[self.start_dt().weekday()]
        return (f'{self.start_dt().strftime("%m/%d")}({start_day_of_week}) {self.start_dt().strftime("%H:%M")}'
                f'〜'
                f'{self.end_dt().strftime("%H:%M")}')

    def split_to_30min(self):
        start = self.start_dt()
        end = self.end_dt()
        time_range_list = []
        while start < end:
            time_range_list.append(TimeRange(start_str=start.strftime("%Y/%m/%d %H:%M"),
                                             end_str=(start + datetime.timedelta(minutes=30)).strftime("%Y/%m/%d %H:%M")))
            start += datetime.timedelta(minutes=30)
        return time_range_list

class TimeRangeList(BaseModel):
    time_range_list: List[TimeRange]
