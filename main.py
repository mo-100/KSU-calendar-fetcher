from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Firefox, Chrome, Edge, Safari

from fetcher.ksu_implementation import KSUCalendarScraper
from fetcher.utils.ical_utils import make_ksa_timezone, make_calendar_from_events


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
    user_input = input('Enter your browser [chrome, firefox, edge, safari]: ').lower()
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    webdriver = get_web_driver(user_input)

    scraper = KSUCalendarScraper(webdriver, username, password)
    events = scraper.get_events()
    print(events)
    calendar = make_calendar_from_events(
        events=events,
        timezone=make_ksa_timezone()
    )

    with open('term.ics', 'wb') as f:
        f.write(calendar.to_ical())


if __name__ == '__main__':
    main()
