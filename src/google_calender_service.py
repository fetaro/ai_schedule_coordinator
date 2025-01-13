import datetime
import os.path
import pickle
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from conf import Config
from event import Event
from event_parser import EventParser

TZ_JST = datetime.timezone(datetime.timedelta(hours=9))


class GoogleCalenderService:

    @staticmethod
    def get_credentials() -> Credentials:
        """
        secret/credentails.jsonをもとにGoogleカレンダーAPIのトークンを取得する。
        トークンがない場合はブラウザによるOauth2認証を行う。
        取得したトークンは保存しておき、有効な限りそれを使う。
        このコードは https://developers.google.com/calendar/quickstart/python 参照にして作成した
        """
        creds = None
        if os.path.exists(Config.TOKEN_PATH):
            with open(Config.TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # ブラウザを用いて認証しトークンを取得
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.CREDENTIAL_APTH, ['https://www.googleapis.com/auth/calendar.readonly'])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(Config.TOKEN_PATH, "wb") as token:
                pickle.dump(creds, token)
                os.chmod(Config.TOKEN_PATH, 0o755)
                print(f"make {Config.TOKEN_PATH}")
        return creds

    @staticmethod
    def call_calender_api(creds: Credentials, start: datetime, end: datetime):
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
        if start.tzinfo is None:
            start = start.astimezone(TZ_JST)
        if end.tzinfo is None:
            end = end.astimezone(TZ_JST)
        time_min = start.isoformat()
        time_max = end.isoformat()
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,  # 'Z' indicates UTC time,
            timeMax=time_max,
            maxResults=Config.API_MAX_RESULT,
            singleEvents=True,
            orderBy='startTime',
            timeZone="Asia/Tokyo",
        ).execute()
        return events_result

    @staticmethod
    def get_my_schedule(start: datetime, end: datetime) -> List[Event]:
        event_list: List[Event] = []
        credentials: Credentials = GoogleCalenderService.get_credentials()
        results = GoogleCalenderService.call_calender_api(credentials, start, end)
        event_dict_list = results.get('items', [])
        if not event_dict_list:
            print('No upcoming events found.')
        for event_dict in event_dict_list:
            if 'summary' in event_dict and event_dict['summary'] != "Home":
                event_list.append(EventParser.parse(event_dict))
        return event_list
