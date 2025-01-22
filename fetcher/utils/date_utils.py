import datetime
from fetcher.utils.config import FIRST_STUDY_DAY

def get_iso_day_int(weekday_num: int) -> int:
    iso_weekdays = {
        1: 7,  # sunday
        2: 1,  # monday
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
    }
    return iso_weekdays[weekday_num]


def get_day_abbr(day: int) -> str:
    days_abbr = {
        1: "SU",
        2: "MO",
        3: "TU",
        4: "WE",
        5: "TH",
        6: "FR",
        7: "SA"
    }
    return days_abbr[day]


def get_nearest_datetime(days: list[int]) -> datetime.datetime:
    iso_weekdays = [get_iso_day_int(day) for day in days]
    start_date = FIRST_STUDY_DAY
    while start_date.isoweekday() not in iso_weekdays:
        start_date += datetime.timedelta(days=1)
    return start_date
