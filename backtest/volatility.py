import joblib
import pandas as pd
import numpy as np

from sklearn.metrics import roc_auc_score
from datapipeline.src.utils.EnvVars import EnvVars


envVars = EnvVars()

# ------------------------------------------------
# Load dataset
# ------------------------------------------------

df = pd.read_csv(envVars.TRAINING_DATA_PATH_MARK_STRUCT)

# ------------------------------------------------
# Load model + feature list
# ------------------------------------------------

model = joblib.load("models/xgb_volatility_model.pkl")
features = joblib.load("models/model_features.pkl")

# ------------------------------------------------
# Build target (same as training)
# ------------------------------------------------

df["future_volatility"] = df["future_return_6h"].abs()

threshold = df["future_volatility"].quantile(0.75)
df["target"] = (df["future_volatility"] > threshold).astype(int)

# ------------------------------------------------
# Split dataset (same split used in training)
# ------------------------------------------------

split = int(len(df) * 0.8)

df_test = df.iloc[split:].copy()

X_test = df_test[features]
y_test = df_test["target"]

# ------------------------------------------------
# Run model
# ------------------------------------------------

proba = model.predict_proba(X_test)[:, 1]
df_test["model_prob"] = proba

print("\nSample predictions:")
print(df_test[["model_prob"]].head())

# ------------------------------------------------
# 1️⃣ AUC check
# ------------------------------------------------

auc = roc_auc_score(y_test, df_test["model_prob"])
print("\nTest AUC:", auc)

# ------------------------------------------------
# 2️⃣ Probability ranking test
# ------------------------------------------------

print("\nVolatility frequency by probability bucket:")

bucket_vol = df_test.groupby(
    pd.qcut(df_test["model_prob"], 10, duplicates="drop")
)["target"].mean()

print(bucket_vol)

# ------------------------------------------------
# 3️⃣ Actual volatility magnitude test
# ------------------------------------------------

print("\nAverage future volatility by probability bucket:")

bucket_mag = df_test.groupby(
    pd.qcut(df_test["model_prob"], 10, duplicates="drop")
)["future_volatility"].mean()

print(bucket_mag)



importance = pd.Series(
    model.feature_importances_,
    index=features
).sort_values(ascending=False)


import matplotlib.pyplot as plt

# ------------------------------------------------
# Prepare test dataframe
# ------------------------------------------------

df_test = df.iloc[split:].copy().reset_index(drop=True)

# run model predictions
df_test["model_prob"] = model.predict_proba(df_test[features])[:,1]

# create volatility regime
high_threshold = 0.40
df_test["vol_regime"] = df_test["model_prob"] > high_threshold

# ------------------------------------------------
# Plot price + predictions
# ------------------------------------------------

fig, ax1 = plt.subplots(figsize=(14,6))

# price
ax1.plot(df_test.index, df_test["close"], color="black", label="Price")
ax1.set_ylabel("Price")

# highlight high-volatility predictions
high_vol = df_test[df_test["vol_regime"]]

ax1.scatter(
    high_vol.index,
    high_vol["close"],
    color="red",
    s=10,
    label="High Volatility Prediction"
)

# second axis for probability
ax2 = ax1.twinx()

ax2.plot(
    df_test.index,
    df_test["model_prob"],
    color="blue",
    alpha=0.4,
    label="Volatility Probability"
)

ax2.set_ylabel("Volatility Probability")

plt.title("Model Volatility Predictions vs Price")

fig.legend(loc="upper left")

plt.show()


