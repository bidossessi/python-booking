from booking.application.dto import ResourceDTO, ResourcePageDTO, ResourceParams
from booking.domain.repositories import Paginate, ResourceQuery
from booking.data.memory import MemoryResourceRepo
from booking.domain.services import ResourceService
from typing import List, Optional
import uuid
from fastapi import FastAPI, Depends, Query


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def _get_resource_service() -> ResourceService:
    return ResourceService(repository=MemoryResourceRepo())


@app.get("/resources")
async def find_resources(
    service: ResourceService = Depends(_get_resource_service),
    paginate: Paginate = Depends(Paginate),
    query: ResourceParams = Depends(ResourceParams),
):
    print(query)
    print(paginate)
    page = service.find(query.to_query(), paginate)
    return ResourcePageDTO.from_orm(page)
