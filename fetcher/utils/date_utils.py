import datetime


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
    now = datetime.datetime.now()
    while now.isoweekday() not in iso_weekdays:
        now += datetime.timedelta(days=1)
    return now
