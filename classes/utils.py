import datetime as dt


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


def get_iso_day_str(weekday_str: str) -> int:
    iso_weekdays = {
        'الاحد': 7,  # sunday
        'الاثنين': 1,  # monday
        'الثلاثاء': 2,
        'الاربعاء': 3,
        'الخميس': 4,
        'الجمعة': 5,
        'السبت': 6,
    }
    return iso_weekdays[weekday_str]


def get_nearest_datetime(iso_weekdays: list[int]) -> dt.datetime:
    now = dt.datetime.now()
    while now.isoweekday() not in iso_weekdays:
        now += dt.timedelta(days=1)
    return now


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
