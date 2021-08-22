import datetime
import uuid
from http import HTTPStatus

from dateutil.relativedelta import relativedelta


def test_list_bookings_no_date_fails(client):
    response = client.get("/bookings")
    data = response.json()

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_list_bookings(client):
    start = (datetime.date.today() + relativedelta(weeks=1)).isoformat()
    end = (datetime.date.today() + relativedelta(weeks=3)).isoformat()
    response = client.get(f"/bookings?date_start={start}&date_end={end}")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert "count" in data
    assert data["count"] == 2


def test_list_bookings_with_tag(client):
    start = (datetime.date.today() + relativedelta(weeks=2)).isoformat()
    end = (datetime.date.today() + relativedelta(weeks=3)).isoformat()
    response = client.get(f"/bookings?date_start={start}&date_end={end}&tags=c")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "count" in data
    assert data["count"] == 1


def test_create_booking_starts_in_the_past_fails(client, resource):
    response = client.post(
        "/bookings/",
        json={
            "resource_id": resource.id.hex,
            "order_id": "ABCDEFG",
            "date_start": (datetime.date.today() - relativedelta(weeks=1)).isoformat(),
            "date_end": (datetime.date.today() + relativedelta(weeks=1)).isoformat(),
        },
    )
    data = response.json()
    assert data == {
        "detail": [
            {
                "loc": ["body", "date_start"],
                "msg": "Invalid start date",
                "type": "value_error",
            }
        ]
    }
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_booking_ends_before_start_fails(client, resource):
    response = client.post(
        "/bookings/",
        json={
            "resource_id": resource.id.hex,
            "order_id": "ABCDEFG",
            "date_start": (datetime.date.today() + relativedelta(weeks=1)).isoformat(),
            "date_end": (datetime.date.today() - relativedelta(weeks=1)).isoformat(),
        },
    )
    data = response.json()
    assert data == {
        "detail": [
            {
                "loc": ["body", "date_end"],
                "msg": "Invalid end date",
                "type": "value_error",
            }
        ]
    }
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_booking_ends_conflict_fails(client, resource):
    today = datetime.date.today()
    response = client.post(
        "/bookings/",
        json={
            "resource_id": resource.id.hex,
            "order_id": "ABCDEFG",
            "date_start": (today + relativedelta(weeks=1)).isoformat(),
            "date_end": (today + relativedelta(weeks=4)).isoformat(),
        },
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT


def test_create_booking(client, resource):
    today = datetime.date.today()
    response = client.post(
        "/bookings/",
        json={
            "resource_id": resource.id.hex,
            "order_id": "ABCDEFG",
            "date_start": (today + relativedelta(weeks=7)).isoformat(),
            "date_end": (today + relativedelta(weeks=8)).isoformat(),
        },
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED


def test_get_resource(client, booking):
    response = client.get(f"/bookings/{booking.id}/")
    assert response.status_code == HTTPStatus.OK


def test_get_resource_not_found(client):
    response = client.get(f"/bookings/{uuid.uuid4()}/")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_resource_invalid(client):
    response = client.get("/bookings/not-a-uuid/")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_booking_invalid_fails(client):
    today = datetime.date.today()
    response = client.patch(
        f"/bookings/not-a-uuid/",
        json={
            "date_start": (today + relativedelta(weeks=1)).isoformat(),
            "date_end": (today + relativedelta(weeks=4)).isoformat(),
        },
    )
    data = response.json()
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_booking_not_found_fails(client):
    today = datetime.date.today()
    response = client.patch(
        f"/bookings/{uuid.uuid4().hex}/",
        json={
            "date_start": (today + relativedelta(weeks=1)).isoformat(),
            "date_end": (today + relativedelta(weeks=4)).isoformat(),
        },
    )
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_booking_not_dates_fails(client, booking):
    today = datetime.date.today()
    response = client.patch(
        f"/bookings/{booking.id}/",
        json={
            "date_start": (today + relativedelta(weeks=1)).isoformat(),
        },
    )
    data = response.json()
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_booking_conflict_fails(client, booking):
    today = datetime.date.today()
    response = client.patch(
        f"/bookings/{booking.id}/",
        json={
            "date_start": (today + relativedelta(weeks=1)).isoformat(),
            "date_end": (today + relativedelta(weeks=4)).isoformat(),
        },
    )
    data = response.json()
    print(data)
    assert response.status_code == HTTPStatus.CONFLICT
