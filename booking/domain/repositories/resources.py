import abc
import uuid
from typing import List, Optional

from pydantic.dataclasses import dataclass

from booking.domain.models import Resource
from booking.domain.repositories.common import Page, Paginate


@dataclass
class ResourceQuery:
    resource_id: Optional[uuid.UUID] = None
    tags: Optional[List[str]] = None


class ResourceRepository(abc.ABC):
    @abc.abstractmethod
    def check(self, query: ResourceQuery) -> bool:
        pass

    @abc.abstractmethod
    def find(
        self,
        query: ResourceQuery,
        paginate: Optional[Paginate] = None,
    ) -> Page[Resource]:
        pass

    @abc.abstractmethod
    def get(self, id: uuid.UUID) -> Resource:
        pass

    @abc.abstractmethod
    def save(self, item: Resource) -> Resource:
        pass

    @abc.abstractmethod
    def delete(self, id: uuid.UUID):
        pass
