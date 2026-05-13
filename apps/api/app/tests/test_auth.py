import uuid
from app.tests.conftest import client, db_conn


def test_register_and_login(client, db_conn):
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    # Register
    response = client.post("/auth/register", json={
        "email": email,
        "password": "testpassword123",
        "full_name": "Test User",
        "role": "ADMIN"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["full_name"] == "Test User"
    assert data["role"] == "ADMIN"

    # Login
    response = client.post("/auth/login", data={
        "username": email,
        "password": "testpassword123"
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Me
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token_data['access_token']}"})
    assert response.status_code == 200
    me_data = response.json()
    assert me_data["email"] == email
    assert "password_hash" not in me_data


def test_login_wrong_password(client, db_conn):
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    client.post("/auth/register", json={
        "email": email,
        "password": "rightpassword",
        "full_name": "Test User",
        "role": "ADMIN"
    })
    response = client.post("/auth/login", data={
        "username": email,
        "password": "wrongpassword"
    })
    assert response.status_code == 401
