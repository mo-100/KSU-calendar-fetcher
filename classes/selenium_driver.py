import time

import bs4
from selenium.webdriver import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from classes.ksu_class import KSUClass
from classes.ksu_final import KSUFinal


class SeleniumDriver:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def sign_in(self, user: str, pw: str):
        self.driver.get("https://edugate.ksu.edu.sa")
        time.sleep(.5)
        self.driver.find_element(by=By.XPATH,
                                 value="//label[@class='pui-dropdown-label pui-inputtext ui-corner-all']").click()
        self.driver.find_element(by=By.XPATH, value="//li[@data-label='طالب']").click()

        username_field = self.driver.find_element(by=By.ID, value="username")
        username_field.send_keys(user)

        password_field = self.driver.find_element(by=By.ID, value="password")
        password_field.send_keys(pw)
        password_field.send_keys(Keys.RETURN)
        time.sleep(.5)

    def get_subjects(self) -> list[KSUClass]:
        self.driver.get("https://edugate.ksu.edu.sa/ksu/ui/student/student_schedule/index/forwardStudentSchedule.faces")
        time.sleep(1)

        table = self.driver.find_element(by=By.ID, value="myForm:studScheduleTable")
        soup = bs4.BeautifulSoup(table.get_attribute("innerHTML"), "html.parser")
        soup = soup.find("tbody")
        row_list = soup.findChildren("tr", recursive=False)

        subject_list = []
        for i, row in enumerate(row_list):
            columns = list(row)
            for time_rows in row.find("span", {"id": f"myForm:studScheduleTable:{i}:section"}).get_text().split("@n"):
                subject_list.append(KSUClass.from_text(columns, time_rows))
        return subject_list

    def get_finals(self) -> list[KSUFinal]:
        self.driver.get('https://edugate.ksu.edu.sa/ksu/ui/student/final_exams/index/forwardFinalExams.faces')
        time.sleep(1)

        rows = self.driver.find_elements(by=By.CLASS_NAME, value='ROW1')
        rows2 = self.driver.find_elements(by=By.CLASS_NAME, value='ROW2')
        rows.extend(rows2)

        def final_from_row(row):
            text_columns = row.find_elements(by=By.TAG_NAME, value='td')
            text_columns_inner = [t.get_attribute('innerHTML') for t in text_columns]
            return KSUFinal.from_text(text_columns_inner)

        return [final_from_row(row) for row in rows]
