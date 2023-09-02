# import pytest
import datetime as dt


# from reasonstudios_report_two import get_first_day_of_next_month
# from reasonstudios_report_two import find_last_day_of_last_month
# from reasonstudios_report_two import find_first_day_of_last_month
from reasonstudios_report_two import get_timewarrior_data


def test_get_data():
    data = get_timewarrior_data(
        ["§reasonstudios"], dt.date(2023, 8, 1), dt.date(2023, 9, 10)
    )
    print(data)


# def test_first_day_of_next_month():
#     today = dt.date(2000, 1, 1)
#     day = find_first_day_of_next_month(today)
#     assert day == dt.date(2000, 2, 1)


# from reasonstudios_report_two import get_last_day_of_month
# def test_last_day_of_last_month():
#     today = dt.date(2000, 1, 10)
#     day = find_last_day_of_last_month(today)
#     assert day == dt.date(1999, 12, 31)


# def test_first_day_of_last_month():
#     today = dt.date(2000, 1, 10)
#     day = find_first_day_of_last_month(today)
#     assert day == dt.date(1999, 12, 1)
