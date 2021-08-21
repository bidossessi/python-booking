from booking.domain.models import Resource
from booking.data.memory import MemoryResourceRepo
import pytest
import uuid
from fastapi.testclient import TestClient
from booking.application.main import app


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
