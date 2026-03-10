from ..abstract.IBinanceClient import IBinanaceClient
import ccxt
import requests
import pandas as pd
from src.Processors.BinanceClientProcessors import BinanceClientProcessors

class BinanceClient(IBinanaceClient):

     def __init__(self):
           self.exchange = ccxt.binance()
           self.futures_base = "https://fapi.binance.com"
           self.binance_client_processors = BinanceClientProcessors()



                #{ 'apiKey': envVars.B_API_KEY,'secret': envVars.B_SECRET_KEY})
           
     def get_ohlc(self,symbol='ETH/USDT', timeframe='1h', since=None, limit=1000):
         return self.exchange.fetch_ohlcv(symbol,timeframe,since, limit)
         

     def get_funding_rates(self, symbol="ETHUSDT", start_time=None,limit=1000):

          url = f"{self.futures_base}/fapi/v1/fundingRate"

          params = {
               "symbol": symbol,
               "limit": limit
          }
          if start_time:
               params["startTime"] = start_time

          data = requests.get(url, params=params).json()
          return self.binance_client_processors.generate_df(data,"funding_rate")

     #NOTE: below only have 30 day data
     def get_open_interest(self, symbol="ETHUSDT", start_time=None, end_time=None, limit=500):

          url = f"{self.futures_base}/futures/data/openInterestHist"

          params = {
               "symbol": symbol,
               "period": "1h",
               "limit": limit
          }

          if start_time:
               params["startTime"] = int(start_time)

          if end_time:
               params["endTime"] = int(end_time)

          response = requests.get(url, params=params)

          data = response.json()

          return self.binance_client_processors.generate_df(data, "open_interest")


     
     def get_long_short_ratio(self, symbol="ETHUSDT", start_time=None, limit=500):

          url = f"{self.futures_base}/futures/data/globalLongShortAccountRatio"

          params = {
               "symbol": symbol,
               "period": "1h",
               "limit": limit
          }

          if start_time:
               params["startTime"] = start_time

          data = requests.get(url, params=params).json()
          return self.binance_client_processors.generate_df(data,"long_short_ratio")


     
