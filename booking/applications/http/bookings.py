import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from booking.applications.http import models
from booking.domain import services

router = APIRouter()


@router.get("/")
async def find_bookings(
    params: models.BookingParams = Depends(models.BookingParams),
    service: services.BookingService = Depends(models.get_booking_service),
):
    matches = service.find(params.to_query())
    return models.BookingOutPage(items=matches)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=models.BookingOut)
async def create_booking(
    booking_in: models.BookingIn,
    service: services.BookingService = Depends(models.get_booking_service),
):
    return service.create(booking_in)


@router.get("/{booking_id}/", response_model=models.BookingOut)
async def get_booking(
    booking_id: uuid.UUID,
    service: services.BookingService = Depends(models.get_booking_service),
):
    return service.get(booking_id)


@router.patch("/{booking_id}/", response_model=models.BookingOut)
async def patch_booking(
    booking_id: uuid.UUID,
    timeframe: models.TimeFrameIn,
    service: services.BookingService = Depends(models.get_booking_service),
):
    return service.update(booking_id, timeframe)


@router.delete(
    "/{booking_id}/",
    status_code=HTTPStatus.ACCEPTED,
    response_class=Response,
)
async def delete_resource(
    booking_id: uuid.UUID,
    service: services.BookingService = Depends(models.get_booking_service),
):
    service.delete(booking_id)
