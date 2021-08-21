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
    end = (datetime.date.today() + relativedelta(weeks=2)).isoformat()
    response = client.get(f"/bookings?date_start={start}&date_end={end}")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert "count" in data
    assert data["count"] == 2


def test_list_bookings_with_tag(client):
    start = (datetime.date.today() + relativedelta(weeks=1)).isoformat()
    end = (datetime.date.today() + relativedelta(weeks=2)).isoformat()
    response = client.get(f"/bookings?date_start={start}&date_end={end}&tags=b")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert "count" in data
    assert data["count"] == 1
