import datetime as dt

import settings
from classes.uploadable import Uploadable
from classes.utils import get_nearest_datetime, get_iso_day_int, get_day_abbr


class KSUClass(Uploadable):

    def __init__(self,
                 symbol: str,
                 full_name: str,
                 mode: str,
                 section: str,
                 days: list[str],
                 start_time: str,
                 end_time: str,
                 building: str,
                 room: str, unit: str,
                 floor: str,
                 ):
        self.symbol = symbol.strip()
        self.full_name = full_name.strip()
        self.type = mode.strip()
        self.section = section.strip()
        self.days = [int(day) for day in days]
        self.start_time = dt.datetime.strptime(start_time.strip(), '%I:%M %p').time()
        self.end_time = dt.datetime.strptime(end_time.strip(), '%I:%M %p').time()
        self.building = building.strip()
        if self.building == "":
            self.building = "NA"
        self.room = room.strip()
        if self.room == "":
            self.room = "NA"
        self.unit = unit.strip()
        self.floor = floor.strip()

        self.location = f"{self.building}/{self.room}"

    def __repr__(self) -> str:
        return f"{self.symbol}, {self.days}, {self.start_time} - {self.end_time}, {self.location}"

    @staticmethod
    def from_text(col, time_rows):
        temp = time_rows.split("@")
        days = temp[0].strip().split()
        symbol = col[1].get_text()
        full_name = col[3].get_text()
        mode = col[7].get_text()
        section = col[9].get_text()
        time = temp[1].replace("t", "").replace("ص", "AM").replace("م", "PM")
        start_time = time.split("-")[0].strip()
        end_time = time.split("-")[1].strip()
        unit = temp[2].replace("u", "")
        building = temp[3].replace("b", "")
        floor = temp[4].replace("f", "")
        room = temp[6].replace("r", "").strip() + temp[5].replace("w", "").strip()
        return KSUClass(symbol, full_name, mode, section, days, start_time, end_time, building, room, unit, floor)

    def to_json(self, color: int) -> dict:
        iso_weekdays = [get_iso_day_int(day) for day in self.days]
        nearest_date = get_nearest_datetime(iso_weekdays)
        start_date = dt.datetime.combine(nearest_date, self.start_time).isoformat()
        end_date = dt.datetime.combine(nearest_date, self.end_time).isoformat()
        until_date = settings.END_DATE.isoformat().replace('-', '').replace(':', '') + 'Z'
        by_day = ','.join([get_day_abbr(day) for day in self.days])
        event = {
            "summary": self.symbol,
            "location": self.location,
            "colorId": color,
            "start": {
                "dateTime": start_date,
                "timeZone": "Asia/Riyadh"
            },
            "end": {
                "dateTime": end_date,
                "timeZone": "Asia/Riyadh"
            },
            "recurrence": [
                f"RRULE:FREQ=WEEKLY"
                f";UNTIL={until_date}"
                f";BYDAY={by_day}"
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        return event
