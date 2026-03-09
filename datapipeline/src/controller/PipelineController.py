from ..abstract.IPipeLine import IPipeLine
from src.Client.BinanaceClient import BinanceClient
from datetime import datetime
import pandas as pd
import numpy as np
from src.utils.EnvVars import EnvVars
from src.Processors.PipeLineProcessors import PipelineProcessors
from src.Client.YFinClient import YFinClient



class PipelineController(IPipeLine):

    def __init__(self):
        self.envVars         = EnvVars()
        self.binance_client  = BinanceClient()
        self.pipline_processors = PipelineProcessors()
        self.yfin_client = YFinClient()




    def fetch_ohlcv(self):
        df          = self.pipline_processors.fetch_ohlc_data()
        adjusted_df =  self.pipline_processors.adjust_df(df)        
        return adjusted_df
    

    def load_ohlc_csv(self):
        file_path = 'datapipeline/data/ohlcv.csv'
        df = pd.read_csv(file_path)
        return df

    def calculate_technical_indicators(self, ohlc_df):
        return  self.pipline_processors.calculate_technical_indicators(ohlc_df)
        
    
    def generate_training_data(self):
        df = self.fetch_ohlcv()
        us_dollar_df = self.yfin_client.fetch_dxy_data()
        df = self.calculate_technical_indicators(df)
        df = self.pipline_processors.add_market_structure(df)
        df = self.pipline_processors.merge_us_dollar_df(df,us_dollar_df )

    

        return df
    
    def convert_df_to_csv(self,df):
        df.to_csv('datapipeline/data/ohlcv+technical+market_struct.csv',index=False)








        



