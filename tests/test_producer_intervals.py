from fastapi.testclient import TestClient
from movies import app

def test_producer_intervals_exact():
    with TestClient(app) as client:
        response = client.get("/producers/intervals")
        assert response.status_code == 200
        data = response.json()

        expected_min = {
            "producer": "Joel Silver",
            "interval": 1,
            "previousWin": 1990,
            "followingWin": 1991
        }

        expected_max = {
            "producer": "Matthew Vaughn",
            "interval": 13,
            "previousWin": 2002,
            "followingWin": 2015
        }

        assert expected_min in data["min"]
        assert expected_max in data["max"]
