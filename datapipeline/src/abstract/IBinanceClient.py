from abc import ABC, abstractmethod

class IBinanaceClient(ABC):
    
    # @abstractmethod
    # def auth_get_request(self):
    #     pass

    # @abstractmethod
    # def auth_post_request(self):
    #     pass

    @abstractmethod
    def get_ohlc(self,symbol='ETH/USDT', timeframe='1h', since=None, limit=1000):
        pass

    @abstractmethod
    def get_funding_rates(self, symbol="ETHUSDT", limit=1000):
        pass


    @abstractmethod
    def get_open_interest(self, symbol="ETHUSDT", limit=500):
        pass


    @abstractmethod
    def get_long_short_ratio(self, symbol="ETHUSDT", limit=500):
        pass









     
        

    