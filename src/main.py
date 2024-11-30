import streamlit as st

from coordinator import Coordinator

st.title("AI日程調整")
user_prompt = st.text_area("日程調整の依頼文を入力してください", height=150)

if st.button("調整"):
    event_list, result_time_range = Coordinator.coordinate(user_prompt)
    st.subheader("空いている時間")
    for time_range in result_time_range:
        st.write(str(time_range))
    st.subheader("付近の予定")
    for event in event_list:
        st.markdown(f'<font color={event.color_code}>{event}</font>', unsafe_allow_html=True)
