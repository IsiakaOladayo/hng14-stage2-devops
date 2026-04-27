from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch

client = TestClient(app)


@patch("api.main.r")
def test_create_job(mock_redis):
    mock_redis.lpush.return_value = True
    mock_redis.hset.return_value = True

    res = client.post("/jobs")
    assert res.status_code == 200


@patch("api.main.r")
def test_get_job_not_found(mock_redis):
    mock_redis.hget.return_value = None

    res = client.get("/jobs/123")
    assert res.status_code == 404


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
