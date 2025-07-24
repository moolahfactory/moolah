from datetime import datetime

from app.database import SessionLocal
from app import models


def _set_timestamp(tx_id: int, ts: datetime):
    db = SessionLocal()
    tx = db.get(models.Transaction, tx_id)
    tx.timestamp = ts
    db.commit()
    db.close()


def test_monthly_summary(client, db_setup, auth_headers):
    headers = auth_headers(is_admin=True)

    resp1 = client.post("/transactions/", json={"amount": 10.10}, headers=headers)
    resp2 = client.post("/transactions/", json={"amount": 20.20}, headers=headers)
    resp3 = client.post("/transactions/", json={"amount": 5.50}, headers=headers)

    _set_timestamp(resp1.json()["id"], datetime(2023, 1, 15))
    _set_timestamp(resp2.json()["id"], datetime(2023, 1, 20))
    _set_timestamp(resp3.json()["id"], datetime(2023, 2, 10))

    resp = client.get("/summary/monthly", headers=headers)
    assert resp.status_code == 200

    data = sorted(resp.json(), key=lambda x: x["month"])
    assert data == [
        {"month": "2023-01", "total": 30.3},
        {"month": "2023-02", "total": 5.5},
    ]


def test_category_summary(client, db_setup, auth_headers):
    headers = auth_headers(is_admin=True)

    cat1 = client.post("/categories/", json={"name": "Food"}, headers=headers).json()
    cat2 = client.post("/categories/", json={"name": "Travel"}, headers=headers).json()

    client.post(
        "/transactions/",
        json={"amount": 10.25, "category_id": cat1["id"]},
        headers=headers,
    )
    client.post(
        "/transactions/",
        json={"amount": 5.05, "category_id": cat2["id"]},
        headers=headers,
    )
    client.post("/transactions/", json={"amount": 7.70}, headers=headers)

    resp = client.get("/summary/category", headers=headers)
    assert resp.status_code == 200

    data = {item["category"]: item["total"] for item in resp.json()}
    assert data == {
        "Food": 10.25,
        "Travel": 5.05,
        "Uncategorized": 7.7,
    }
