import pytest
from ..app import Flask

# Test GET in homepage
def test_homepage():
    flask_app = Flask("flask_test.cfg")
    with flask_app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert b"Crypto Tracker" in response.data

# Test POST in add page
def test_post_add_page():
    flask_app = Flask("flask_test.cfg")
    with flask_app.test_client() as test_client:
        response = test_client.post("/ajouter")
        assert response.status_code == 405
        assert b"Ajouter" not in response.data

