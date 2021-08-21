import abc
from booking.domain.repositories.common import Page, Paginate
import uuid
import datetime
from typing import List, Optional
from booking.domain.models import Booking
from pydantic.dataclasses import dataclass


@dataclass
class BookingQuery:
    date_start: datetime.datetime
    date_end: datetime.datetime
    resource_id: Optional[uuid.UUID] = None
    order_id: Optional[str] = None
    tags: Optional[List[str]] = None


class BookingRepository(abc.ABC):
    @abc.abstractmethod
    def find(
        self,
        query: BookingQuery,
        paginate: Optional[Paginate] = None,
    ) -> Page[Booking]:
        pass

    @abc.abstractmethod
    def get(self, id: uuid.UUID) -> Optional[Booking]:
        pass

    @abc.abstractmethod
    def save(self, item: Booking):
        pass

    @abc.abstractmethod
    def delete(self, item: Booking):
        pass
