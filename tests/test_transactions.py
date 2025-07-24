from datetime import datetime


def test_over_limit_transaction_not_persisted(client, db_setup, auth_headers):
    headers = auth_headers()

    # Create a small budget for the current month
    month = datetime.utcnow().strftime("%Y-%m")
    client.post(
        "/budgets/",
        json={"month": month, "limit": 50.55},
        headers=headers,
    )

    # Attempt to record an expense exceeding the limit
    resp = client.post(
        "/transactions/",
        json={"amount": -60.10},
        headers=headers,
    )
    assert resp.status_code == 400

    # Verify no transactions were stored
    list_resp = client.get("/transactions/", headers=headers)
    assert list_resp.status_code == 200
    assert list_resp.json() == []


def test_edit_transaction_budget_enforced(client, db_setup, auth_headers):
    headers = auth_headers()

    month = datetime.utcnow().strftime("%Y-%m")
    client.post(
        "/budgets/",
        json={"month": month, "limit": 50.0},
        headers=headers,
    )

    resp = client.post(
        "/transactions/",
        json={"amount": -30.0},
        headers=headers,
    )
    tx_id = resp.json()["id"]

    update_resp = client.put(
        f"/transactions/{tx_id}",
        json={"amount": -60.0},
        headers=headers,
    )
    assert update_resp.status_code == 400

    tx_list = client.get("/transactions/", headers=headers).json()
    assert tx_list[0]["amount"] == -30.0

    progress = client.get("/rewards/", headers=headers).json()
    assert progress["points"] == 30


def test_points_after_edit(client, db_setup, auth_headers):
    headers = auth_headers()

    resp = client.post(
        "/transactions/",
        json={"amount": 20.0},
        headers=headers,
    )
    tx_id = resp.json()["id"]

    progress = client.get("/rewards/", headers=headers).json()
    assert progress["points"] == 20

    update_resp = client.put(
        f"/transactions/{tx_id}",
        json={"amount": 50.0},
        headers=headers,
    )
    assert update_resp.status_code == 200

    progress = client.get("/rewards/", headers=headers).json()
    assert progress["points"] == 50
