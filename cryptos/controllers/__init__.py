from colorlog import info
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint 

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, FloatField, SubmitField
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
  "X-CMC_PRO_API_KEY": "6dbc77f7-ff71-432a-9061-8024cfc58b72",
} 
session = Session()
session.headers.update(headers) 
try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

def printCoinData():  
  for x in data["data"]:
    if x["symbol"] == "BTC" or x["symbol"] == "ETH" or x["symbol"] == "XRP":
      symbol = str(x["symbol"])
      name = str(x["name"])
      price = float(x["quote"]["EUR"]["price"])
      change = float(x["quote"]["EUR"]["percent_change_24h"])
      print(symbol, "-", name, " : ", f"{price:.2f}", "€", " / change last 24h: ", f"{change:.2f}", "%")
printCoinData()

# Def coin ID dict
coin_id_dict = {
  "eth": 1027,
  "btc": 1,
  "xrp": 52,
}

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

print(get_coin_price('1'))
print(get_coin_change('1'))

# Create AddCrypto form Class
class AddForm(FlaskForm):
    name = SelectField("Sélectionner une crypto", choices=[("BTC", "Bitcoin"),("ETH", "Etheureum"),("XRP", "Ripple")], coerce=str, validators=[DataRequired()])
    quantity = FloatField("Quantité", validators=[DataRequired()])
    cost = FloatField("Prix d'achat", validators=[DataRequired()])
    submit = SubmitField("Ajouter")

# Add Crypto from the form to the db
# def add_crypto():




# Create RemoveCrypto Form Class
class RemoveForm(FlaskForm):
    name = SelectField("Sélectionner une crypto", choices=[("BTC", "Bitcoin"),("ETH", "Etheureum"),("XRP", "Ripple")], coerce=str, validators=[DataRequired()])
    quantity = FloatField("Quantité", validators=[DataRequired()])
    submit = SubmitField("Valider")

# Remove Crypto from the form to the db, get_btc_price get_eth_price or get_xrp_price 
# to obtain and insert the current price in the db
# def RemoveCrypto():

# Get Total Cryptos sum of all cryptos added and removed in the db 
# def TotalCryptos():

