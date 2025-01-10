from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Firefox, Chrome, Edge, Safari
from fetcher.utils.config import DRIVER_WAIT_TIME


valid_drivers = {'chrome', 'firefox', 'edge', 'safari'}
def get_web_driver(driver_str: str) -> WebDriver:
    match driver_str.lower():
        case 'chrome':
            driver = Chrome()
        case 'firefox':
            driver = Firefox()
        case 'edge':
            driver = Edge()
        case 'safari':
            driver = Safari()
        case _:
            raise Exception('Invalid input')
    driver.implicitly_wait(DRIVER_WAIT_TIME)
    return driver