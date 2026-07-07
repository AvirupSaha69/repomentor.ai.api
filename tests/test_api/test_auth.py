import uuid
import pytest
from fastapi.testclient import TestClient

def get_random_email() -> str:
    return f"user_{uuid.uuid4().hex[:8]}@example.com"

def test_register_user_success(client: TestClient):
    """Test that a new user can be registered successfully."""
    email = get_random_email()
    payload = {
        "email": email,
        "full_name": "Arijit Roy",
        "password": "securepassword123"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == email
    assert data["full_name"] == "Arijit Roy"
    assert "_id" in data
    assert "password" not in data
    assert "hashed_password" not in data

def test_register_user_duplicate(client: TestClient):
    """Test registering the same email twice returns 400 Bad Request."""
    email = get_random_email()
    payload = {
        "email": email,
        "full_name": "Arijit Roy",
        "password": "securepassword123"
    }
    
    # First registration
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    
    # Duplicate registration
    response2 = client.post("/api/v1/auth/register", json=payload)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]

def test_signin_success(client: TestClient):
    """Test that an existing user can sign in and receive a JWT token."""
    email = get_random_email()
    password = "secretpassword"
    
    # Register the user
    register_payload = {
        "email": email,
        "full_name": "Arijit Roy",
        "password": password
    }
    register_response = client.post("/api/v1/auth/register", json=register_payload)
    assert register_response.status_code == 201
    
    # Sign in
    signin_payload = {
        "email": email,
        "password": password
    }
    response = client.post("/api/v1/auth/signin", json=signin_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_signin_invalid_credentials(client: TestClient):
    """Test that signing in with invalid credentials returns 401 Unauthorized."""
    email = get_random_email()
    
    # Test signin with non-existing user
    signin_payload = {
        "email": email,
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/signin", json=signin_payload)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]
