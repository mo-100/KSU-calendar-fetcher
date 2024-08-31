import datetime
from dataclasses import dataclass


@dataclass
class KSUClass:
    symbol: str
    full_name: str
    type_: str
    section: str
    days: list[int]
    start_time: datetime.time
    end_time: datetime.time
    building: str
    room: str
    unit: str
    floor: str
    location: str


def make_class_from_text(col, time_rows) -> KSUClass:
    temp = time_rows.split("@")
    days = temp[0].strip().split()
    days = [int(day) for day in days]
    symbol = col[1].get_text().strip()
    full_name = col[3].get_text().strip()
    type_ = col[7].get_text().strip()
    section = col[9].get_text().strip()
    time = temp[1].replace("t", "").replace("ص", "AM").replace("م", "PM")
    start_time = time.split("-")[0].strip()
    start_time = datetime.datetime.strptime(start_time.strip(), '%I:%M %p').time()
    end_time = time.split("-")[1].strip()
    end_time = datetime.datetime.strptime(end_time.strip(), '%I:%M %p').time()
    unit = temp[2].replace("u", "").strip()
    building = temp[3].replace("b", "").strip()
    floor = temp[4].replace("f", "").strip()
    room = temp[6].replace("r", "").strip() + temp[5].replace("w", "").strip()
    if not room:
        room = "NA"
    if not building:
        building = "NA"
    location = f"{building}/{room}"
    return KSUClass(symbol, full_name, type_, section, days, start_time, end_time, building, room, unit, floor,
                    location)
