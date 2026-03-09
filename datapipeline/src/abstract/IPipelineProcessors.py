from abc import ABC, abstractmethod
import pandas as pd

class IPipelineProcessor(ABC):

    @abstractmethod
    def fetch_ohlc_data(self,df:pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def adjust_df(self, df) -> pd.DataFrame:
        pass

    @abstractmethod
    def calculate_technical_indicators() -> pd.DataFrame:
        pass

    @abstractmethod
    def add_market_structure(self, df):
        pass

    @abstractmethod
    def fetch_open_interest_history(self):
        pass
    
    @abstractmethod
    def fetch_funding_history(self):
        pass

    @abstractmethod
    def fetch_long_short_ratio_history(self):
        pass

    @abstractmethod
    def add_market_structure(self, df):
        pass






    