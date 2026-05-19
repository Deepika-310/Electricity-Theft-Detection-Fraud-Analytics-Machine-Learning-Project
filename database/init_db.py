import random
from datetime import datetime, timedelta
from database.db import get_connection

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(BASE_DIR, "schema.sql")
    with open(schema_path, "r") as f:
        cursor.execute(f.read())

    base_time = datetime.now()

    for i in range(300):
        meter_id = f"M{i % 5}"
        timestamp = base_time - timedelta(hours=i)

        # Normal behavior
        consumption = random.uniform(10, 20)

        # Inject anomaly (fraud-like spike)
        if random.random() < 0.08:
            consumption = random.uniform(45, 70)

        voltage = random.uniform(210, 240)

        cursor.execute(
            """
            INSERT INTO electricity_usage (meter_id, timestamp, voltage, consumption)
            VALUES (?, ?, ?, ?)
            """,
            (meter_id, timestamp, voltage, consumption)
        )

    conn.commit()
    conn.close()

    print("Database initialized.")

if __name__ == "__main__":
    initialize_database()