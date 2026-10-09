import os
import pyodbc
from fastapi import FastAPI
from pydantic import BaseModel, Field


CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost,1433;DATABASE=DormCast;"
    f"UID=sa;PWD={os.environ['DB_PASSWORD']};TrustServerCertificate=yes"
)


def get_connection():
    return pyodbc.connect(CONN_STR)


app = FastAPI(
    title = "DormCast API",
    description = "Weather station API for temperature and humidity readings.",
    version = "0.1.0"
)

class WeatherReading(BaseModel):
    temperature: float = Field(ge = -50, le = 100)
    humidity: float = Field(ge = 0, le = 100)



@app.post("/readings")
def create_reading(reading: WeatherReading):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO Readings (Temperature, Humidity) VALUES (?, ?)",
            reading.temperature, reading.humidity,
        )
        conn.commit()
    finally:
        conn.close()
    return {"message": "Reading received successfully."}


@app.get("/readings/latest")
def get_latest_reading():
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT TOP 1 Temperature, Humidity, RecordedAt FROM Readings ORDER BY Id DESC"
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        return {"message": "No readings available."}
    return {
        "temperature": row.Temperature,
        "humidity": row.Humidity,
        "timestamp": row.RecordedAt.isoformat(),
    }


@app.get("/readings")
def get_readings(limit: int = 100):
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT TOP (?) Temperature, Humidity, RecordedAt FROM Readings ORDER BY Id DESC",
            limit,
        ).fetchall()
    finally:
        conn.close()
    return [
        {
            "temperature": r.Temperature,
            "humidity": r.Humidity,
            "timestamp": r.RecordedAt.isoformat(),
        }
        for r in rows
    ]