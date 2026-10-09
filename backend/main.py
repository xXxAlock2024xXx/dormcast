from datetime import datetime, timezone
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title = "DormCast API",
    description = "Weather station API for temperature and humidity readings.",
    version = "0.1.0"
)

class WeatherReading(BaseModel):
    temperature: float = Field(ge = -50, le = 100)
    humidity: float = Field(ge = 0, le = 100)

latest_reading: dict | None = None

@app.get("/")
def root():
    return {"message": "Welcome to the DormCast API!"}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/readings")
def create_reading(reading: WeatherReading):
    global latest_reading

    latest_reading = {
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return {"message": "Reading received successfully.", "reading": latest_reading}

@app.get("/readings/latest")
def get_latest_reading():
    if latest_reading is None:
        return {"message": "No readings available."}
    return latest_reading
