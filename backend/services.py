import pandas as pd
import joblib
import os
from database.db import get_connection


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")


class FraudDetector:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def load_data(self):
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM electricity_usage", conn)
        conn.close()
        return df

    def engineer_features(self, df):
        df = df.sort_values(by=["meter_id", "timestamp"])

        df["rolling_avg"] = df.groupby("meter_id")["consumption"].transform(
            lambda x: x.rolling(window=5, min_periods=1).mean()
        )

        df["spike_ratio"] = df["consumption"] / df["rolling_avg"]
        return df.fillna(0)

    def detect(self):
        df = self.load_data()
        df = self.engineer_features(df)

        features = df[["consumption", "voltage", "spike_ratio"]]
        df["anomaly"] = self.model.predict(features)

        return df

   
    def predict_single(self, consumption, voltage):
        # No history → assume spike_ratio = 1 (baseline)
        spike_ratio = 1  

        features = [[consumption, voltage, spike_ratio]]

        pred = self.model.predict(features)

        return int(pred[0])  # return -1 or 1