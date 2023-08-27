from __future__ import print_function

import os
import bs4
import selenium.webdriver
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import settings
from class_event import KSUClass


def get_driver() -> selenium.webdriver:
    d = webdriver.Edge()
    d.implicitly_wait(2)
    return d


def sign_in(d: selenium.webdriver, user: str, pw: str) -> None:
    d.find_element(by=By.XPATH, value="//label[@class='pui-dropdown-label pui-inputtext ui-corner-all']").click()
    d.find_element(by=By.XPATH, value="//li[@data-label='طالب']").click()

    username_field = d.find_element(by=By.ID, value="username")
    username_field.send_keys(user)

    password_field = d.find_element(by=By.ID, value="password")
    password_field.send_keys(pw)
    password_field.send_keys(Keys.RETURN)


def get_rows(d: selenium.webdriver) -> bs4.element.ResultSet:
    table = d.find_element(by=By.ID, value="myForm:studScheduleTable")
    soup = bs4.BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
    soup = soup.find("tbody")
    return soup.findChildren("tr", recursive=False)


def get_subjects(row_list: bs4.element.ResultSet) -> list[KSUClass]:
    subject_list = list()
    for i, row in enumerate(row_list):
        columns = list(row)
        for time_rows in row.find("span", {"id": f"myForm:studScheduleTable:{i}:section"}).get_text().split("@n"):
            temp = time_rows.split("@")
            days = temp[0].strip().split()
            symbol = columns[1].get_text()
            full_name = columns[3].get_text()
            mode = columns[7].get_text()
            section = columns[9].get_text()
            time = temp[1].replace("t", "").replace("ص", "AM").replace("م", "PM")
            start_time = time.split("-")[0].strip()
            end_time = time.split("-")[1].strip()
            unit = temp[2].replace("u", "")
            building = temp[3].replace("b", "")
            floor = temp[4].replace("f", "")
            room = temp[6].replace("r", "").strip() + temp[5].replace("w", "").strip()
            subject_list.append(
                KSUClass(symbol, full_name, mode, section, days, start_time, end_time, building, room, unit, floor)
            )
    return subject_list


def get_service():
    scopes = [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events"
    ]
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def main():
    driver = get_driver()
    driver.get("https://edugate.ksu.edu.sa")
    sign_in(driver, settings.USERNAME, settings.PASSWORD)
    driver.get("https://edugate.ksu.edu.sa/ksu/ui/student/student_schedule/index/forwardStudentSchedule.faces")
    rows = get_rows(driver)
    driver.quit()
    subjects = get_subjects(rows)
    try:
        service = get_service()
        names = []
        for subject in subjects:
            if subject.symbol not in names:
                names.append(subject.symbol)
            color = names.index(subject.symbol)
            e = subject.toJson(settings.END_DATE, color)
            event = service.events().insert(calendarId='primary', body=e).execute()
            print(f"event created: {event.get('htmlLink')}")
    except HttpError as e:
        print('An error occurred: %s' % e)


if __name__ == '__main__':
    main()
