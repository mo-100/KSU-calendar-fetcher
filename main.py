import settings
from classes.selenium_driver import SeleniumDriver
from classes.google_service import GoogleService
from selenium.webdriver import Edge, Firefox, Chrome, Safari


def main():

    try:
        driver = SeleniumDriver(
            Firefox()
        )

        driver.sign_in(settings.USERNAME, settings.PASSWORD)

        subjects = driver.get_subjects()

        finals = driver.get_finals()

        driver.driver.quit()

        # upload to google calendar

        service = GoogleService()
        # service.upload(subjects)
        # service.upload(finals)
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
