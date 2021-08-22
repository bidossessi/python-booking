import datetime
import uuid
from http import HTTPStatus

from dateutil.relativedelta import relativedelta


def test_list_bookings_no_date_fails(client):
    response = client.get("/bookings/")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_list_bookings(client):
    start = (datetime.date.today()).isoformat()
    end = (datetime.date.today() + relativedelta(months=6)).isoformat()
    response = client.get(f"/bookings/?date_start={start}&date_end={end}")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "count" in data
    assert data["count"] == 5


def test_list_bookings_with_tag(client):
    start = (datetime.date.today()).isoformat()
    end = (datetime.date.today() + relativedelta(months=3)).isoformat()
    response = client.get(f"/bookings/?date_start={start}&date_end={end}&tags=b")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "count" in data
    assert data["count"] == 2


def test_get_bookings_with_resource(client, resource):
    start = (datetime.date.today()).isoformat()
    end = (datetime.date.today() + relativedelta(months=12)).isoformat()
    response = client.get(
        f"/bookings/?resource_id={resource.resource_id}&date_start={start}&date_end={end}"
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "count" in data
    assert data["count"] == 3


def test_create_booking_starts_in_the_past_fails(client, resource):
    response = client.post(
        "/bookings/",
        json={
            "resource_id": resource.resource_id.hex,
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
            "resource_id": resource.resource_id.hex,
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
            "resource_id": resource.resource_id.hex,
            "order_id": "ABCDEFG",
            "date_start": (today + relativedelta(weeks=1)).isoformat(),
            "date_end": (today + relativedelta(weeks=4)).isoformat(),
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_create_booking(client, resource):
    today = datetime.date.today()
    response = client.post(
        "/bookings/",
        json={
            "resource_id": resource.resource_id.hex,
            "order_id": "ABCDEFG",
            "date_start": (today + relativedelta(weeks=7)).isoformat(),
            "date_end": (today + relativedelta(weeks=8)).isoformat(),
        },
    )
    assert response.status_code == HTTPStatus.CREATED


def test_get_resource(client, booking):
    response = client.get(f"/bookings/{booking.booking_id}/")
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
        "/bookings/not-a-uuid/",
        json={
            "date_start": (today + relativedelta(weeks=1)).isoformat(),
            "date_end": (today + relativedelta(weeks=4)).isoformat(),
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_booking_not_found_fails(client):
    today = datetime.date.today()
    response = client.patch(
        f"/bookings/{str(uuid.uuid4())}/",
        json={
            "date_start": (today + relativedelta(weeks=1)).isoformat(),
            "date_end": (today + relativedelta(weeks=4)).isoformat(),
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_booking_not_dates_fails(client, booking):
    today = datetime.date.today()
    response = client.patch(
        f"/bookings/{booking.booking_id}/",
        json={
            "date_start": (today + relativedelta(weeks=1)).isoformat(),
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_booking_conflict_fails(client, booking):
    today = datetime.date.today()
    response = client.patch(
        f"/bookings/{booking.booking_id}/",
        json={
            "date_start": (today + relativedelta(weeks=1)).isoformat(),
            "date_end": (today + relativedelta(weeks=19)).isoformat(),
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_update_booking(client, last_booking):
    today = datetime.date.today()
    response = client.patch(
        f"/bookings/{last_booking.booking_id}/",
        json={
            "date_start": (today + relativedelta(year=1)).isoformat(),
            "date_end": (today + relativedelta(year=3)).isoformat(),
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_delete_resource_invalid(client):
    response = client.delete("/bookings/not-a-uuid/")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_delete_resource(client, last_booking):
    response = client.delete(f"/bookings/{last_booking.booking_id}/")
    assert response.status_code == HTTPStatus.ACCEPTED
