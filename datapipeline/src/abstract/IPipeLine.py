from abc import ABC, abstractmethod
import pandas as pd




class IPipeLine(ABC):

    @abstractmethod 
    def fetch_ohlcv(self):
        pass

    @abstractmethod 
    def load_ohlc_csv(self) -> pd.DataFrame :
        pass

    @abstractmethod 
    def calculate_technical_indicators(self, df)-> pd.DataFrame:
        pass

    @abstractmethod
    def generate_training_data(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def convert_df_to_csv(self, df) -> None:
        pass







