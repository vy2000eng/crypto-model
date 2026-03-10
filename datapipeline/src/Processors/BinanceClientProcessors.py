
from ..abstract.IBinanceClientProcessors import IBinanceClientProcesssors
import requests
import pandas as pd
class BinanceClientProcessors(IBinanceClientProcesssors):
    def __init__(self):
        self.structure = {  
                            "funding_rate":["timestamp","fundingTime", "funding_rate","fundingRate"],
                            "open_interest":["timestamp", "timestamp","open_interest","sumOpenInterest"],
                            "long_short_ratio":["timestamp", "timestamp","long_short_ratio","longShortRatio"],
                            }

    def generate_df(self,data:requests.Response, type:str) -> pd.DataFrame:
        df = pd.DataFrame(data)
        response_df_col = self.structure[type]
        response_col_name1 = response_df_col[0]
        response_col_name2 = response_df_col[1]
        response_col_name3 = response_df_col[2]
        response_col_name4 = response_df_col[3]

        df[response_col_name1] = pd.to_datetime(df[response_col_name2], unit="ms")
        df[response_col_name3] = df[response_col_name4].astype(float)
        return df[[response_col_name1, response_col_name3]]

