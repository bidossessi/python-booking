from http import HTTPStatus
from booking.applications.http.models import (
    BookingIn,
    BookingOut,
    BookingOutPage,
    BookingParams,
    get_booking_service,
)
from booking.domain.repositories import Paginate
from booking.domain.services import BookingService
from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/")
async def find_resources(
    paginate: Paginate = Depends(Paginate),
    params: BookingParams = Depends(BookingParams),
    service: BookingService = Depends(get_booking_service),
):
    page = service.find(params.to_query(), paginate)
    return BookingOutPage.from_orm(page)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=BookingOut)
async def create_resource(
    booking_in: BookingIn,
    service: BookingService = Depends(get_booking_service),
):
    return service.create(booking_in)
