import datetime

import streamlit as st

from coordinator import Coordinator
from result import Result

st.title("AI日程調整")
user_prompt = st.text_area("日程調整の依頼文を入力してください", height=150)

if st.button("調整"):
    r: Result = Coordinator.coordinate(user_prompt)


    st.subheader("空いている時間")
    for time_range in r.result_time_range_list:
        st.write(str(time_range))

    st.subheader("付近の予定")
    for time_range in r.result_time_range_list:
        st.write("■" + str(time_range) + "の前後２時間の予定")
        for event in r.event_list:
            # time_range.start_dt() の前後２時間以内にあるイベントがあるかどうか
            if event.start - datetime.timedelta(hours=2) < time_range.end_dt() and event.end + datetime.timedelta(hours=2) > time_range.start_dt():
                st.markdown(f'<font color={event.color_code}>{event}</font>', unsafe_allow_html=True)

    if st.button("デバッグ情報"):
        st.subheader("相手からきた候補日")
        for time_range in r.candidate_time_range_list:
            st.write(str(time_range))

        st.subheader("30分ごとに分解した候補日")
        for time_range in r.candidate_time_range_list_30min:
            st.write(str(time_range))