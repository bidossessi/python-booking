import datetime
from dateutil.relativedelta import relativedelta, MO
from booking.domain.models import Booking, Resource
from booking.data.memory import MemoryBookingRepo, MemoryResourceRepo
import pytest
import uuid
from fastapi.testclient import TestClient
from booking.applications.http import app


@pytest.fixture(scope="function")
def client():
    return TestClient(app, base_url="http://localhost")


@pytest.fixture(scope="session", autouse=True)
def resource_repo():
    repo = MemoryResourceRepo()
    items = [
        Resource(id=uuid.uuid4(), tags=["a", "b"]),
        Resource(id=uuid.uuid4(), tags=["b", "c"]),
        Resource(id=uuid.uuid4(), tags=["c", "d"]),
    ]
    for item in items:
        repo.save(item)

    return repo


@pytest.fixture(scope="session", autouse=True)
def booking_repo(resource_repo):
    repo = MemoryBookingRepo()
    items = [
        Booking(
            order_id=uuid.uuid4().hex,
            resource_id=r.id,
            date_start=(datetime.datetime.now() + relativedelta(days=count)),
            date_end=(datetime.datetime.now() + relativedelta(months=count)),
            tags=r.tags,
        )
        for count, r in enumerate(resource_repo.store)
    ]
    for item in items:
        repo.save(item)

    return repo


@pytest.fixture(scope="function")
def resource(resource_repo):
    return resource_repo.store[0]
