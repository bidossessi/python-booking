import abc
import datetime
import uuid
from typing import Iterable, List, Optional
from pydantic.dataclasses import dataclass
from booking.domain import models


@dataclass
class FreeQuery:
    date_start: Optional[datetime.datetime] = None
    date_end: Optional[datetime.datetime] = None
    tags: Optional[List[str]] = None


@dataclass
class BookingQuery(FreeQuery):
    resource_id: Optional[uuid.UUID] = None
    order_id: Optional[str] = None


@dataclass
class ResourceQuery:
    resource_id: Optional[uuid.UUID] = None
    reference_id: str = None
    tags: Optional[List[str]] = None


class BookingRepository(abc.ABC):
    @abc.abstractmethod
    def find_resources(
        self,
        query: ResourceQuery,
    ) -> Iterable[models.Resource]:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_free_resources(
        self, timeframe: models.Timeframe, tags: List[str]
    ) -> Iterable[models.Resource]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_resource(self, item_id: uuid.UUID) -> models.Resource:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_resource(self, item: models.Resource) -> models.Resource:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_resource(self, item_id: uuid.UUID, tags: List[str]) -> models.Resource:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_resource(self, item_id: uuid.UUID):
        raise NotImplementedError()

    @abc.abstractmethod
    def check_booking_overlap(self, item: models.Booking) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_bookings(self, query: BookingQuery) -> Iterable[models.Booking]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_booking(self, item: models.Booking):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_booking(self, item_id: uuid.UUID) -> models.Booking:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_booking(self, item_id: uuid.UUID, timeframe: models.Timeframe):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_booking(self, item_id: uuid.UUID):
        raise NotImplementedError()
