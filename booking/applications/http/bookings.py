import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from booking.applications.http.models import (
    BookingIn,
    BookingOut,
    BookingOutPage,
    BookingParams,
    TimeFrameIn,
    get_booking_service,
)
from booking.domain.repositories import Paginate
from booking.domain.services import BookingService

router = APIRouter()


@router.get("/")
async def find_bookings(
    paginate: Paginate = Depends(Paginate),
    params: BookingParams = Depends(BookingParams),
    service: BookingService = Depends(get_booking_service),
):
    page = service.find(params.to_query(), paginate)
    return BookingOutPage.from_orm(page)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=BookingOut)
async def create_booking(
    booking_in: BookingIn,
    service: BookingService = Depends(get_booking_service),
):
    return service.create(booking_in)


@router.get("/{booking_id}/", response_model=BookingOut)
async def get_resource(
    booking_id: uuid.UUID,
    service: BookingService = Depends(get_booking_service),
):
    return service.get(booking_id)


@router.patch("/{booking_id}/", response_model=BookingOut)
async def patch_booking(
    booking_id: uuid.UUID,
    timeframe: TimeFrameIn,
    service: BookingService = Depends(get_booking_service),
):
    return service.update(booking_id, timeframe)


@router.delete(
    "/{booking_id}/", status_code=HTTPStatus.ACCEPTED, response_class=Response
)
async def delete_resource(
    booking_id: uuid.UUID,
    service: BookingService = Depends(get_booking_service),
):
    service.delete(booking_id)
