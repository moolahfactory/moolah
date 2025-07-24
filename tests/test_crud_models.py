def test_category_crud(client, db_setup, auth_headers):
    admin_headers = auth_headers("admin@example.com", is_admin=True)
    user_headers = auth_headers("user2@example.com")

    resp = client.post("/categories/", json={"name": "Food"}, headers=admin_headers)
    assert resp.status_code == 200
    cat_id = resp.json()["id"]
    assert resp.json()["name"] == "Food"

    resp = client.get("/categories/", headers=admin_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.put(
        f"/categories/{cat_id}",
        json={"name": "Groceries"},
        headers=admin_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Groceries"

    resp = client.delete(f"/categories/{cat_id}", headers=admin_headers)
    assert resp.status_code == 200

    resp = client.get("/categories/", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json() == []

    # non-admin cannot modify categories
    resp = client.post("/categories/", json={"name": "Other"}, headers=user_headers)
    assert resp.status_code == 403
    resp = client.put(
        f"/categories/{cat_id}", json={"name": "X"}, headers=user_headers
    )
    assert resp.status_code == 403
    resp = client.delete(f"/categories/{cat_id}", headers=user_headers)
    assert resp.status_code == 403


def test_budget_crud(client, db_setup, auth_headers):
    headers = auth_headers()

    resp = client.post("/budgets/", json={"month": "2023-01", "limit": 100.50}, headers=headers)
    assert resp.status_code == 200
    budget_id = resp.json()["id"]
    assert resp.json()["month"] == "2023-01"

    resp = client.get("/budgets/", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.put(f"/budgets/{budget_id}", json={"limit": 150.75}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["limit"] == 150.75

    resp = client.delete(f"/budgets/{budget_id}", headers=headers)
    assert resp.status_code == 200

    resp = client.get("/budgets/", headers=headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_budget_unique_constraint(client, db_setup, auth_headers):
    headers = auth_headers()

    data = {"month": "2023-01", "limit": 50.0}
    resp1 = client.post("/budgets/", json=data, headers=headers)
    assert resp1.status_code == 200

    resp2 = client.post("/budgets/", json=data, headers=headers)
    assert resp2.status_code == 400


def test_budget_invalid_month(client, db_setup, auth_headers):
    headers = auth_headers()

    resp = client.post(
        "/budgets/",
        json={"month": "2023-13", "limit": 10.0},
        headers=headers,
    )
    assert resp.status_code == 422

    resp = client.post(
        "/budgets/",
        json={"month": "2023-01", "limit": 10.0},
        headers=headers,
    )
    budget_id = resp.json()["id"]

    update_resp = client.put(
        f"/budgets/{budget_id}",
        json={"month": "bad-format"},
        headers=headers,
    )
    assert update_resp.status_code == 422


def test_budget_negative_limit(client, db_setup, auth_headers):
    headers = auth_headers()

    resp = client.post(
        "/budgets/",
        json={"month": "2023-01", "limit": -1.0},
        headers=headers,
    )
    assert resp.status_code == 422

    resp = client.post(
        "/budgets/",
        json={"month": "2023-01", "limit": 10.0},
        headers=headers,
    )
    budget_id = resp.json()["id"]

    update_resp = client.put(
        f"/budgets/{budget_id}",
        json={"limit": -5.0},
        headers=headers,
    )
    assert update_resp.status_code == 422


def test_goal_crud_and_complete(client, db_setup, auth_headers):
    headers = auth_headers()

    resp = client.post(
        "/goals/",
        json={"description": "Save", "target_amount": 60.25},
        headers=headers,
    )
    assert resp.status_code == 200
    goal_id = resp.json()["id"]

    resp = client.get("/goals/", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.put(f"/goals/{goal_id}", json={"target_amount": 80.50}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["target_amount"] == 80.50

    resp = client.patch(f"/goals/{goal_id}/complete", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["points"] == 80
    assert data["rewards"] == []

    resp = client.delete(f"/goals/{goal_id}", headers=headers)
    assert resp.status_code == 200

    resp = client.get("/goals/", headers=headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_rewards_after_transactions(client, db_setup, auth_headers):
    headers = auth_headers()

    client.post("/transactions/", json={"amount": 120.30}, headers=headers)

    resp = client.get("/rewards/", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["points"] == 120
    assert any(reward["level"] == "Bronze" for reward in data["rewards"])


def test_reward_after_goal_completion(client, db_setup, auth_headers):
    headers = auth_headers()

    resp = client.post(
        "/goals/",
        json={"description": "Big", "target_amount": 120.0},
        headers=headers,
    )
    goal_id = resp.json()["id"]

    complete = client.patch(f"/goals/{goal_id}/complete", headers=headers)
    assert complete.status_code == 200

    progress = client.get("/rewards/", headers=headers).json()
    assert progress["points"] == 120
    assert any(r["level"] == "Bronze" for r in progress["rewards"])
