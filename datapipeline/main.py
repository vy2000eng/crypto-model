

from src.utils.EnvVars import EnvVars
from src.Client.BinanaceClient import BinanceClient
from src.controller.PipelineController import PipelineController
import pandas as pd

if __name__ == "__main__":
    envVars         = EnvVars()
   # binanceClient   = BinanceClient(envVars)
    df = pd.read_csv(envVars.TRAINING_DATA_PATH_MARK_STRUCT)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")
    target_corr = df.corr(numeric_only=True)["future_return"].sort_values(ascending=False)
    print(target_corr)



    # print(envVars.B_API_KEY)
    # print(envVars.B_SECRET_KEY)

    # df = pipeline.fetch_ohlcv()
    # computed_df = pipeline.calculate_technical_indicators(df)
    # computed_df.to_csv('datapipeline/data/ohlcv+technical.csv')


    # print(df.tail(10))





