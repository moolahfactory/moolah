
def test_get_current_user(client, db_setup):
    # Register a new user
    resp = client.post(
        "/users/",
        json={"email": "me@example.com", "password": "secret"},
    )
    assert resp.status_code == 200

    # Obtain an access token
    token_resp = client.post(
        "/token",
        data={"username": "me@example.com", "password": "secret"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Call the /users/me/ endpoint
    me_resp = client.get("/users/me/", headers=headers)
    assert me_resp.status_code == 200
    data = me_resp.json()

    assert data["email"] == "me@example.com"
    assert data["is_admin"] is False
    assert data["is_active"] is True
    assert data["points"] == 0
