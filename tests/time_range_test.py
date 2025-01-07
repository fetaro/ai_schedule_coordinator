from time_range import TimeRange

def test_constant():
    a = TimeRange(start_str="2025/01/08 14:00", end_str="2025/01/08 15:00")
    assert a.start_str == "2025/01/08 14:00"
    assert a.end_str == "2025/01/08 15:00"
    assert a.start_dt().strftime("%Y/%m/%d %H:%M") == "2025/01/08 14:00"
    assert a.end_dt().strftime("%Y/%m/%d %H:%M") == "2025/01/08 15:00"

def test_split_to_30_min():
    actual = TimeRange(start_str="2025/01/08 14:00", end_str="2025/01/08 15:00").split_to_30min()
    expected = [TimeRange(start_str="2025/01/08 14:00", end_str="2025/01/08 14:30"),
                TimeRange(start_str="2025/01/08 14:30", end_str="2025/01/08 15:00")]
    assert actual == expected

    actual = TimeRange(start_str="2025/01/08 14:00", end_str="2025/01/08 15:30").split_to_30min()
    expected = [TimeRange(start_str="2025/01/08 14:00", end_str="2025/01/08 14:30"),
                TimeRange(start_str="2025/01/08 14:30", end_str="2025/01/08 15:00"),
                TimeRange(start_str="2025/01/08 15:00", end_str="2025/01/08 15:30")]
    assert actual == expected