import datetime
import uuid
from typing import List, Optional

from dateutil.parser import parse
from pydantic import BaseModel, validator

from booking.data.memory import MemoryRepository
from booking.domain.repository import BookingQuery, ResourceQuery
from booking.domain.services import BookingService, ResourceService


async def get_resource_service() -> ResourceService:
    return ResourceService(repo=MemoryRepository())


async def get_booking_service() -> BookingService:
    return BookingService(repo=MemoryRepository())


class TagsParams(BaseModel):
    tags: Optional[str] = None

    @validator("tags", always=True)
    def split_tags(cls, v):
        if v:
            return v.split(",")


class ResourceParams(TagsParams):
    resource_id: Optional[uuid.UUID] = None
    reference_id: Optional[str] = None

    def to_query(self) -> ResourceQuery:
        return ResourceQuery(
            resource_id=self.resource_id,
            reference_id=self.reference_id,
            tags=self.tags,
        )


class TagsIn(BaseModel):
    tags: List[str]


class ResourceIn(BaseModel):
    reference_id: str
    tags: List[str]


class ResourceOut(ResourceIn):
    resource_id: uuid.UUID

    class Config:
        orm_mode = True


class ResourceOutPage(BaseModel):
    items: List[ResourceOut]
    count: Optional[int]

    @validator("count", always=True)
    def compute_count(cls, v, values, **kwargs):
        return len(values.get("items", []))

    class Config:
        orm_mode = True


class TimeFrameIn(BaseModel):
    date_start: str
    date_end: str

    @validator("date_start", always=True)
    def parse_date_start(cls, v):
        return parse(v)

    @validator("date_end", always=True)
    def parse_date_end(cls, v):
        return parse(v)


class BookingParams(TimeFrameIn, TagsParams):
    resource_id: Optional[uuid.UUID] = None
    order_id: Optional[str] = None

    def to_query(self) -> BookingQuery:
        return BookingQuery(
            date_start=self.date_start,
            date_end=self.date_end,
            order_id=self.order_id,
            resource_id=self.resource_id,
            tags=self.tags,
        )


class BookingIn(BookingParams):
    resource_id: uuid.UUID
    order_id: str
    system: bool = False

    @validator("date_start")
    def validate_date_start(cls, v):
        if v < datetime.datetime.today():
            raise ValueError("Invalid start date")
        return v

    @validator("date_end")
    def validate_date_end(cls, v, values, **kwargs):
        if "date_start" in values and v < values["date_start"]:
            raise ValueError("Invalid end date")
        return v


class BookingOut(BaseModel):
    resource_id: uuid.UUID
    order_id: str
    date_start: datetime.datetime
    date_end: datetime.datetime
    system: bool

    class Config:
        orm_mode = True


class BookingOutPage(BaseModel):
    items: List[BookingOut]
    count: Optional[int]

    @validator("count", always=True)
    def compute_count(cls, v, values, **kwargs):
        return len(values.get("items", []))

    class Config:
        orm_mode = True
