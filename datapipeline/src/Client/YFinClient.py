import yfinance as yf
import pandas as pd
from src.utils.EnvVars import EnvVars
from src.Processors.YFinProcessors import YFinProcessor
from ..abstract.IYfinClient import IYFindClient


class YFinClient(IYFindClient):
    def __init__(self):
        self.envVars = EnvVars()
        self.yfinPRocessors = YFinProcessor()
        #self.start_Date = self.envVars.


    def fetch_dxy_data(self):
        start = self.envVars.START_DATE

        dxy = yf.download(
            "DX-Y.NYB",   # US Dollar Index
            start=start,
            interval="1d"
        )
        dxy.columns = dxy.columns.droplevel(1)
        dxy = dxy.reset_index()
        return self.yfinPRocessors.processData(dxy)

        #print(dxy.head())




