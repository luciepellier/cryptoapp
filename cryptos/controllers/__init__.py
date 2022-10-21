from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired

# API coinmarketcap connexion

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
parameters = {
  "start" : "1",
  "limit" : "1050",
  "convert" : "EUR"
}
headers = {
  "Accepts": "application/json",
  "X-CMC_PRO_API_KEY": "3d73188b-6111-4121-b699-d3004c398725",
} 
session = Session()
session.headers.update(headers) 
try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

# Def coin ID dict
coin_id_dict = {
  "ETH": 1027,
  "BTC": 1,
  "XRP": 52,
}

# Get coin name:
def get_coin_name(coin):
  coin_id = coin_id_dict.get(coin, False)
  if (coin_id):
    for x in data["data"]:
      if x["id"] == coin_id:
        name = str(x["name"])
        return name
  return False

# Get coins current prices:
def get_coin_price(coin):
  coin_id = coin_id_dict.get(coin, False)
  if (coin_id):
    for x in data["data"]:
      if x["id"] == coin_id:
        price = float(x["quote"]["EUR"]["price"])
        return price
  return False

# Get coin changes last 24h
def get_coin_change(coin):
  coin_id = coin_id_dict.get(coin, False)
  if (coin_id):
    for x in data["data"]:
      if x["id"] == coin_id:
        change = float(x["quote"]["EUR"]["percent_change_24h"])
        return change
  return False

# Create AddCrypto form Class
class AddForm(FlaskForm):
    name = SelectField("Sélectionner une crypto", choices=[("BTC", "Bitcoin"),("ETH", "Etheureum"),("XRP", "Ripple")], coerce=str, validators=[DataRequired()])
    quantity = FloatField("Quantité", validators=[DataRequired()])
    cost = FloatField("Prix d'achat", validators=[DataRequired()])
    submit = SubmitField("Ajouter")

# Create RemoveCrypto Form Class
class RemoveForm(FlaskForm):
    name = SelectField("Sélectionner une crypto", choices=[("BTC", "Bitcoin"),("ETH", "Etheureum"),("XRP", "Ripple")], coerce=str, validators=[DataRequired()])
    quantity = FloatField("Quantité", validators=[DataRequired()])
    cost = FloatField("Prix de vente", validators=[DataRequired()])
    submit = SubmitField("Valider")

# Define Save coin function
def save_coin(name: str, quantity: float, cost: float):
  from ..models import Cryptos
  from ..app import db, engine, session
  print(f"Crypto bought {name.data} {quantity.data} {cost.data}")
  with session() as session:
    new_crypto = Cryptos(
      name=name.data, quantity=quantity.data, cost=cost.data
    )
    session.add(new_crypto)
    session.commit()

# Define Edit coin function
def edit_coin(name: str, quantity: float, cost: float):
  from ..models import Cryptos
  from ..app import db, engine, session
  print(f"Crypto sold {name.data} {quantity.data} {cost.data}") 
  with session() as session:
    new_crypto = Cryptos(
      name=name.data, quantity= quantity.data, cost= -cost.data
    )
    session.add(new_crypto)
    session.commit()

## Define Delete coin function
#def delete_coin(name: str, quantity: float):
#  from ..models import Cryptos
#  from ..app import db, engine, session
#  print(f"Crypto removed {name.data} {quantity.data}") 
#  with session() as session:
#    to_delete_crypto = Cryptos(
#      name=name.data, quantity= quantity.data)
#    session.delete(to_delete_crypto)
#    session.commit()