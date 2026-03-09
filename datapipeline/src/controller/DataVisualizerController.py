
from ..abstract.IDataVisualizer import IDataVisualizerController
from src.utils.EnvVars import EnvVars
import pandas as pd
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport
import os

class DataVisualizerController(IDataVisualizerController):


    def __init__(self):
        self.envVars = EnvVars()
        self.envVars = EnvVars()
        self.report_dir = "report"
        os.makedirs(self.report_dir, exist_ok=True)

  

    def loadCsv(self):
        df = pd.read_csv(self.envVars.TRAINING_DATA_PATH_MARK_STRUCT)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        return df
    
    def visualizeData(self, df):

    # show only recent data so chart isn't compressed
        df = df.tail(1000)

        fig, axs = plt.subplots(5, 1, figsize=(16,14), sharex=True)

        # ----- PRICE + BOLLINGER BANDS -----
        axs[0].plot(df["timestamp"], df["close"], label="Close")
        axs[0].plot(df["timestamp"], df["bb_upper"], linestyle="--", label="BB Upper")
        axs[0].plot(df["timestamp"], df["bb_lower"], linestyle="--", label="BB Lower")

        axs[0].set_title("Price with Bollinger Bands")
        axs[0].legend()
        axs[0].grid(True, alpha=0.3)


        # ----- VOLUME -----
        axs[1].bar(df["timestamp"], df["volume"])
        axs[1].set_title("Volume")
        axs[1].grid(True, alpha=0.3)


        # ----- RSI -----
        axs[2].plot(df["timestamp"], df["rsi"])

        axs[2].axhline(70, linestyle="--")
        axs[2].axhline(30, linestyle="--")

        axs[2].set_ylim(0,100)  # makes RSI easier to read
        axs[2].set_title("RSI")
        axs[2].grid(True, alpha=0.3)


        # ----- MACD -----
        axs[3].plot(df["timestamp"], df["macd"], label="MACD")
        axs[3].plot(df["timestamp"], df["macd_signal"], label="Signal")
        axs[3].bar(df["timestamp"], df["macd_hist"], alpha=0.3)

        axs[3].set_title("MACD")
        axs[3].legend()
        axs[3].grid(True, alpha=0.3)

        # ----- FUNDING RATE -----
        axs[4].plot(df["timestamp"], df["funding_rate"], color="purple")

        axs[4].axhline(0, linestyle="--")

        axs[4].set_title("Funding Rate")
        axs[4].grid(True, alpha=0.3)


        plt.tight_layout()
        plt.show()

    def visualizeFeatureSignal(self, df):

        df["future_return"] = df["close"].pct_change().shift(-1)

        plt.figure(figsize=(8,6))

        plt.scatter(df["rsi"], df["future_return"], alpha=0.2)

        plt.xlabel("RSI")
        plt.ylabel("Next Return")

        plt.title("RSI vs Future Return")

        plt.grid(True)

        plt.show()

    def price_momentum_vs_returns(self,df):
        plt.scatter(df["price_momentum"], df["future_return"], alpha=0.2)
        plt.xlabel("Price Momentum")
        plt.ylabel("Next Return")
        plt.show()



    def funding_vs_returns(self, df):

        df["future_return"] = df["close"].pct_change().shift(-1)

        plt.figure(figsize=(8,6))

        plt.scatter(df["funding_rate"], df["future_return"], alpha=0.2)

        plt.xlabel("Funding Rate")
        plt.ylabel("Next Return")

        plt.title("Funding Rate vs Future Return")

        plt.grid(True)

        plt.show()

    def funding_regimes(self, df):

        plt.figure(figsize=(14,6))

        plt.plot(df["timestamp"], df["close"], label="Price")

        high_funding = df["funding_rate"] > df["funding_rate"].quantile(0.95)
        low_funding = df["funding_rate"] < df["funding_rate"].quantile(0.05)

        plt.scatter(df.loc[high_funding, "timestamp"],
                    df.loc[high_funding, "close"],
                    color="red",
                    label="High Funding")

        plt.scatter(df.loc[low_funding, "timestamp"],
                    df.loc[low_funding, "close"],
                    color="green",
                    label="Low Funding")

        plt.legend()

        plt.title("Extreme Funding Events")

        plt.show()
    
    def feature_correlation(self, df):

        corr = df.corr(numeric_only=True)

        plt.figure(figsize=(10,8))

        plt.imshow(corr, cmap="coolwarm", interpolation="none")

        plt.colorbar()

        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)

        plt.title("Feature Correlation Matrix")

        plt.tight_layout()

        plt.show()


    def feature_vs_future_return(self, df, feature):

        df["future_return"] = df["close"].pct_change().shift(-1)

        plt.figure(figsize=(8,6))

        plt.scatter(df[feature], df["future_return"], alpha=0.2)

        plt.xlabel(feature)
        plt.ylabel("Next Return")

        plt.title(f"{feature} vs Future Return")

        plt.grid(True)

        plt.show()


    def feature_bucket_returns(self, df, feature):

        df["future_return"] = df["close"].pct_change().shift(-1)

        df["bucket"] = pd.qcut(df[feature], 10, duplicates="drop")

        bucket_returns = df.groupby("bucket")["future_return"].mean()

        bucket_returns.plot(kind="bar", figsize=(10,5))

        plt.title(f"Average Future Return by {feature} Bucket")
        plt.ylabel("Average Next Return")

        plt.grid(True)

        plt.show()
        

    def generate_full_report(self, df):

        report = ProfileReport(
            df,

            title="Crypto Feature Research Report",

            explorative=True,

            correlations={
                "pearson": {"calculate": True},
                "spearman": {"calculate": True},
                "phi_k": {"calculate": True},
            },

            interactions={
                "continuous": True
            },

            missing_diagrams={
                "matrix": True,
                "bar": True,
                "heatmap": True
            },

            samples={
                "head": 20,
                "tail": 20
            }
        )

        report.to_file(f"{self.report_dir}/feature_report.html")