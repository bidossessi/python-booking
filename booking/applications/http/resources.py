from http import HTTPStatus
from booking.applications.http.dto import (
    ResourceDTO,
    ResourcePageDTO,
    ResourceParams,
    TagsDTO,
)
from booking.domain.repositories import Paginate
from booking.data.memory import MemoryResourceRepo
from booking.domain.services import ResourceService
import uuid
from fastapi import APIRouter, Depends


router = APIRouter()


async def _get_service() -> ResourceService:
    return ResourceService(repository=MemoryResourceRepo())


@router.get("/", response_model=ResourcePageDTO)
async def find_resources(
    paginate: Paginate = Depends(Paginate),
    params: ResourceParams = Depends(ResourceParams),
    service: ResourceService = Depends(_get_service),
):
    return service.find(params.to_query(), paginate)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=ResourceDTO)
async def create_resource(
    dto: ResourceDTO,
    service: ResourceService = Depends(_get_service),
):
    return service.create(dto)


@router.get("/{resource_id}/", response_model=ResourceDTO)
async def get_resource(
    resource_id: uuid.UUID,
    service: ResourceService = Depends(_get_service),
):
    return service.get(resource_id)


@router.patch(
    "/{resource_id}/", status_code=HTTPStatus.ACCEPTED, response_model=ResourceDTO
)
async def patch_resource(
    resource_id: uuid.UUID,
    dto: TagsDTO,
    service: ResourceService = Depends(_get_service),
):
    return service.update_tags(resource_id, dto.tags)
