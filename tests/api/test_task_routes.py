import pytest

@pytest.mark.asyncio
async def test_create_get_list_delete(client, task_payload):
    r = await client.post("/tasks/", json=task_payload)
    assert r.status_code == 201, r.text
    data = r.json()
    task_id = data["id"]
    assert data["title"] == task_payload["title"]

    r = await client.get(f"/tasks/{task_id}")
    assert r.status_code == 200
    assert r.json()["id"] == task_id

    r = await client.get("/tasks/")
    assert r.status_code == 200
    assert any(t["id"] == task_id for t in r.json())

    r = await client.delete(f"/tasks/{task_id}")
    assert r.status_code in (200, 204)

    r = await client.get(f"/tasks/{task_id}")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_update_task(client, task_payload, update_payload):
    r = await client.post("/tasks/", json=task_payload)
    assert r.status_code == 201
    task_id = r.json()["id"]

    r = await client.put(f"/tasks/{task_id}", json=update_payload)
    assert r.status_code == 200
    assert r.json()["title"] == update_payload["title"]
    assert r.json()["description"] == update_payload["description"]

@pytest.mark.asyncio
async def test_create_validation_error(client):
    r = await client.post("/tasks/", json={"title": "   "})
    assert r.status_code == 400

@pytest.mark.asyncio
async def test_change_status(client, task_payload, status_values):
    r = await client.post("/tasks/", json=task_payload)
    assert r.status_code == 201
    task_id = r.json()["id"]

    payload = {"status": "in_work"}  
    r = await client.patch(f"/tasks/{task_id}/status", json=payload)
    assert r.status_code == 200, r.text

    body = r.json()
    assert body.get("status") in (
        status_values["in_work"],  
        "in_work", "В работе"
    )
    sd = body.get("status_display")
    if sd is not None:
        assert sd in ("В работе", "Создана", "Завершена")