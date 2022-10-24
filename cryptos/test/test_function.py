import os
from sqlalchemy import select
from ..models import Cryptos

# Patch DB
os.environ["CRYPTOS_DATABASE_URI"] = "sqlite:///testing.db"
db = os.environ["CRYPTOS_DATABASE_URI"]
from ..app import app, engine, db, session
import pudb

# Test GET in homepage
def test_app():
    with app.test_client() as test_client:
        os.environ["CRYPTOS_DATABASE_URI"] = "sqlite:///testing.db"
        print(os.environ["CRYPTOS_DATABASE_URI"])
        response = test_client.get("/")
        print(response)
        assert response.status_code == 200
        assert "<h1>Crypto Tracker</h1>" in response.text

# Test POST in add page
def test_post_add_page():
    with app.test_client() as test_client:
        new_buy_payload = {"name":"BTC", "quantity":0.0555, "cost":15555.5}
        response = test_client.post("/ajouter", data=new_buy_payload)
        assert response.status_code == 200
        assert "<h2>Ajouter une transaction</h2>" in response.text
        assert "a été ajoutée !" in response.text
        result = select(Cryptos).where(Cryptos.name == "BTC", Cryptos.quantity == 2, Cryptos.cost == 5)
        print(result)

# Test POST in remove page
def test_post_remove_page():
    with app.test_client() as test_client:
        new_sell_payload = {"name":"BTC", "quantity":0.0555, "cost":15555.5}
        response = test_client.post("/supprimer", data=new_sell_payload)
        assert response.status_code == 200
        assert "<h2>Supprimer un montant</h2>" in response.text
        assert "a été retirée !" in response.text
        result = select(Cryptos).where(Cryptos.name == "BTC", Cryptos.quantity == 2, Cryptos.cost == 5)
        print(result)