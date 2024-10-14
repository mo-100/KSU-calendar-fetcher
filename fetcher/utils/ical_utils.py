import datetime

from icalendar import Timezone, TimezoneStandard, Alarm, Calendar

from fetcher.abstract_classes import CalendarEvent


def make_ksa_timezone() -> Timezone:
    timezone = Timezone()
    timezone.add('TZID', 'Asia/Riyadh')

    tzstandard = TimezoneStandard()
    tzstandard.add('DTSTART', datetime.datetime(1970, 1, 1, 0, 0, 0))
    tzstandard.add('TZOFFSETFROM', datetime.timedelta(hours=3))
    tzstandard.add('TZOFFSETTO', datetime.timedelta(hours=3))
    tzstandard.add('TZNAME', 'AST')

    timezone.add_component(tzstandard)
    return timezone


def make_alarm(diff: datetime.timedelta, msg: str) -> Alarm:
    alarm = Alarm()
    alarm.add('trigger', -diff)
    alarm.add('action', 'DISPLAY')
    alarm.add('description', msg)
    return alarm


def make_calendar_from_events(events: list[CalendarEvent], timezone: Timezone) -> Calendar:
    cal = Calendar()
    cal.add('prodid', '-KSU Calendar Fetcher-')
    cal.add('version', '2.0')
    cal.add_component(timezone)
    for event in events:
        cal.add_component(event.make_event())
    return cal
