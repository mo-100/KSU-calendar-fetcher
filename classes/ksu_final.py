import datetime as dt
from hijridate import Hijri

from classes.uploadable import Uploadable


class KSUFinal(Uploadable):
    def __init__(self, symbol, full_name, section, day, time, date):
        self.symbol = symbol
        self.full_name = full_name
        self.section = section
        self.day = day.strip()

        self.time = dt.datetime.strptime(time.strip(), '%H:%M').time()
        date_list_temp = [int(x) for x in date.split('-')]
        self.date = Hijri(date_list_temp[2], date_list_temp[1], date_list_temp[0]).to_gregorian()
        self.datetime = dt.datetime.combine(self.date, self.time)

    @staticmethod
    def from_text(text_columns):
        symbol = text_columns[0]
        full_name = text_columns[1]
        section = text_columns[2]
        day = text_columns[-3]
        time = text_columns[-2]
        date = text_columns[-1]
        return KSUFinal(symbol, full_name, section, day, time, date)

    def to_json(self, color):
        start_date = self.datetime.isoformat()
        end_date = (self.datetime + dt.timedelta(hours=3)).isoformat()
        event = {
            "summary": self.symbol,
            "colorId": color,
            "start": {
                "dateTime": start_date,
                "timeZone": "Asia/Riyadh"
            },
            "end": {
                "dateTime": end_date,
                "timeZone": "Asia/Riyadh"
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},
                ],
            },
        }
        return event
