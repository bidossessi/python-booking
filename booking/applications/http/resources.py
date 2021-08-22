import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from booking.applications.http.models import (
    BookingOutPage,
    ResourceIn,
    ResourceOut,
    ResourceOutPage,
    ResourceParams,
    TagsIn,
    TimeFrameIn,
    get_booking_service,
    get_resource_service,
)
from booking.domain.repositories import Paginate
from booking.domain.repositories.bookings import BookingQuery
from booking.domain.services import ResourceService
from booking.domain.services.bookings import BookingService

router = APIRouter()


@router.get("/", response_model=ResourceOutPage)
async def find_resources(
    params: ResourceParams = Depends(ResourceParams),
    paginate: Paginate = Depends(Paginate),
    service: ResourceService = Depends(get_resource_service),
):
    return service.find(params.to_query(), paginate)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=ResourceOut)
async def create_resource(
    dao: ResourceIn,
    service: ResourceService = Depends(get_resource_service),
):
    return service.create(dao)


@router.get("/{resource_id}/", response_model=ResourceOut)
async def get_resource(
    resource_id: uuid.UUID,
    service: ResourceService = Depends(get_resource_service),
):
    return service.get(resource_id)


@router.patch("/{resource_id}/", response_model=ResourceOut)
async def patch_resource(
    resource_id: uuid.UUID,
    dto: TagsIn,
    service: ResourceService = Depends(get_resource_service),
):
    return service.update(resource_id, dto.tags)


@router.get("/{resource_id}/bookings", response_model=BookingOutPage)
async def get_resource_bookings(
    resource_id: uuid.UUID,
    timeframe: TimeFrameIn = Depends(TimeFrameIn),
    paginate: Paginate = Depends(Paginate),
    service: BookingService = Depends(get_booking_service),
):
    query = BookingQuery(
        resource_id=resource_id,
        date_start=timeframe.date_start,
        date_end=timeframe.date_end,
    )
    return service.find(query, paginate=paginate)


@router.delete(
    "/{resource_id}/", status_code=HTTPStatus.ACCEPTED, response_class=Response
)
async def delete_resource(
    resource_id: uuid.UUID,
    service: ResourceService = Depends(get_resource_service),
):
    service.delete(resource_id)
