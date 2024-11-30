import json
from typing import List

from event import Event
from google_calender_service import GoogleCalenderService
from gpt_service import GptService
from time_range import TimeRangeList, TimeRange


class Coordinator:

    @staticmethod
    def _intersect(time_range: TimeRange, event: Event) -> bool:
        return time_range.end_dt() > event.start and event.end > time_range.start_dt()

    @staticmethod
    def calc(candidate_time_range_list: List[TimeRange], event_list: List[Event]) -> List[TimeRange]:
        result_time_range_list = []
        for time_range in candidate_time_range_list:
            # 全てのイベントと重複していないかどうかを確認
            for event in event_list:
                if Coordinator._intersect(time_range, event):
                    break
            else:
                result_time_range_list.append(time_range)
        return result_time_range_list

    @staticmethod
    def coordinate(user_prompt: str):
        gpt = GptService()
        system_prompt = '''
次に示す会話の中に登場する、会議の時間候補を、30分ごとに区切って出力してください。

会話の中で、年が省略されている場合は、2024年としてください。

以下のJSON形式で出力してください。出力に「```json」や「```」といった文字は不要です。

{
  "time_range_list":[
    {"start":"YYYY/MM/DD HH:MM","end":"YYYY/MM/DD HH:MM"},
    {"start":"YYYY/MM/DD HH:MM","end":"YYYY/MM/DD HH:MM"},
  ]
}

time_range_listは、相手が提案した日程候補の中で、私が空いている時間のリストです。
startは開始時間、endは終了時間です。
'''
        gpt_out_json = gpt.call_api(system_prompt=system_prompt, user_prompt=user_prompt, output_schema=TimeRangeList)

        candidate_time_range_list = TimeRangeList(**json.loads(gpt_out_json)).time_range_list

        # 開始時間ソートする
        candidate_time_range_list.sort(key=lambda x: x.start_dt())

        event_list = GoogleCalenderService.get_my_schedule(start=candidate_time_range_list[0].start_dt(),
                                                           end=candidate_time_range_list[-1].end_dt())
        result_time_range_list = Coordinator.calc(candidate_time_range_list, event_list)

        return event_list, result_time_range_list
