from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from booking.applications.http.bookings import router as booking_router
from booking.applications.http.resources import router as resource_router
from booking.applications.http.free import router as free_router
from booking.domain.errors import (
    BookingConflict,
    BookingNotFound,
    ResourceConflict,
    ResourceNotFound,
)

app = FastAPI(default_response_class=JSONResponse)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.exception_handler(ResourceNotFound)
async def resource_not_found_handler(request: Request, exc: ResourceNotFound):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(BookingNotFound)
async def booking_not_foud_handler(request: Request, exc: BookingNotFound):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(ResourceConflict)
async def resource_conflict_handler(request: Request, exc: ResourceConflict):
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(BookingConflict)
async def booking_conflict_handler(request: Request, exc: BookingConflict):
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content={"detail": str(exc)},
    )


app.include_router(resource_router, prefix="/resources", tags=["resources"])
app.include_router(booking_router, prefix="/bookings", tags=["bookings"])
app.include_router(free_router, prefix="/free", tags=["free"])
