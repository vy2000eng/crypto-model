import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datapipeline.src.utils.EnvVars import EnvVars


# ------------------------------------------------
# Load data
# ------------------------------------------------

envVars = EnvVars()
df = pd.read_csv(envVars.TRAINING_DATA_PATH_MARK_STRUCT)

split = int(len(df) * 0.8)
df_test = df.iloc[split:].copy().reset_index(drop=True)


# ------------------------------------------------
# Load model
# ------------------------------------------------

model = joblib.load("models/xgb_volatility_model_new_features.pkl")
features = joblib.load("models/model_features_new_features.pkl")


# ------------------------------------------------
# Predict probabilities
# ------------------------------------------------

df_test["model_prob"] = model.predict_proba(df_test[features])[:, 1]

# match label horizon
df_test["abs_return"] = df_test["future_return_12h"].abs()


# ------------------------------------------------
# Signal diagnostics
# ------------------------------------------------

print("\nModel probability distribution")
print(df_test["model_prob"].describe())

print("\nVolatility by probability bucket")
print(
    df_test.groupby(pd.qcut(df_test["model_prob"], 10))["abs_return"].mean()
)

print("\nCorrelation between probability and volatility")
print(df_test[["model_prob", "abs_return"]].corr())


# ------------------------------------------------
# Strategy parameters
# ------------------------------------------------

threshold = df_test["model_prob"].quantile(0.98)   # try stronger signals

capital = 500
position_size = 0.20
capture_rate = 0.25

fee = 0.001
slippage = 0.0005
vol_premium = 0.01

equity_curve = [capital]
profits = []

wins = 0
losses = 0
trades = 0


# ------------------------------------------------
# Backtest
# ------------------------------------------------

HORIZON = 12

i = 0

while i < len(df_test) - HORIZON:

    prob = df_test["model_prob"].iloc[i]

    if prob > threshold:

        trades += 1

        entry_price = df_test["close"].iloc[i]

        future_window = df_test.iloc[i:i+HORIZON]

        future_high = future_window["high"].max()
        future_low = future_window["low"].min()

        # true volatility range
        realized_move = abs((future_high - future_low) / entry_price)

        captured_move = realized_move * capture_rate

        cost = (fee * 2) + slippage + vol_premium

        net_move = captured_move - cost

        trade_capital = capital * position_size
        profit = trade_capital * net_move

        profits.append(profit)

        capital += profit

        if profit > 0:
            wins += 1
        else:
            losses += 1

        i += HORIZON

    else:
        i += 1

    equity_curve.append(capital)


# ------------------------------------------------
# Results
# ------------------------------------------------

print("\nFinal capital:", round(capital, 2))
print("Return:", round((capital / 500 - 1) * 100, 2), "%")
print("Trades:", trades)

if trades > 0:
    print("Win rate:", round(wins / trades * 100, 2), "%")


# ------------------------------------------------
# Trade statistics
# ------------------------------------------------

profits = np.array(profits)

if len(profits) > 0:

    avg_win = profits[profits > 0].mean() if (profits > 0).any() else 0
    avg_loss = profits[profits < 0].mean() if (profits < 0).any() else 0

    profit_factor = (
        profits[profits > 0].sum()
        / abs(profits[profits < 0].sum())
        if (profits < 0).any()
        else float("inf")
    )

    expectancy = profits.mean()

    print("\nTrade statistics")
    print("Avg win:", round(avg_win, 4))
    print("Avg loss:", round(avg_loss, 4))
    print("Profit factor:", round(profit_factor, 3))
    print("Expectancy per trade:", round(expectancy, 4))

    print("\nSignal thresholds")
    print(df_test["model_prob"].quantile([0.90, 0.95, 0.98, 0.99]))


# ------------------------------------------------
# Plot equity curve
# ------------------------------------------------

plt.figure(figsize=(12,5))
plt.plot(equity_curve)
plt.title("Volatility Strategy Equity Curve (Test Data)")
plt.xlabel("Steps")
plt.ylabel("Portfolio Value ($)")
plt.show()


# ------------------------------------------------
# Signal scatter plot
# ------------------------------------------------

plt.figure(figsize=(6,5))
plt.scatter(df_test["model_prob"], df_test["abs_return"], alpha=0.2)
plt.xlabel("Model Probability")
plt.ylabel("Absolute Return")
plt.title("Model Signal vs Realized Volatility")
plt.show()


# ------------------------------------------------
# Alpha curve
# ------------------------------------------------

percentiles = np.linspace(0.80, 0.995, 30)
results = []

for p in percentiles:

    threshold = df_test["model_prob"].quantile(p)
    subset = df_test[df_test["model_prob"] > threshold]

    results.append(subset["abs_return"].mean() if len(subset) > 0 else np.nan)

plt.figure(figsize=(8,5))
plt.plot(percentiles, results)
plt.xlabel("Signal Percentile Threshold")
plt.ylabel("Average Realized Volatility")
plt.title("Signal Strength Curve")
plt.show()