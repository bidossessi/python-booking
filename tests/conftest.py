from booking.helpers import flatten_list
import datetime
from dateutil.relativedelta import relativedelta
from booking.domain.models import Booking, Resource
from booking.data.memory import MemoryRepository
import pytest
import uuid
from fastapi.testclient import TestClient
from booking.applications.http import app


@pytest.fixture(scope="function")
def client():
    return TestClient(app, base_url="http://localhost")


@pytest.fixture(scope="session", autouse=True)
def repository():
    repo = MemoryRepository()
    items = [
        Resource(reference_id=str(uuid.uuid4()), tags=["a", "b"]),
        Resource(reference_id=str(uuid.uuid4()), tags=["b", "c"]),
        Resource(reference_id=str(uuid.uuid4()), tags=["c", "d"]),
        Resource(reference_id=str(uuid.uuid4()), tags=[]),
    ]
    for item in items:
        repo.create_resource(item)

    today = datetime.datetime.today()
    tuples = [
        [
            (r.resource_id, count, count + 1, r.tags),
            (r.resource_id, count + 4, count + 5, r.tags),
            (r.resource_id, count + 9, count + 10, r.tags),
        ]
        for count, r in enumerate(items)
        if r.tags
    ]
    tuples = flatten_list(tuples)
    items = [
        Booking(
            order_id=str(uuid.uuid4()),
            resource_id=item_id,
            date_start=today + relativedelta(months=start),
            date_end=today + relativedelta(months=end),
            tags=tags,
        )
        for item_id, start, end, tags in tuples
    ]
    for item in items:
        repo.create_booking(item)

    return repo


@pytest.fixture(scope="function")
def resource(repository):
    return repository.resource_store[0]


@pytest.fixture(scope="function")
def last_resource(repository):
    return repository.resource_store[-1]


@pytest.fixture(scope="function")
def booking(repository):
    return repository.booking_store[0]


@pytest.fixture(scope="function")
def last_booking(repository):
    return repository.booking_store[-1]
