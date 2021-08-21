import datetime

from dateutil.parser import parse
from booking.domain.repositories import BookingQuery, ResourceQuery
from typing import List, Optional
import uuid

from pydantic import BaseModel, validator

from booking.domain.services import BookingService, ResourceService
from booking.data.memory import MemoryResourceRepo, MemoryBookingRepo


async def get_resource_service() -> ResourceService:
    return ResourceService(
        booking_repo=MemoryBookingRepo(),
        resource_repo=MemoryResourceRepo(),
    )


async def get_booking_service() -> BookingService:
    return BookingService(
        booking_repo=MemoryBookingRepo(),
        resource_repo=MemoryResourceRepo(),
    )


class ResourceParams(BaseModel):
    resource_id: Optional[uuid.UUID] = None
    tags: Optional[str] = None

    def to_query(self) -> ResourceQuery:
        tags = self.tags.split(",") if self.tags else None
        return ResourceQuery(resource_id=self.resource_id, tags=tags)


class TagsIn(BaseModel):
    tags: List[str]


class ResourceIn(BaseModel):
    id: uuid.UUID
    tags: List[str]


class ResourceOut(ResourceIn):
    class Config:
        orm_mode = True


class ResourceOutPage(BaseModel):
    count: int
    items: List[ResourceOut]

    class Config:
        orm_mode = True


class BookingParams(BaseModel):
    date_start: str
    date_end: str
    resource_id: Optional[uuid.UUID] = None
    order_id: Optional[str] = None
    tags: Optional[str] = None

    @validator("date_start")
    def parse_date_start(cls, v):
        return parse(v)

    @validator("date_end", check_fields=False)
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


class BookingIn(BookingParams):
    resource_id: uuid.UUID
    order_id: str

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

    class Config:
        orm_mode = True


class BookingOutPage(BaseModel):
    count: int
    items: List[BookingOut]

    class Config:
        orm_mode = True
