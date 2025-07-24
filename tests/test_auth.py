

def test_create_user_ignores_is_admin_flag(client, db_setup):
    resp = client.post(
        "/users/",
        json={"email": "admin@example.com", "password": "secret", "is_admin": True},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "admin@example.com"
    assert data["is_admin"] is False


def test_token_wrong_credentials_returns_401(client, db_setup):
    # Create a valid user first
    client.post(
        "/users/",
        json={"email": "user@example.com", "password": "secret"},
    )

    resp = client.post(
        "/token",
        data={"username": "user@example.com", "password": "wrong"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 401


def test_users_me_requires_authorization(client, db_setup):
    resp = client.get("/users/me/")
    assert resp.status_code == 401
