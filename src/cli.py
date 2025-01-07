import datetime

from main import user_prompt

from coordinator import Coordinator

if __name__ == "__main__":

    user_prompt = """
    ・1/8（水）14:00-15:00
    ・1/9（木）11:00-12:00
    ・1/15（水）11:00-15:00
    """

    r = Coordinator.coordinate(user_prompt)


    print("相手からきた候補日")
    for time_range in r.candidate_time_range_list:
        print(str(time_range))

    print("30分ごとに分解した候補日")
    for time_range in r.candidate_time_range_list_30min:
        print(str(time_range))

    print("空いている時間")
    for time_range in r.result_time_range_list:
        print(str(time_range))

    print("付近の予定")
    for time_range in r.result_time_range_list:
        print(str(time_range) + "の付近")
        for event in r.event_list:
            # time_range.start_dt() の前後２時間以内にあるイベントがあるかどうか
            if event.start_str - datetime.timedelta(hours=2) < time_range.end_dt() and event.end_str + datetime.timedelta(hours=2) > time_range.start_dt():
                print(f'<font color={event.color_code}>{event}</font>', unsafe_allow_html=True)
