#from datetime import datetime
#import pytest
#import os
#from ..models import Cryptos
#
## Patch DB
#os.environ["CRYPTOS_DATABASE_URI"] = "sqlite:///testing.db"
#db = os.environ["CRYPTOS_DATABASE_URI"]
#from ..app import app, engine, db, session
#
## Test GET in homepage
#def test_app():
#    with app.test_client() as test_client:
#        os.environ["CRYPTOS_DATABASE_URI"] = "sqlite:///testing.db"
#        print(os.environ["CRYPTOS_DATABASE_URI"])
#        app = app.test_client()
#
#    response = app.get("/")
#    assert response.status_code == 200
#    assert "<h1>Crypto Tracker</h1>" in response.data
#
## Test POST in add page
#def test_post_add_page():
#    with app.test_client() as test_client:
#        response = test_client.post("/ajouter")
#        assert response.status_code == 200
#        assert "<h2>Ajouter une transaction</h2>" in response.data
#
#def test_models():
#    crypto = Cryptos("Bitcoin", 0.003, 10000, datetime.utcnow)
#    db.session.add(crypto)
#    db.session.commit()
#    #Check that all users exist
#    assert len(Cryptos.query.all()) != 0