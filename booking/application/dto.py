from booking.domain.repositories import ResourceQuery
from booking.domain.models import Resource
from typing import List, Optional
import uuid

from pydantic import BaseModel, validator
from pydantic.dataclasses import dataclass


@dataclass
class ResourceParams:
    resource_id: Optional[uuid.UUID] = None
    tags: Optional[str] = None

    def to_query(self) -> ResourceQuery:
        tags = self.tags.split(",") if self.tags else None
        return ResourceQuery(resource_id=self.resource_id, tags=tags)


class ResourceDTO(BaseModel):
    id: uuid.UUID
    tags: List[str]

    class Config:
        orm_mode = True


class ResourcePageDTO(BaseModel):
    count: int
    items: List[ResourceDTO]

    class Config:
        orm_mode = True
