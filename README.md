Electricity Theft Detection System

Electricity theft is a major issue in power distribution systems, leading to financial losses and grid inefficiencies.
This project is a full-stack AI system that detects abnormal electricity usage patterns using machine learning and provides real-time fraud detection through an API and dashboard.

The system combines:

Machine Learning (Anomaly Detection)
Backend API (FastAPI)
Database (SQL)
Frontend Dashboard (Streamlit)
Problem Statement

Electricity consumption data often contains:

sudden spikes in usage
abnormal drops
inconsistent voltage-consumption patterns

Manual monitoring is not scalable.

This project automates detection of suspicious usage patterns in real time.

System Architecture
SQL Database → FastAPI Backend → ML Model → Streamlit Dashboard
Flow:
Data is stored in SQL database
Backend fetches data using FastAPI
ML model analyzes consumption patterns
API returns:
full dataset
fraud cases
real-time prediction
Streamlit visualizes results
 Tech Stack
 Backend
FastAPI → API development
Pydantic → request validation
Uvicorn → server runtime
 Machine Learning
Pandas → data processing
Scikit-learn → Isolation Forest model
NumPy → numerical computation
 Database
SQLite (lightweight local SQL database)
Stores electricity usage logs:
meter_id
timestamp
voltage
consumption
 Frontend
Streamlit → interactive dashboard
Requests → API communication
 Database Schema
CREATE TABLE IF NOT EXISTS electricity_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meter_id TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    voltage REAL,
    consumption REAL
);
This stores
Each row represents electricity usage at a specific time for a meter.

 Machine Learning Approach
Model Used:
Isolation Forest (Unsupervised Anomaly Detection)
Why this model?
No labeled fraud dataset required
Detects unusual patterns automatically
Works well for real-world anomaly detection problems
Features used:
consumption
voltage
spike-based derived patterns (rolling average, anomaly score)
Output:
1 → normal
-1 → anomaly (fraud suspected)
🔌 Backend (FastAPI)
Key Endpoints:
1. Health Check
GET /
2. Full Data
GET /detect

Returns all electricity usage records with anomaly labels.

3. Fraud Cases
GET /fraud-cases

Returns only abnormal electricity usage entries.

4. Real-time Prediction
POST /predict
Input:
{
  "consumption": 15.0,
  "voltage": 220.0
}
Output:
{
  "consumption": 15.0,
  "voltage": 220.0,
  "prediction": -1,
  "is_fraud": true
}
Frontend (Streamlit Dashboard)
Features:
Displays full electricity dataset
Shows detected fraud cases
Allows real-time fraud prediction
User Interaction:
Enter consumption value
Enter voltage value
Click “Run Detection”
View prediction result instantly
 Data Flow
SQL Database
   ↓
FastAPI (/detect, /fraud-cases, /predict)
   ↓
ML Model (Isolation Forest)
   ↓
Streamlit Dashboard
Where does the data come from?
Current Setup:
Data is synthetically generated inside Python
It simulates real electricity usage patterns
Why synthetic data?
Real utility data is not publicly available
Allows controlled testing of fraud scenarios

If we'd want to replace synthetic data:

Step 1: Replace database insertion logic

Instead of random generation, insert CSV data:

df = pd.read_csv("your_data.csv")
df.to_sql("electricity_usage", conn, if_exists="replace")
 Real-World Applications

This system can be used in:
Power Distribution Companies
Detect electricity theft
Monitor abnormal usage

Industrial Monitoring
Detect equipment failures via power anomalies

Smart Grids
Real-time monitoring of city electricity consumption

Revenue Protection
Reduce financial loss due to unauthorized usage

Key Features

✔ Full-stack ML system
✔ Real-time anomaly detection
✔ REST API architecture
✔ Interactive dashboard
✔ SQL-based data storage
✔ Extensible to real datasets

 How to Run the Project
1. Start Backend
uvicorn backend.main:app --reload
2. Run Streamlit App
streamlit run frontend/app.py
3. Access:
API: http://127.0.0.1:8000/docs
Dashboard: Streamlit UI


Limitations
Uses synthetic dataset (not real utility data)
Model is unsupervised (no labeled fraud ground truth)
Designed for learning + prototype level systems

Future Improvements
Use real smart meter datasets
Add deep learning anomaly detection
Deploy using Docker + cloud
Add authentication system

Final Note

This project demonstrates how machine learning moves from:

“model training” → “real-world system deployment”

It bridges the gap between:

Data science
Backend engineering
Product-level thinking