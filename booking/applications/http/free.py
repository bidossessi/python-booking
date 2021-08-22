from fastapi import APIRouter, Depends

from booking.applications.http import models
from booking.domain import services

router = APIRouter()


@router.get("/")
async def find_resources(
    timeframe: models.TimeFrameIn = Depends(models.TimeFrameIn),
    tags: models.TagsParams = Depends(models.TagsParams),
    resource_service: services.ResourceService = Depends(models.get_resource_service),
):
    matches = resource_service.list_free(timeframe, tags.tags)
    return models.ResourceOutPage(items=matches)
