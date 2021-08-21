def test_list_resources(client):
    response = client.get("/resources")
    data = response.json()

    assert response.status_code == 200
    assert "count" in data
    assert data["count"] == 3


def test_list_resources_by_tag(client):
    response = client.get("/resources?per_page=20&tags=a,b")
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert "count" in data
    assert data["count"] == 2
