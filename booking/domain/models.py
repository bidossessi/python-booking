import uuid
import datetime
from dateutil import rrule
from typing import List, Optional
from pydantic.dataclasses import dataclass
from pydantic import ValidationError


@dataclass
class ResourceIn:
    id: uuid.UUID
    tags: List[str]


@dataclass
class Resource(ResourceIn):
    def __eq__(self, o: object) -> bool:
        return hasattr(o, "id") and self.id == o.id


@dataclass
class BookingIn:
    resource_id: uuid.UUID
    order_id: str
    date_start: datetime.datetime
    date_end: datetime.datetime


@dataclass
class Booking(BookingIn):
    tags: List[str]

    # @validator("date_end")
    def end_before_start(cls, v, values, **kwargs):
        if "date_start" in values and v < values["date_start"]:
            raise ValueError("End must be after start")
        return v

    def intersects(self, start: datetime.datetime, end: datetime.datetime) -> bool:
        return self.date_start < end and self.date_end > start

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, "Booking")
            and other.date_start == self.date_start
            and other.date_end == self.date_end
        )

    def __gt__(self, other: object):
        return isinstance(other, "Booking") and self.date_start > other.date_start

    def __lt__(self, other: object):
        return isinstance(other, "Booking") and self.date_start < other.date_start
