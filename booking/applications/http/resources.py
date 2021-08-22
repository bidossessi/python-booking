from http import HTTPStatus
from booking.applications.http.models import (
    BookingOutPage,
    ResourceIn,
    ResourceOut,
    ResourceOutPage,
    ResourceParams,
    TagsIn,
    get_resource_service,
)
from booking.domain.repositories import Paginate
from booking.domain.services import ResourceService
import uuid
from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/", response_model=ResourceOutPage)
async def find_resources(
    paginate: Paginate = Depends(Paginate),
    params: ResourceParams = Depends(ResourceParams),
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


@router.patch(
    "/{resource_id}/", status_code=HTTPStatus.ACCEPTED, response_model=ResourceOut
)
async def patch_resource(
    resource_id: uuid.UUID,
    dto: TagsIn,
    service: ResourceService = Depends(get_resource_service),
):
    return service.update(resource_id, dto.tags)


@router.get("/{resource_id}/bookings", response_model=BookingOutPage)
async def get_resource(
    resource_id: uuid.UUID,
    service: ResourceService = Depends(get_resource_service),
):
    return service.get_bookings_for(resource_id)
