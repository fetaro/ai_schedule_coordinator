import datetime
from typing import List

from event import Event
from google_calender_service import GoogleCalenderService


def test_get_credentials():
    creds = GoogleCalenderService.get_credentials()
    assert creds.valid


def test_event_list():
    start = datetime.datetime.now() - datetime.timedelta(days=5)
    end = datetime.datetime.now() + datetime.timedelta(days=10)
    event_list: List[Event] = GoogleCalenderService.get_my_schedule(start, end)
    assert len(event_list) > 0
