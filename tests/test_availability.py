import datetime
from http import HTTPStatus

from dateutil.relativedelta import relativedelta


def test_free_no_date_fails(client):
    response = client.get("/free/")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_list_free_resources(client, resource):
    start = datetime.date.today().isoformat()
    start_2 = (datetime.date.today() + relativedelta(months=2)).isoformat()
    end_3 = (datetime.date.today() + relativedelta(months=3)).isoformat()
    end_12 = (datetime.date.today() + relativedelta(months=12)).isoformat()
    response = client.get(f"/free/?date_start={start_2}&date_end={end_3}")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "count" in data
    assert data["count"] == 2

    for match in data["items"]:
        resource_id = match["resource_id"]
        reference = str(resource.resource_id)
        is_first_resource = resource_id == reference
        response = client.get(
            f"/bookings/?resource_id={resource_id}&date_start={start}&date_end={end_12}"
        )
        b_data = response.json()
        if is_first_resource:
            # The first resource has 3 bookings
            # It just happens to be free for when we need it.
            assert b_data["count"] == 3
        else:
            assert b_data["count"] == 0
