import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from booking.applications.http import models
from booking.domain import services

router = APIRouter()


@router.get("/")
async def find_resources(
    params: models.ResourceParams = Depends(models.ResourceParams),
    service: services.ResourceService = Depends(models.get_resource_service),
):
    matches = service.find(params.to_query())
    return models.ResourceOutPage(items=matches)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=models.ResourceOut)
async def create_resource(
    dao: models.ResourceIn,
    service: services.ResourceService = Depends(models.get_resource_service),
):
    return service.create(dao)


@router.get("/{resource_id}/", response_model=models.ResourceOut)
async def get_resource(
    resource_id: uuid.UUID,
    service: services.ResourceService = Depends(models.get_resource_service),
):
    return service.get(resource_id)


@router.patch("/{resource_id}/", response_model=models.ResourceOut)
async def patch_resource(
    resource_id: uuid.UUID,
    dto: models.TagsIn,
    service: services.ResourceService = Depends(models.get_resource_service),
):
    return service.update(resource_id, dto.tags)


@router.get("/{resource_id}/bookings")
async def get_resource_bookings(
    resource_id: uuid.UUID,
    timeframe: models.TimeFrameIn = Depends(models.TimeFrameIn),
    service: services.ResourceService = Depends(models.get_resource_service),
):
    matches = service.find_bookings_for(resource_id, timeframe)
    return models.BookingOutPage(items=matches)


@router.delete(
    "/{resource_id}/", status_code=HTTPStatus.ACCEPTED, response_class=Response
)
async def delete_resource(
    resource_id: uuid.UUID,
    service: services.ResourceService = Depends(models.get_resource_service),
):
    service.delete(resource_id)
