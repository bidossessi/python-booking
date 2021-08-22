import datetime
import uuid
from typing import List, Optional
import dataclasses

from pydantic.dataclasses import dataclass


@dataclass
class ResourceIn:
    reference_id: str
    tags: List[str]


@dataclass
class Resource(ResourceIn):
    resource_id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)

    # def __eq__(self, o: object) -> bool:
    #     return hasattr(o, "resource_id") and self.resource_id == o.resource_id


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
    resource_id: uuid.UUID
    order_id: str
    booking_id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    system: bool = False
    tags: Optional[List[str]] = None

    @property
    def timeframe(self) -> Timeframe:
        return Timeframe(self.date_start, self.date_end)

    @timeframe.setter
    def timeframe(self, t: Timeframe):
        self.date_start = t.date_start
        self.date_end = t.date_end

    def intersects(
        self,
        start: datetime.datetime,
        end: datetime.datetime,
    ) -> bool:
        return self.date_start < end and self.date_end > start

    def overlaps_timeframe(self, t: Timeframe):
        return self.intersects(t.date_start, t.date_end)

    def overlaps_other(self, o: object):
        return self.intersects(o.date_start, o.date_end)

    # def __eq__(self, o: object) -> bool:
    #     return hasattr(o, "booking_id") and self.booking_id == o.booking_id

    # def __gt__(self, other: object):
    #     return self.date_start > other.date_start

    # def __lt__(self, other: object):
    #     return self.date_start < other.date_start
