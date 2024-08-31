import datetime

import pytz
import selenium
from icalendar import Timezone, TimezoneStandard, Calendar, Event, vText, Alarm
from selenium.webdriver import Chrome, Firefox, Edge

from fetcher.constants import LAST_STUDY_DAY
from fetcher.ksu_class import KSUClass
from fetcher.ksu_final import KSUFinal


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


def make_alarm(diff: datetime.timedelta, msg: str) -> Alarm:
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alarm.add('description', msg)
    alarm.add('trigger', -diff)
    return alarm


def make_event(c: KSUClass, color: int) -> Event:
    timezone = pytz.timezone('Asia/Riyadh')
    nearest_date = get_nearest_datetime(c.days)

    start_date = datetime.datetime.combine(nearest_date, c.start_time)
    end_date = datetime.datetime.combine(nearest_date, c.end_time)

    start_date = timezone.localize(start_date)
    end_date = timezone.localize(end_date)

    by_day = [get_day_abbr(day) for day in c.days]

    event = Event()

    event.add('summary', c.symbol)
    event.add('location', vText(c.location))
    event.add('dtstart', start_date)
    event.add('dtend', end_date)
    event.add('rrule', {
        'FREQ': 'WEEKLY',
        'UNTIL': LAST_STUDY_DAY,
        'BYDAY': by_day,
    })
    event.add('uid', f'{c.symbol}-{c.type_}-{c.start_time}-{c.days}')
    event.add('colorId', color)
    event.add('dtstamp', datetime.datetime.now(pytz.utc))
    event.add_component(
        make_alarm(
            datetime.timedelta(minutes=10),
            msg=f'Reminder: class in {10} minutes'
        )
    )
    return event


def make_event_final(f: KSUFinal, color: int) -> Event:
    timezone = pytz.timezone('Asia/Riyadh')

    start_date = f.datetime
    end_date = f.datetime + datetime.timedelta(hours=2)

    start_date = timezone.localize(start_date)
    end_date = timezone.localize(end_date)

    event = Event()

    event.add('summary', f'{f.symbol} final')
    event.add('dtstart', start_date)
    event.add('dtend', end_date)
    event.add('uid', f'{f.symbol}-final')
    event.add('colorId', color)
    event.add('dtstamp', datetime.datetime.now(pytz.utc))
    event.add_component(
        make_alarm(
            datetime.timedelta(hours=24),
            msg=f'Reminder: final in {24} hours',
        )
    )
    return event


def make_timezone() -> Timezone:
    timezone = Timezone()
    timezone.add('TZID', 'Asia/Riyadh')

    tzstandard = TimezoneStandard()
    tzstandard.add('DTSTART', datetime.datetime(1970, 1, 1, 0, 0, 0))
    tzstandard.add('TZOFFSETFROM', datetime.timedelta(hours=3))
    tzstandard.add('TZOFFSETTO', datetime.timedelta(hours=3))
    tzstandard.add('TZNAME', 'AST')

    timezone.add_component(tzstandard)
    return timezone


def make_calendar() -> Calendar:
    cal = Calendar()
    cal.add('prodid', '-KSU Calendar Fetcher-')
    cal.add('version', '2.0')
    cal.add_component(make_timezone())
    return cal


def get_driver() -> selenium.webdriver:
    driver = input('Enter your browser [chrome, firefox, edge]: ')
    match driver:
        case 'chrome':
            return Chrome()
        case 'firefox':
            return Firefox()
        case 'edge':
            return Edge()
        case _:
            raise Exception('Invalid input')
