from requests import Request, Session
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json 

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, FloatField, SubmitField
from wtforms.validators import DataRequired

# API coinmarketcap connexion

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
  'start' : '1',
  'limit' : '10',
  'convert' : 'EUR'
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '6dbc77f7-ff71-432a-9061-8024cfc58b72',
} 

session = Session()
session.headers.update(headers) 

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

for x in data['data']:
  if x['symbol'] == 'BTC' or x['symbol'] == 'ETH' or x['symbol'] == 'XRP':
    symbol = str(x['symbol'])
    name = str(x['name'])
    price = float(x['quote']['EUR']['price'])
    print(symbol, '-', name, ' : ', f'{price:.2f}', '€')

# tests to get btc eth xrp prices:
#
# def get_bitcoin_price(): 
#   price = float(data['data']['1']['quote']['EUR']['price']) 
# 
# def get_ethereum_price(): 
#   price = float(data['data']['1027']['quote']['EUR']['price']) 
# 
# def get_ripple_price():
#   price = float(data['data']['52']['quote']['EUR']['price']) 
# 
# print(get_bitcoin_price(), get_ethereum_price(), get_ripple_price())

# Business logic:



# Create AddCrypto form Class
class AddCrypto(FlaskForm):
    name = SelectField("Sélectionner une crypto", choices=[("BTC", "Bitcoin"),("ETH", "Etheureum"),("XRP", "Ripple")], coerce=str, validators=[DataRequired()])
    quantity = FloatField("Quantité", validators=[DataRequired()])
    cost = FloatField("Prix d'achat", validators=[DataRequired()])
    submit = SubmitField("Ajouter")

# Create RemoveCrypto Form Class
class RemoveCrypto(FlaskForm):
    name = SelectField("Sélectionner une crypto", choices=[("BTC", "Bitcoin"),("ETH", "Etheureum"),("XRP", "Ripple")], coerce=str, validators=[DataRequired()])
    quantity = FloatField("Quantité", validators=[DataRequired()])
    submit = SubmitField("Valider")

