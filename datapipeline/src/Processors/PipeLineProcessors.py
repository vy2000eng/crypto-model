


from ..abstract.IPipelineProcessors import IPipelineProcessor
from src.Client.BinanaceClient import BinanceClient
from src.utils.EnvVars import EnvVars
from datetime import datetime
import pandas as pd
import pandas_ta as ta
import numpy as np





class PipelineProcessors(IPipelineProcessor):
    def __init__(self):
        self.binance_client  = BinanceClient()

    def fetch_ohlc_data(self):

        since = int(datetime(2021, 8, 1).timestamp() * 1000)

        all_candles = []

        while True:

            candles = self.binance_client.get_ohlc(since=since)

            if not candles:
                break

            all_candles.extend(candles)

            since = candles[-1][0] + 1

            print(f"Fetched up to {pd.to_datetime(candles[-1][0], unit='ms')}")

            if len(candles) < 1000:
                break

        df = pd.DataFrame(
            all_candles,
            columns=['timestamp','open','high','low','close','volume']
        )

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        df.set_index('timestamp', inplace=True)

        df = df.drop_duplicates()

        print(f"\nDone — {len(df)} rows fetched")

        return df

    def adjust_df(self, df):
        #df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        #df.set_index('timestamp', inplace=True)
        df = df.drop_duplicates()
        print(f"\nDone — {len(df)} rows fetched")
        return df
    
    def calculate_technical_indicators(self, df):
        df = df.copy()

        # RSI
        df['rsi'] = ta.rsi(df['close'], length=14)

        # MACD
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
        df[['macd', 'macd_signal', 'macd_hist']] = macd

        # Bollinger Bands
        bb = ta.bbands(df['close'], length=20, std=2)
        df[['bb_lower', 'bb_mid', 'bb_upper', 'bb_percent', 'bb_bandwidth']] = bb

        # Custom metrics
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['close']
        df['volume_change'] = df['volume'].pct_change() * 100
        df['price_momentum'] = df['close'].pct_change(4) * 100

        df.dropna(inplace=True)

        return df
    

    def fetch_open_interest_history(self):

        since = int(datetime(2021, 8, 1).timestamp() * 1000)

        step = 500 * 60 * 60 * 1000  # 500 hours in ms

        all_data = []

        while True:

            end_time = since + step

            df = self.binance_client.get_open_interest(
                start_time=since,
                end_time=end_time
            )

            if df.empty:
                break

            all_data.append(df)

            last_ts = int(df.index[-1].value / 1e6)

            print(f"Fetched OI up to {df.index[-1]}")

            since = last_ts + 1

            if len(df) < 500:
                break

        final_df = pd.concat(all_data)

        final_df = final_df.drop_duplicates()

        final_df.sort_index(inplace=True)

        return final_df
    


    def fetch_funding_history(self):

        since = int(datetime(2021, 8, 1).timestamp() * 1000)

        now = int(datetime.utcnow().timestamp() * 1000)

        all_data = []

        while True:

            df = self.binance_client.get_funding_rates(start_time=since)

            if df.empty:
                break

            all_data.append(df)

            last_ts = int(df["timestamp"].iloc[-1].timestamp() * 1000)

            print(f"Fetched funding up to {df['timestamp'].iloc[-1]}")

            if last_ts >= now:
                break

            since = last_ts + 1

            if len(df) < 1000:
                break

        final_df = pd.concat(all_data)

        final_df = final_df.drop_duplicates()

        final_df.set_index("timestamp", inplace=True)

        return final_df
    
    def fetch_long_short_ratio_history(self):

        since = int(datetime(2021, 8, 1).timestamp() * 1000)

        all_data = []

        while True:

            df = self.binance_client.get_long_short_ratio(start_time=since)

            if df.empty:
                break

            all_data.append(df)

            last_ts = int(df["timestamp"].iloc[-1].timestamp() * 1000)

            since = last_ts + 1

            print(f"Fetched long/short up to {df['timestamp'].iloc[-1]}")

            if len(df) < 500:
                break

        final_df = pd.concat(all_data)

        final_df = final_df.drop_duplicates()

        final_df.set_index("timestamp", inplace=True)

        return final_df
    


    def add_market_structure(self, df):
    # fetch market datasets
        funding = self.fetch_funding_history()
       # oi = self.fetch_open_interest_history()
        #ratio = self.fetch_long_short_ratio_history()

        # ensure OHLC dataframe is sorted
        df = df.sort_index()

        # join datasets
        df = df.join(funding, how="left")
        df["funding_rate"] = df["funding_rate"].ffill()
        df["funding_rate"] = df["funding_rate"].fillna(0)
        df["future_return"] = df["close"].pct_change().shift(-1)
        df["log_return"] = np.log(df["close"] / df["close"].shift(1))
        df = df.dropna()
        df["return_1h"] = df["close"].pct_change()

        df["volatility_12h"] = df["return_1h"].rolling(12).std()
        df["volatility_24h"] = df["return_1h"].rolling(24).std()

        df["hl_range"] = (df["high"] - df["low"]) / df["close"]
        df["hl_volatility"] = df["hl_range"].rolling(12).mean()

        df["return_1h"] = df["close"].pct_change()

        df["volatility_12h"] = df["return_1h"].rolling(12).std()
        df["volatility_24h"] = df["return_1h"].rolling(24).std()

        df["hl_range"] = (df["high"] - df["low"]) / df["close"]
        df["hl_volatility"] = df["hl_range"].rolling(12).mean()
        df["future_return_1h"] = df["close"].pct_change(1).shift(-1)
        df["future_return_3h"] = df["close"].pct_change(3).shift(-3)
        df["future_return_6h"] = df["close"].pct_change(6).shift(-6)
        df["future_return_12h"] = df["close"].pct_change(12).shift(-12)



        #df = df.join(oi, how="left")
        #df = df.join(ratio, how="left")

        # forward fill because funding / OI aren't every candle
        #df["funding_rate"].fillna(method="ffill", inplace=True)
       # df["open_interest"].fillna(method="ffill", inplace=True)
        #df["long_short_ratio"].fillna(method="ffill", inplace=True)

        # derived features
       # df["oi_change"] = df["open_interest"].pct_change()

        return df

    def merge_us_dollar_df(self, df, us_dollar_df):

        # merge macro data into crypto dataframe
        df = df.merge(
            us_dollar_df,
            on="timestamp",
            how="left"
        )

        # forward fill because DXY is daily but crypto is higher frequency
        macro_cols = [
            "dxy_close",
            "dxy_change",
            "dxy_momentum"
        ]

        df[macro_cols] = df[macro_cols].ffill()

        return df