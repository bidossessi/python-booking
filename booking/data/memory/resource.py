import uuid
from typing import List, Optional

from booking.domain.errors import ResourceNotFound
from booking.domain.models import Resource
from booking.domain.repositories import (
    Page,
    Paginate,
    ResourceQuery,
    ResourceRepository,
)
from booking.helpers import singleton


def _match_resource(item: Resource, query) -> bool:
    matches_res = item.id == query.resource_id if query.resource_id else True
    matches_tags = any(x in query.tags for x in item.tags) if query.tags else True
    return all([matches_res, matches_tags])


@singleton
class MemoryResourceRepo(ResourceRepository):
    def __init__(self) -> None:
        super().__init__()
        self.store: List[Resource] = []

    def check(self, query: ResourceQuery) -> bool:
        return any(item for item in self.store if _match_resource(item, query))

    def find(
        self,
        query: ResourceQuery,
        # TODO: implement poor man's pagination
        paginate: Optional[Paginate] = None,
    ) -> Page[Resource]:

        matches = [item for item in self.store if _match_resource(item, query)]
        print(self.store)
        return Page(matches, len(matches))

    def get(self, id: uuid.UUID) -> Resource:
        try:
            return next(item for item in self.store if item.id == id)
        except StopIteration:
            raise ResourceNotFound(id)

    def save(self, item: Resource) -> Resource:
        try:
            match = self.get(item.id)
            self.store = [item if s == match else s for s in self.store]
        except Exception:
            self.store.append(item)
        return item

    def delete(self, id: uuid.UUID):
        item = self.get(id)
        self.store = [match for match in self.store if match is not item]
