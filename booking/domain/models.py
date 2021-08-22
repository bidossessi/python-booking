import datetime
import uuid
from typing import List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class ResourceIn:
    id: uuid.UUID
    tags: List[str]


@dataclass
class Resource(ResourceIn):
    def __eq__(self, o: object) -> bool:
        return hasattr(o, "id") and self.id == o.id


@dataclass
class Timeframe:
    date_start: datetime.datetime
    date_end: datetime.datetime


@dataclass
class BookingIn(Timeframe):
    resource_id: uuid.UUID
    order_id: str
    system: bool = False


@dataclass
class Booking(Timeframe):
    id: uuid.UUID
    resource_id: uuid.UUID
    order_id: str
    system: bool = False
    tags: Optional[List[str]] = None

    def intersects(
        self,
        start: Optional[datetime.datetime],
        end: Optional[datetime.datetime],
    ) -> bool:
        if not start and not end:
            return True
        return self.date_start < end and self.date_end > start

    def __eq__(self, o: object) -> bool:
        return hasattr(o, "id") and self.id == o.id

    def __gt__(self, other: object):
        return isinstance(other, "Booking") and self.date_start > other.date_start

    def __lt__(self, other: object):
        return isinstance(other, "Booking") and self.date_start < other.date_start
