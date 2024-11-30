import dataclasses
import datetime


@dataclasses.dataclass
class Event:
    """
    Googleカレンダーのイベント
    """
    id: str
    start: datetime.datetime
    end: datetime.datetime
    summary: str
    color_code: str

    def __str__(self):
        week = ["月", "火", "水", "木", "金", "土", "日"]
        start_day_of_week = week[self.start.weekday()]
        start = self.start.strftime("%m/%d") + "(" + start_day_of_week + ")" + self.start.strftime("%H:%M")
        end = self.end.strftime("%H:%M")
        return f"{start}〜{end} {self.summary}"
