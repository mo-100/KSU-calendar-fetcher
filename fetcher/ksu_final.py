from dataclasses import dataclass
import datetime
from hijridate import Hijri


@dataclass
class KSUFinal:
    symbol: str
    full_name: str
    section: str
    # day: str
    # time: datetime.time
    # date: datetime.date
    datetime: datetime.datetime


def make_final_from_text(text_columns) -> KSUFinal:
    symbol = text_columns[0]
    full_name = text_columns[1]
    section = text_columns[2]
    # day = text_columns[-3].strip()
    time = text_columns[-2]
    time = datetime.datetime.strptime(time.strip(), '%H:%M').time()
    date = text_columns[-1]
    date_list_temp = [int(x) for x in date.split('-')]
    date = Hijri(date_list_temp[2], date_list_temp[1], date_list_temp[0]).to_gregorian()

    datetime_ = datetime.datetime.combine(date, time)
    return KSUFinal(symbol, full_name, section, datetime_)
