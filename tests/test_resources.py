import datetime
import uuid
from http import HTTPStatus

from dateutil.relativedelta import relativedelta


def test_list_resources(client):
    response = client.get("/resources/")
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "count" in data
    assert data["count"] == 3
    assert len(data["items"]) == 3


def test_list_resources_by_tag(client):
    response = client.get("/resources/?tags=a,b")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "count" in data
    assert data["count"] == 2


def test_list_resources_by_id_no_match(client, resource):
    response = client.get(f"/resources/?resource_id={uuid.uuid4()}")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "count" in data
    assert data["count"] == 0


def test_list_resources_by_id_invalid(client, resource):
    response = client.get("/resources/?resource_id=not-a-uuid")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_list_resources_by_id(client, resource):
    response = client.get(f"/resources/?resource_id={resource.id}")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "count" in data
    assert data["count"] == 1


def test_create_resource(client):
    response = client.post(
        "/resources/", json={"id": uuid.uuid4().hex, "tags": ["y", "z"]}
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.get("/resources/")
    data = response.json()
    assert "count" in data
    assert data["count"] == 4


def test_get_resource(client, resource):
    response = client.get(f"/resources/{resource.id}/")
    assert response.status_code == HTTPStatus.OK


def test_get_resource_not_found(client):
    response = client.get(f"/resources/{uuid.uuid4()}/")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_resource_invalid(client):
    response = client.get("/resources/not-a-uuid/")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_tag(client, resource):
    tags = ["h", "k"]
    response = client.patch(f"/resources/{resource.id}/", json={"tags": tags})
    assert response.status_code == HTTPStatus.OK

    response = client.get(f"/resources/{resource.id}/")
    data = response.json()
    assert data["tags"] == tags


def test_get_resource_bookings(client, resource):
    start = (datetime.date.today() + relativedelta(weeks=1)).isoformat()
    end = (datetime.date.today() + relativedelta(weeks=3)).isoformat()
    response = client.get(
        f"/resources/{resource.id}/bookings/?date_start={start}&date_end={end}"
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "count" in data
    assert data["count"] == 1


def test_delete_resource_invalid(client):
    response = client.delete("/resources/not-a-uuid/")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_delete_resource_not_found(client):
    response = client.delete(f"/resources/{uuid.uuid4()}/")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_resource_conflict(client, resource):
    response = client.delete(f"/resources/{resource.id}/")
    assert response.status_code == HTTPStatus.CONFLICT


def test_delete_resource(client, last_resource):
    response = client.delete(f"/resources/{last_resource.id}/")
    assert response.status_code == HTTPStatus.ACCEPTED
