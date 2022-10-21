import pytest
import os

# Patch DB
os.environ["CRYPTOS_DATABASE_URI"] = "sqlite:///testing.db"
from ..app import app



# Test GET in homepage
def test_homepage():
    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert b"Crypto Tracker" in response.data

# Test POST in add page
def test_post_add_page():
    with app.test_client() as test_client:
        response = test_client.post("/ajouter")
        assert response.status_code == 405
        assert b"Ajouter" not in response.data


