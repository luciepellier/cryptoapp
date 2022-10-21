#from sqlalchemy import null
#from ..controllers import coin_id_dict, get_coin_price, get_coin_change, get_coin_name
#from ..models import Cryptos
#from ..app import app
#from datetime import datetime
#import pytest
#import os
#
## Patch DB
#os.environ["CRYPTOS_DATABASE_URI"] = "sqlite:///testing.db"
#db = os.environ["CRYPTOS_DATABASE_URI"]
#from ..app import app, engine, db, session
#
## test coin prices are returned and not null
#def test_should_get_coin_price():
#    assert get_coin_price("BTC") and get_coin_price("ETH") and get_coin_price("XRP") > 0, "Coin prices should be superior than zero"
#
## test coin changes are returned and different from zero
#def test_should_get_coin_change():
#    assert get_coin_change("BTC") and get_coin_change("ETH") and get_coin_change("XRP") != 0, "Coin evolution should be different from zero"
#
## test coin names matching with symbol = bitcoin, eth or xrp
#def test_should_get_coin_name():
#    assert get_coin_name("BTC") == "Bitcoin", "Bitcoin name should match with the coin symbol"
#    assert get_coin_name("ETH") == "Ethereum", "Ethereum name should match with the coin symbol"
#    assert get_coin_name("XRP") == "XRP", "XRP name should match with the coin symbol"
#
## test db model
#def test_db_model():
#    new_crypto = Cryptos(name="Bitcoin", quantity=0.005, cost=12000, date_added=datetime.utcnow)
#    assert new_crypto.name == "Bitcoin", "Crypto's name doesn't match with DB model"
#    assert new_crypto.quantity == 0.005, "Crypto's quantity doesn't match with DB model"
#    assert new_crypto.cost == 12000, "Crypto's cost doesn't match with DB model"
#
#