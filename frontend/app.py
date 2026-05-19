import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Fraud Detection", layout="wide")

st.title(" Electricity Fraud Detection System")
#loading of data
@st.cache_data
def load_data():
    try:
        res = requests.get(f"{API_URL}/detect")
        res.raise_for_status()
        data = res.json()

        if isinstance(data, dict):
            data = [data]

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


df = load_data()

st.subheader(" Raw Usage Data")
st.dataframe(df, use_container_width=True)


#fraud cases
st.subheader("🚨 Detected Anomalies")

try:
    frauds = requests.get(f"{API_URL}/fraud-cases")
    frauds.raise_for_status()
    fraud_data = frauds.json()

    # FIX: handle dict vs list
    if isinstance(fraud_data, dict):
        fraud_data = [fraud_data]

    fraud_df = pd.DataFrame(fraud_data)

except Exception as e:
    st.error(f"Error loading fraud cases: {e}")
    fraud_df = pd.DataFrame()

st.dataframe(fraud_df, use_container_width=True)


#prediction selection
st.subheader(" Check New Reading")

col1, col2 = st.columns(2)

with col1:
    consumption = st.number_input("Consumption", value=15.0)

with col2:
    voltage = st.number_input("Voltage", value=220.0)


if st.button("Run Detection"):
    try:
        res = requests.post(
            f"{API_URL}/predict",
            json={
                "consumption": consumption,
                "voltage": voltage
            }
        )
        res.raise_for_status()
        result = res.json()

        # Flexible handling
        is_fraud = result.get("fraud") or result.get("anomaly") == 1

        if is_fraud:
            st.error("Fraud Detected")
        else:
            st.success(" Normal Usage")

        st.write(" Response:", result)

    except Exception as e:
        st.error(f"Prediction failed: {e}")