

import pandas as pd





class YFinProcessor():
    def __init__(self):
        pass


    def processData(self, dxy):
              # rename columns

        dxy = dxy.rename(columns={
            "Date": "timestamp",
            "Open": "dxy_open",
            "High": "dxy_high",
            "Low": "dxy_low",
            "Close": "dxy_close"
        })

        dxy["timestamp"] = pd.to_datetime(dxy["timestamp"])

        # useful features
        dxy["dxy_change"] = dxy["dxy_close"].pct_change()
        dxy["dxy_momentum"] = dxy["dxy_close"] - dxy["dxy_close"].rolling(5).mean()

        dxy = dxy.dropna()

        # keep only useful columns
        dxy = dxy[
            [
                "timestamp",
                "dxy_close",
                "dxy_change",
                "dxy_momentum"
            ]
        ]

        return dxy
