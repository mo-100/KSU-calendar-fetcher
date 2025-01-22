import datetime
from dataclasses import dataclass

import bs4
import pytz
from hijridate import Hijri
from icalendar import Event, vText
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from fetcher.abstract_classes import CalendarEvent, CalendarScraper
from fetcher.utils.date_utils import get_nearest_datetime, get_day_abbr
from fetcher.utils.ical_utils import make_alarm
from fetcher.utils.config import LAST_STUDY_DAY, DRIVER_WAIT_TIME, CLASS_ALARM, FINAL_ALARM
from fetcher.utils.string_utils import apply_replaces


@dataclass
class KSUFinal(CalendarEvent):
    symbol: str
    full_name: str
    section: str
    datetime: datetime.datetime

    @staticmethod
    def from_text(text_columns: list[str | None]) -> "KSUFinal":
        symbol = text_columns[0]
        full_name = text_columns[1]
        section = text_columns[2]
        time_str = text_columns[-2]
        time_ = datetime.datetime.strptime(time_str.strip(), '%H:%M').time()
        date = text_columns[-1]
        date_list_temp = [int(x) for x in date.split('-')]
        date_greg = Hijri(date_list_temp[2], date_list_temp[1], date_list_temp[0]).to_gregorian()

        datetime_ = datetime.datetime.combine(date_greg, time_)
        return KSUFinal(symbol, full_name, section, datetime_)

    def make_event(self) -> Event:
        timezone = pytz.timezone('Asia/Riyadh')

        start_date = self.datetime
        end_date = self.datetime + datetime.timedelta(hours=2)

        start_date = timezone.localize(start_date)
        end_date = timezone.localize(end_date)

        event = Event()

        event.add('summary', apply_replaces(f'{self.symbol} final'))
        event.add('dtstart', start_date)
        event.add('dtend', end_date)
        event.add('uid', f'{self.symbol}-final')
        event.add('dtstamp', datetime.datetime.now(pytz.utc))
        event.add_component(
            make_alarm(
                datetime.timedelta(hours=FINAL_ALARM),
                msg=f'Reminder: final in {FINAL_ALARM} hours',
            )
        )
        return event


@dataclass
class KSUClass(CalendarEvent):
    symbol: str
    full_name: str
    type_: str
    section: str
    days: list[int]
    start_time: datetime.time
    end_time: datetime.time
    unit: str
    floor: str
    location: str

    @staticmethod
    def from_text(col: list, time_row: str) -> "KSUClass":
        temp = time_row.split("@")
        days = temp[0].strip().split()
        days = [int(day) for day in days]
        symbol = col[1].get_text().strip()
        full_name = col[3].get_text().strip()
        type_ = col[7].get_text().strip()
        section = col[9].get_text().strip()
        time_ = temp[1].replace("t", "").replace("ص", "AM").replace("م", "PM")
        start_time = time_.split("-")[0].strip()
        start_time = datetime.datetime.strptime(start_time, '%I:%M %p').time()
        end_time = time_.split("-")[1].strip()
        end_time = datetime.datetime.strptime(end_time, '%I:%M %p').time()
        unit = temp[2].replace("u", "").strip()
        building = temp[3].replace("b", "").strip()
        floor = temp[4].replace("f", "").strip()
        room = temp[6].replace("r", "").strip() + temp[5].replace("w", "").strip()
        if not room:
            room = "NA"
        if not building:
            building = "NA"
        location = f"Building: {building}, Room: {room}"
        return KSUClass(symbol, full_name, type_, section, days, start_time, end_time, unit, floor, location)

    def make_event(self) -> Event:

        timezone = pytz.timezone('Asia/Riyadh')
        nearest_date = get_nearest_datetime(self.days)

        start_date = datetime.datetime.combine(nearest_date, self.start_time)
        end_date = datetime.datetime.combine(nearest_date, self.end_time)

        start_date = timezone.localize(start_date)
        end_date = timezone.localize(end_date)

        by_day = [get_day_abbr(day) for day in self.days]

        event = Event()

        event.add('summary', apply_replaces(f'{self.type_} {self.symbol}'))
        event.add('location', vText(self.location))
        event.add('dtstart', start_date)
        event.add('dtend', end_date)
        event.add('rrule', {
            'FREQ': 'WEEKLY',
            'UNTIL': LAST_STUDY_DAY,
            'BYDAY': by_day,
        })
        event.add('uid', f'{self.symbol}-{self.type_}-{self.start_time}-{self.days}')
        event.add('dtstamp', datetime.datetime.now(pytz.utc))
        event.add_component(
            make_alarm(
                datetime.timedelta(minutes=CLASS_ALARM),
                msg=f'Reminder: class in {CLASS_ALARM} minutes'
            )
        )
        return event


class KSUCalendarScraper(CalendarScraper):
    def __init__(self, webdriver: WebDriver, username: str, password: str):
        self.webdriver = webdriver
        self.username = username
        self.password = password
        self.logged_in = False

    def log_in(self):
        self.webdriver.get("https://edugate.ksu.edu.sa")

        username_field = self.webdriver.find_element(by=By.ID, value="username")
        username_field.send_keys(self.username)

        password_field = self.webdriver.find_element(by=By.ID, value="password")
        password_field.send_keys(self.password)

        password_field.send_keys(Keys.RETURN)
        
        try:
            wait = WebDriverWait(self.webdriver, timeout=DRIVER_WAIT_TIME)
            wait.until(lambda d : not password_field.is_displayed())
        except StaleElementReferenceException:
            pass

        self.logged_in = True

    def get_classes(self) -> list[CalendarEvent]:
        self.webdriver.get("https://edugate.ksu.edu.sa/ksu/ui/student/student_schedule/index/forwardStudentSchedule.faces")

        table = self.webdriver.find_element(by=By.ID, value="myForm:studScheduleTable")
        soup = bs4.BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
        soup = soup.find("tbody")
        row_list = soup.findChildren("tr", recursive=False)

        classes = []
        for i, row in enumerate(row_list):
            columns = list(row)
            for time_row in row.find("span", {"id": f"myForm:studScheduleTable:{i}:section"}).get_text().split("@n"):
                if not time_row:
                    continue
                # else:
                #     print(columns, time_rows)
                c = KSUClass.from_text(columns, time_row)
                classes.append(c)
        return classes

    def get_finals(self) -> list[CalendarEvent]:
        self.webdriver.get('https://edugate.ksu.edu.sa/ksu/ui/student/final_exams/index/forwardFinalExams.faces')

        rows = self.webdriver.find_elements(by=By.CLASS_NAME, value='ROW1')
        rows.extend(self.webdriver.find_elements(by=By.CLASS_NAME, value='ROW2'))

        finals = []
        for row in rows:
            text_columns = row.find_elements(by=By.TAG_NAME, value='td')
            text_columns_inner = [t.get_attribute('innerHTML') for t in text_columns]
            if not text_columns_inner[-1]:
                continue
            # else:
            #     print(text_columns_inner[-1])
            f = KSUFinal.from_text(text_columns_inner)
            finals.append(f)

        return finals

    def is_alive(self):
        try:
            s = self.webdriver.title
            return True
        except:
            return False

    def get_events(self) -> list[CalendarEvent]:
        try:
            if not self.is_alive():
                raise Exception('Browser is closed')
            if not self.logged_in:
                print('logging in')
                self.log_in()
                print('logged in')
            print("getting finals")
            finals = self.get_finals()
            print("getting classes")
            classes = self.get_classes()
            return finals + classes
        except Exception as e:
            raise e
        finally:
            print('quitting webdriver')
            self.webdriver.quit()
