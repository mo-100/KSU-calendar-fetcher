from fetcher import Fetcher
from fetcher.color_generator import ColorGenerator
from fetcher.selenium_driver import SeleniumDriver
from fetcher.utils import make_calendar, make_event, make_event_final, get_driver


def main():
    webdriver = get_driver()
    driver = SeleniumDriver(webdriver)
    f = Fetcher(
        username=input('Username: '),
        password=input('Password: '),
    )
    classes, finals = f.fetch(driver)

    print(classes)
    print(finals)

    calendar = make_calendar()
    cgen = ColorGenerator()
    for c in classes:
        calendar.add_component(
            make_event(
                c,
                cgen.color_of(c.symbol)
            )
        )
    for f in finals:
        calendar.add_component(
            make_event_final(
                f,
                cgen.color_of(f.symbol)
            )
        )

    driver.driver.quit()

    with open('term.ics', 'wb') as f:
        f.write(calendar.to_ical())


if __name__ == '__main__':
    main()
