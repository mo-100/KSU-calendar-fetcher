import datetime
from abc import ABC, abstractmethod


class Uploadable(ABC):
    symbol: str

    @abstractmethod
    def to_json(self, color: int) -> dict:
        pass
