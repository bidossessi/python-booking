from http import HTTPStatus
from booking.applications.http.dto import (
    BookingPageDTO,
    BookingParams,
    ResourceDTO,
    ResourcePageDTO,
    ResourceParams,
)
from booking.domain.repositories import Paginate
from booking.data.memory import MemoryBookingRepo
from booking.domain.services import BookingService
import uuid
from fastapi import APIRouter, Depends


router = APIRouter()


async def _get_service() -> BookingService:
    return BookingService(repository=MemoryBookingRepo())


@router.get("/")
async def find_resources(
    paginate: Paginate = Depends(Paginate),
    params: BookingParams = Depends(BookingParams),
    service: BookingService = Depends(_get_service),
):
    page = service.find(params.to_query(), paginate)
    return BookingPageDTO.from_orm(page)
