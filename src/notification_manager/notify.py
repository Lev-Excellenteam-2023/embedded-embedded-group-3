from abc import ABC, abstractmethod
from dataclasses import dataclass


class Notify(ABC):
    """
   An abstract base class for fire alert notification mechanisms.

   Subclasses should implement the `send_notification` method to provide
   specific notification functionality.
   """
    @abstractmethod
    def send_notification(self, image, coordinates: tuple[float, float]) -> None:
        pass
