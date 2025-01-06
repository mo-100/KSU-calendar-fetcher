from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Firefox, Chrome, Edge, Safari

from fetcher.ksu_implementation import KSUCalendarScraper
from fetcher.utils.ical_utils import make_ksa_timezone, make_calendar_from_events
import sys

valid_drivers = {'chrome', 'firefox', 'edge', 'safari'}
def get_web_driver(driver: str) -> WebDriver:
    match driver.lower():
        case 'chrome':
            return Chrome()
        case 'firefox':
            return Firefox()
        case 'edge':
            return Edge()
        case 'safari':
            return Safari()
        case _:
            raise Exception('Invalid input')


def main():
    args = sys.argv[1:]
    if len(args) != 3:
        print("invalid arguments")
        return
    browser = args[0].lower()
    if browser not in valid_drivers:
        print(f"invalid driver, valid drivers: {list(valid_drivers)}")
        return
    username = args[1]
    password = args[2]

    print(f"opening {browser} browser")
    webdriver = get_web_driver(browser)
    print(f"{browser} opened")
    scraper = KSUCalendarScraper(webdriver, username, password)
    print("starting scrape process")
    events = scraper.get_events()
    print("scrape done")

    print(f"found {set([e.symbol for e in events])}")

    calendar = make_calendar_from_events(
        events=events,
        timezone=make_ksa_timezone()
    )

    with open('term.ics', 'wb') as f:
        f.write(calendar.to_ical())

    print("file generated")


if __name__ == '__main__':
    main()
