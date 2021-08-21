from typing import Iterable, List
import uuid
from booking.domain import repositories, models, errors


class ResourceService:
    def __init__(self, repository: repositories.ResourceRepository) -> None:
        self.repository = repository

    def find(
        self,
        query: repositories.ResourceQuery,
        paginate: repositories.Paginate,
    ) -> Iterable[models.Resource]:
        return self.repository.find(query, paginate)

    def create(self, resource: models.Resource) -> models.Resource:
        return self.repository.save(resource)

    def update_tags(self, id: uuid.UUID, tags: List[str]) -> models.Resource:
        match = self.repository.get(id)
        if not match:
            raise errors.ResourceNotFound(id)
        match.tags = tags
        return self.repository.save(match)

    def delete(self, id: models.Resource) -> models.Resource:
        match = self.repository.get(id)
        if not match:
            raise errors.ResourceNotFound(id)
        return self.repository.delete(match)
