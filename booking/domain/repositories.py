import abc
import uuid
import datetime
import dataclasses
from typing import Iterable, List, Optional, TypeVar, Generic
from booking.domain.models import Booking, Resource
from pydantic.dataclasses import dataclass


@dataclass
class Paginate:
    per_page: Optional[int] = None
    page: Optional[int] = None


T = TypeVar("T")


class Page(Generic[T]):
    def __init__(self, items: List[T], count: int) -> None:
        self.count: int = count
        self.items: List[T] = items


@dataclass
class ResourceQuery:
    resource_id: Optional[uuid.UUID] = None
    tags: Optional[List[str]] = None


class ResourceRepository(abc.ABC):
    @abc.abstractmethod
    def find(
        self,
        query: ResourceQuery,
        paginate: Optional[Paginate],
    ) -> Page[Resource]:
        pass

    @abc.abstractmethod
    def get(self, id: uuid.UUID) -> Optional[Resource]:
        pass

    @abc.abstractmethod
    def save(self, item: Resource) -> Resource:
        pass

    @abc.abstractmethod
    def delete(self, item: Resource):
        pass


@dataclass
class BookingQuery:
    date_start: datetime.datetime
    date_end: datetime.datetime
    resource_id: Optional[uuid.UUID]
    tags: List[str]


class BookingRepository(abc.ABC):
    @abc.abstractmethod
    def find(
        self,
        query: BookingQuery,
        paginate: Optional[Paginate],
    ) -> Iterable[Booking]:
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
