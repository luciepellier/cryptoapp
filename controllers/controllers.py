from colorlog import info
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint 

from flask_sqlalchemy import SQLAlchemy

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

# Get 3 cryptos current prices:
def get_btc_price():
  for x in data["data"]:
    if x["id"] == 1:
      price = float(x["quote"]["EUR"]["price"])
      return price
print(get_btc_price())

def get_eth_price():
  for x in data["data"]:
    if x["id"] == 1027:
      price = float(x["quote"]["EUR"]["price"])
      return price
print(get_eth_price())

def get_xrp_price():
  for x in data["data"]:
    if x["id"] == 52:
      price = float(x["quote"]["EUR"]["price"])
      return price
print(get_xrp_price())

# Get 3 cryptos changes last 24h

def get_btc_change():
  for x in data["data"]:
    if x["id"] == 1:
      price = float(x["quote"]["EUR"]["percent_change_24h"])
      return price
print(get_btc_change())

def get_eth_change():
  for x in data["data"]:
    if x["id"] == 1027:
      price = float(x["quote"]["EUR"]["percent_change_24h"])
      return price
print(get_eth_change())

def get_xrp_change():
  for x in data["data"]:
    if x["id"] == 52:
      price = float(x["quote"]["EUR"]["percent_change_24h"])
      return price
print(get_xrp_change())

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

