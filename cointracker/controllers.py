from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
from .models import Crypto

from pprint import pprint

# from .settings import COINMARKETCAP_TOKEN

COINMARKETCAP_TOKEN = "6dbc77f7-ff71-432a-9061-8024cfc58b72"


def get_coin_price():

  cmc = CoinMarketCapAPI(COINMARKETCAP_TOKEN)
  
#   r = cmc.cryptocurrency_info(symbol='BTC')
  r = cmc.cryptocurrency_listings_historical(symbol='BTC')

  pprint(r.data)




get_coin_price()