import uuid
import datetime
from dateutil import rrule
from typing import List, Optional
from pydantic.dataclasses import dataclass


@dataclass
class Resource:
    id: uuid.UUID
    tags: List[str]

    def __eq__(self, o: object) -> bool:
        return hasattr(o, "id") and self.id == o.id


@dataclass
class Booking:
    id: uuid.UUID
    resource_id: uuid.UUID
    order_id: str
    date_start: datetime.datetime
    date_end: datetime.datetime

    def __eq__(self, o: object) -> bool:
        return hasattr(o, "id") and self.id == o.id
