from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "cmsdb")
DB_USER = os.getenv("DB_USER", "ngocquy")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL = os.getenv(
    "WEATHER_API_URL",
    "https://api.openweathermap.org/data/2.5/weather"
)


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/weather")
def get_weather(city: str):
    if not WEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="Missing WEATHER_API_KEY")

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(WEATHER_API_URL, params=params, timeout=15)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    city_name = data.get("name")
    country = data.get("sys", {}).get("country")
    temperature = data.get("main", {}).get("temp")
    description = data.get("weather", [{}])[0].get("description")
    icon = data.get("weather", [{}])[0].get("icon")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO search_history (city, country, temperature, description, icon)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (city_name, country, temperature, description, icon)
    )
    conn.commit()
    cur.close()
    conn.close()

    return {
        "city": city_name,
        "country": country,
        "temperature": temperature,
        "description": description,
        "icon": icon
    }


@app.get("/api/history")
def get_history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, city, country, temperature, description, icon, searched_at
        FROM search_history
        ORDER BY searched_at DESC
        LIMIT 10;
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "city": row[1],
            "country": row[2],
            "temperature": row[3],
            "description": row[4],
            "icon": row[5],
            "searched_at": str(row[6])
        })

    return {"history": result}
