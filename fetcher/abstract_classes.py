from abc import ABC, abstractmethod
from icalendar import Event


class CalendarEvent(ABC):
    @abstractmethod
    def make_event(self) -> Event:
        raise NotImplementedError()


class CalendarScraper(ABC):
    @abstractmethod
    def get_events(self) -> list[CalendarEvent]:
        raise NotImplementedError()
