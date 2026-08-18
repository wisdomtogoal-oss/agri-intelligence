import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="Agri Intelligence Cloud")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/weather")
def weather(lat: float = 28.9845, lon: float = 77.7064):
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M,RH2M,PRECTOTCORR,WS2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": "20260801",
        "end": "20260817",
        "format": "JSON"
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

@app.get("/api/satellite")
def satellite():
    url = "https://stac.dataspace.copernicus.eu/v1/search"
    payload = {
        "collections": ["sentinel-2-l2a"],
        "bbox": [77.45, 28.75, 77.95, 29.20],
        "datetime": "2026-08-01T00:00:00Z/2026-08-17T23:59:59Z",
        "limit": 10,
        "query": {"eo:cloud_cover": {"lte": 30}},
        "sortby": [{"field": "datetime", "direction": "desc"}]
    }
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    return [{"id": x.get("id"),
             "date": x.get("properties", {}).get("datetime"),
             "cloud": x.get("properties", {}).get("eo:cloud_cover")}
            for x in r.json().get("features", [])]
