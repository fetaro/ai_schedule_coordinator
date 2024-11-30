import datetime
from pathlib import Path

from event import Event

TZ_JST = datetime.timezone(datetime.timedelta(hours=9))
THIS_DIR = Path(__file__).parent.resolve()

_COLOR_CODE_MAP = {
    "1": "#A4BDFC",  # Lavender
    "2": "#7AE7BF",  # Sage
    "3": "#DBADFF",  # Grape
    "4": "#FF887C",  # Flamingo
    "5": "#FBD75B",  # Banana
    "6": "#FFB878",  # Tangerine
    "7": "#46D6DB",  # Peacock
    "8": "#E1E1E1",  # Graphite
    "9": "#5484ED",  # Blueberry
    "10": "#51B749",  # Basil
    "11": "#DC2127",  # Tomato
}


class EventParser:

    @staticmethod
    def parse(event_dict) -> Event:
        return Event(
            id=event_dict["id"],
            start=datetime.datetime.fromisoformat(event_dict['start'].get('dateTime', event_dict['start'].get('date'))),
            end=datetime.datetime.fromisoformat(event_dict['end'].get('dateTime', event_dict['start'].get('date'))),
            summary=event_dict['summary'],
            color_code=_COLOR_CODE_MAP[event_dict.get("colorId", "1")],
        )
