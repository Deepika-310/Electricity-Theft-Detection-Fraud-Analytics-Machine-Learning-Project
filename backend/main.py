from fastapi import FastAPI
from backend.services import FraudDetector

app = FastAPI()
from pydantic import BaseModel

class InputData(BaseModel):
    consumption: float
    voltage: float

@app.post("/predict")  
def predict(data: InputData):
    result = detector.predict_single(data.consumption, data.voltage)

    return {
        "consumption": data.consumption,
        "voltage": data.voltage,
        "prediction": result,
        "is_fraud": result == -1
    }
detector = FraudDetector()

@app.get("/")
def home():
    return {"message": "Electricity Theft Detection API Running"}


@app.get("/detect")
def detect():
    df = detector.detect()
    return df.to_dict(orient="records")

@app.get("/fraud-cases")
def get_fraud_cases():
    df = detector.detect()  # DataFrame

    data = df.to_dict(orient="records")  

    frauds = [row for row in data if row.get("anomaly") == 1]

    return frauds