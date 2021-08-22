from typing import List
import uuid
from booking.domain import repositories, models, errors


class ResourceService:
    def __init__(
        self,
        resource_repo: repositories.ResourceRepository,
        booking_repo: repositories.BookingRepository,
    ) -> None:
        self.resource_repo = resource_repo
        self.booking_repo = booking_repo

    def find(
        self,
        query: repositories.ResourceQuery,
        paginate: repositories.Paginate,
    ) -> repositories.Page[models.Resource]:
        return self.resource_repo.find(query, paginate=paginate)

    def create(self, resource: models.ResourceIn) -> models.Resource:
        return self.resource_repo.save(resource)

    def get(self, id: uuid.UUID) -> models.Resource:
        return self.resource_repo.get(id)

    def update(self, id: uuid.UUID, tags: List[str]) -> models.Resource:
        match = self.resource_repo.get(id)
        match.tags = tags
        return self.resource_repo.save(match)

    def delete(self, id: models.Resource) -> models.Resource:
        return self.resource_repo.delete(id)