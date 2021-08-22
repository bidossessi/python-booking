import uuid
from typing import Iterable, List

from booking.domain import models, repository


class ResourceService:
    def __init__(self, repo: repository.BookingRepository) -> None:
        self.repo = repo

    def find(self, query: repository.ResourceQuery) -> Iterable[models.Resource]:
        return self.repo.find_resources(query)

    def find_bookings_for(self, item_id: uuid.UUID, timeframe: models.Timeframe):
        query = repository.BookingQuery(
            resource_id=item_id,
            date_start=timeframe.date_start,
            date_end=timeframe.date_end,
        )
        return self.repo.find_bookings(query)

    def create(self, resource_in: models.ResourceIn) -> models.Resource:
        resource = models.Resource(
            reference_id=resource_in.reference_id,
            tags=resource_in.tags,
        )
        return self.repo.create_resource(resource)

    def get(self, item_id: uuid.UUID) -> models.Resource:
        return self.repo.get_resource(item_id)

    def update(self, item_id: uuid.UUID, tags: List[str]) -> models.Resource:
        return self.repo.update_resource(item_id, tags)

    def delete(self, item_id: uuid.UUID) -> models.Resource:
        return self.repo.delete_resource(item_id)

    def list_free(
        self,
        timeframe: models.Timeframe,
        tags: List[str],
    ) -> Iterable[models.Resource]:
        return self.repo.find_free_resources(timeframe, tags)
