from booking.domain.errors import ResourceNotFound
from http import HTTPStatus
from fastapi import FastAPI, requests
from fastapi.responses import JSONResponse
from booking.applications.http.resources import router as resource_router
from booking.applications.http.bookings import router as booking_router

app = FastAPI(default_response_class=JSONResponse)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.exception_handler(ResourceNotFound)
async def version_exception_handler(request: requests, exc: ResourceNotFound):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"detail": str(exc)},
    )


app.include_router(resource_router, prefix="/resources", tags=["resources"])
app.include_router(booking_router, prefix="/bookings", tags=["bookings"])
