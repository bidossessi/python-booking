import abc
import datetime
import uuid
from typing import List, Optional

from pydantic.dataclasses import dataclass

from booking.domain.models import Booking
from booking.domain.repositories.common import Page, Paginate


@dataclass
class BookingQuery:
    date_start: Optional[datetime.datetime] = None
    date_end: Optional[datetime.datetime] = None
    resource_id: Optional[uuid.UUID] = None
    order_id: Optional[str] = None
    tags: Optional[List[str]] = None


class BookingRepository(abc.ABC):
    @abc.abstractmethod
    def check(self, query: BookingQuery) -> bool:
        pass

    @abc.abstractmethod
    def find(
        self,
        query: BookingQuery,
        paginate: Optional[Paginate] = None,
    ) -> Page[Booking]:
        pass

    @abc.abstractmethod
    def get(self, id: uuid.UUID) -> Booking:
        pass

    @abc.abstractmethod
    def save(self, item: Booking):
        pass

    @abc.abstractmethod
    def delete(self, id: uuid.UUID):
        pass
