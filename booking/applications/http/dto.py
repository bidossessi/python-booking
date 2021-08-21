import datetime

import dateutil
from dateutil.parser import parse
from booking.domain.repositories import BookingQuery, ResourceQuery
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


@dataclass
class TagsDTO:
    tags: List[str]


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


@dataclass
class BookingParams:
    date_start: str
    date_end: str
    order_id: Optional[uuid.UUID] = None
    resource_id: Optional[uuid.UUID] = None
    tags: Optional[str] = None

    @validator("date_start")
    def parse_date_start(cls, v):
        return parse(v)

    @validator("date_end")
    def parse_date_end(cls, v):
        return parse(v)

    def to_query(self) -> BookingQuery:
        tags = self.tags.split(",") if self.tags else None
        return BookingQuery(
            date_start=self.date_start,
            date_end=self.date_end,
            order_id=self.order_id,
            resource_id=self.resource_id,
            tags=tags,
        )


class BookingDTO(BaseModel):
    resource_id: uuid.UUID
    order_id: str
    date_start: datetime.datetime
    date_end: datetime.datetime
    tags: List[str]

    class Config:
        orm_mode = True


class BookingPageDTO(BaseModel):
    count: int
    items: List[BookingDTO]

    class Config:
        orm_mode = True
