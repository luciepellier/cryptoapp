from sqlalchemy import null
from ..controllers import coin_id_dict, get_coin_price, get_coin_change, get_coin_name
from ..models import Cryptos
from ..app import app, db

# test coin prices are returned and not null
def test_should_get_coin_price():
    assert get_coin_price("BTC") and get_coin_price("ETH") and get_coin_price("XRP") > 0, "Coin prices should be superior than zero"

# test coin changes are returned and different from zero
def test_should_get_coin_change():
    assert get_coin_change("BTC") and get_coin_change("ETH") and get_coin_change("XRP") != 0, "Coin evolution should be different from zero"

# test coin names matching with symbol = bitcoin, eth or xrp
def test_should_get_coin_name():
    assert get_coin_name("BTC") == "Bitcoin", "Bitcoin name should match with the coin symbol"
    assert get_coin_name("ETH") == "Ethereum", "Ethereum name should match with the coin symbol"
    assert get_coin_name("XRP") == "XRP", "XRP name should match with the coin symbol"

# test db model
def test_db_model():
    new_crypto = Cryptos(name="Bitcoin", quantity=0.005, cost=12000)
    assert new_crypto.name == "Bitcoin", "Crypto's name doesn't match with DB model"
    assert new_crypto.quantity == 0.005, "Crypto's quantity doesn't match with DB model"
    assert new_crypto.cost == 12000, "Crypto's cost doesn't match with DB model"

# Test Set up db and add crypto

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))

class TestCrypto():

    def setUp(self):
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testAddCrypto(self):
        # Create a crypto
        crypto = Cryptos("Bitcoin", 0.005, 12000)
        db.session.add(crypto)
        db.session.commit()

        # Check that it exists in the db
        assert len(crypto.query.all()) is not null




