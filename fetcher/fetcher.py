from fetcher.ksu_class import KSUClass
from fetcher.ksu_final import KSUFinal
from fetcher.selenium_driver import SeleniumDriver


class Fetcher:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    # @use_cache
    def fetch(self, driver: SeleniumDriver) -> tuple[list[KSUClass], list[KSUFinal]]:
        try:
            driver.sign_in(self.username, self.password)
            classes = driver.get_subjects()
            finals = driver.get_finals()
            return classes, finals
        except Exception as e:
            print(f'An error occurred during fetching: {e}')
