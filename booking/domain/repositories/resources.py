import abc
from booking.domain.repositories.common import Page, Paginate
import uuid
import datetime
from typing import List, Optional
from booking.domain.models import Resource
from pydantic.dataclasses import dataclass


@dataclass
class ResourceQuery:
    resource_id: Optional[uuid.UUID] = None
    tags: Optional[List[str]] = None


class ResourceRepository(abc.ABC):
    @abc.abstractmethod
    def find(
        self,
        query: ResourceQuery,
        paginate: Optional[Paginate] = None,
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
