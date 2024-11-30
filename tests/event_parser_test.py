import datetime

from event import Event
from event_parser import EventParser


def test_parse():
    event_dict = {'kind': 'calendar#event',
                  'etag': '"xxxxxxxx"',
                  'id': 'xxxxxxxxxxxxxxx',
                  'status': 'confirmed',
                  'htmlLink': 'https://www.google.com/calendar/event?eid=xxxxxxx&ctz=Asia/Tokyo',
                  'created': '2024-11-14T01:33:36.000Z',
                  'updated': '2024-11-22T00:06:17.426Z',
                  'summary': 'MTG',
                  'description': 'お世話になります。MTGとなります。',
                  'location': '会議室',
                  'colorId': '11',
                  'creator': {'email': 'fetaro@gmail.com', 'self': True},
                  'organizer': {'email': 'fetaro@gmail.com'},
                  'start': {'dateTime': '2024-11-25T11:00:00+09:00', 'timeZone': 'Asia/Dili'},
                  'end': {'dateTime': '2024-11-25T12:00:00+09:00', 'timeZone': 'Asia/Dili'},
                  'iCalUID': '0402C',
                  'sequence': 0,
                  'attendees': [{'email': 'fetaro@gmail.com', 'self': True, 'responseStatus': 'accepted'},
                                {'email': 'hoge@hoge', 'responseStatus': 'needsAction'}],
                  'guestsCanInviteOthers': False,
                  'privateCopy': True,
                  'reminders': {'useDefault': True},
                  'eventType': 'default'}
    e: Event = EventParser.parse(event_dict)
    assert e.id == "xxxxxxxxxxxxxxx"
    assert e.summary == "MTG"
    assert e.start == datetime.datetime(2024, 11, 25, 11, 0, 0,
                                        tzinfo=datetime.timezone(datetime.timedelta(seconds=32400), 'Asia/Dili'))
    assert e.end == datetime.datetime(2024, 11, 25, 12, 0, 0,
                                      tzinfo=datetime.timezone(datetime.timedelta(seconds=32400), 'Asia/Dili'))
    assert e.color_code == {"name": "Tomato", "rgb": "#DC2127"}
