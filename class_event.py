import datetime as dt


class KSUClass:
    symbol: str
    full_name: str
    mode: str
    section: str
    days: list[int]
    start_time: dt.time
    end_time: dt.time
    building: str
    room: str
    unit: str
    floor: str

    def __init__(self, symbol: str, full_name: str, mode: str, section: str, days: list[str], start_time: str,
                 end_time: str,
                 building: str,
                 room: str, unit: str, floor: str):
        self.symbol = symbol.strip()
        self.full_name = full_name.strip()
        self.type = mode.strip()
        self.section = section.strip()
        self.days = [int(day) for day in days]
        self.start_time = dt.datetime.strptime(start_time.strip(), '%I:%M %p').time()
        self.end_time = dt.datetime.strptime(end_time.strip(), '%I:%M %p').time()
        self.building = building.strip()
        self.room = room.strip()
        self.unit = unit.strip()
        self.floor = floor.strip()

    def _get_days(self) -> list[str]:
        return [["", "SU", "MO", "TU", "WE", "TH", "FR", "SA"][day] for day in self.days]

    def _get_nearest_datetime(self) -> dt.datetime:
        iso_weekdays = [[0, 7, 1, 2, 3, 4, 5, 6][day] for day in self.days]
        now = dt.datetime.now()
        while now.isoweekday() not in iso_weekdays:
            now += dt.timedelta(days=1)
        return now

    def _get_building(self) -> str:
        if self.building == "":
            return "NA"
        return self.building

    def _get_room(self) -> str:
        if self.room == "":
            return "NA"
        return self.room

    def _get_location(self) -> str:
        return f"{self._get_building()}/{self._get_room()}"

    def __repr__(self) -> str:
        return f"{self.symbol}, {self.days}, {self.start_time} - {self.end_time}, {self._get_location()}"

    def toJson(self, until: dt.datetime, color: int) -> dict:
        event = {
            "summary": self.symbol,
            "location": self._get_location(),
            "colorId": color % 12,
            "start": {
                "dateTime": dt.datetime.combine(self._get_nearest_datetime(), self.start_time).isoformat(),
                "timeZone": "Asia/Riyadh"
            },
            "end": {
                "dateTime": dt.datetime.combine(self._get_nearest_datetime(), self.end_time).isoformat(),
                "timeZone": "Asia/Riyadh"
            },
            "recurrence": [
                f"RRULE:FREQ=WEEKLY"
                f";UNTIL={until.isoformat().replace('-', '').replace(':', '') + 'Z'}"
                f";BYDAY={','.join(self._get_days())}"
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        return event
