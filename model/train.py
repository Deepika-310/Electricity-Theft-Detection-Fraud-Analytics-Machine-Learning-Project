import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from database.db import get_connection


MODEL_PATH = "model/model.pkl"


def load_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM electricity_usage", conn)
    conn.close()
    return df
df = load_data()
print("Rows:", len(df))
print(df.head())


def engineer_features(df):
    """
    Add simple but meaningful features.
    This is where you show thinking.
    """

    df = df.sort_values(by=["meter_id", "timestamp"])

    # Rolling average (per meter)
    df["rolling_avg"] = df.groupby("meter_id")["consumption"].transform(
        lambda x: x.rolling(window=5, min_periods=1).mean()
    )

    # Spike ratio
    df["spike_ratio"] = df["consumption"] / df["rolling_avg"]

    return df


def train():
    df = load_data()
    df = engineer_features(df)

    features = df[["consumption", "voltage", "spike_ratio"]].fillna(0)

    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    model.fit(features)

    joblib.dump(model, MODEL_PATH)

    print("✅ Model trained and saved at:", MODEL_PATH)


if __name__ == "__main__":
    train()