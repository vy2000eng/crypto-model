

from abc import ABC, abstractmethod
import pandas as pd
import requests


class IBinanceClientProcesssors(ABC):
    
    @abstractmethod
    def generate_df(data:requests.Response,type:str) -> pd.DataFrame:
        pass

