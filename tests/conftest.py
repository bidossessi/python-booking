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
    today = datetime.datetime.today()
    tuples = [
        (
            r.id,
            today + relativedelta(weeks=count + 1),
            today + relativedelta(months=count + 1),
            r.tags,
        )
        for count, r in enumerate(resource_repo.store)
    ]
    items = [
        Booking(
            id=uuid.uuid4(),
            order_id=uuid.uuid4().hex,
            resource_id=id,
            date_start=start,
            date_end=end,
            tags=tags,
        )
        for id, start, end, tags in tuples
    ]
    for item in items:
        repo.save(item)

    return repo


@pytest.fixture(scope="function")
def resource(resource_repo):
    return resource_repo.store[0]


@pytest.fixture(scope="function")
def booking(booking_repo):
    return booking_repo.store[0]
