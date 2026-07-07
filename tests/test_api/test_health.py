def test_health_check(client):
    """Test that the health check endpoint returns 200 and correct status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "api_version" in response.json()
