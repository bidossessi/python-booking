import uuid
import datetime
from typing import Iterable, List, Optional
from pydantic.dataclasses import dataclass
from booking.helpers import singleton
from booking.domain.models import Booking, Resource
from booking.domain.repositories import (
    Page,
    Paginate,
    ResourceQuery,
    ResourceRepository,
)


@singleton
class MemoryResourceRepo(ResourceRepository):
    def __init__(self) -> None:
        super().__init__()
        self.store: List[Resource] = []

    def find(
        self,
        query: ResourceQuery,
        paginate: Optional[Paginate],
    ) -> Page[Resource]:
        matched_tags = (
            [item for item in self.store if any(x in query.tags for x in item.tags)]
            if query.tags
            else self.store
        )
        matched_id = (
            [item for item in matched_tags if item.id == query.resource_id]
            if query.resource_id
            else matched_tags
        )
        return Page(matched_id, len(matched_id))

    def get(self, id: uuid.UUID) -> Optional[Resource]:
        try:
            return next(item for item in self.store if item.id == id)
        except StopIteration:
            pass

    def save(self, item: Resource) -> Resource:
        self.store.append(item)

    def delete(self, item: Resource):
        self.store = [match for match in self.store if match is not item]
