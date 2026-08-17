import os, requests
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app=FastAPI(title="Agri Intelligence Cloud")
app.mount("/static",StaticFiles(directory="app/static"),name="static")

@app.get("/")
def home(): return FileResponse("app/static/index.html")

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/api/weather")
def weather(lat:float=28.9845,lon:float=77.7064):
    u="https://power.larc.nasa.gov/api/temporal/daily/point"
    p={"parameters":"T2M,RH2M,PRECTOTCORR,WS2M","community":"AG",
       "longitude":lon,"latitude":lat,"start":"20260801","end":"20260817","format":"JSON"}
    r=requests.get(u,params=p,timeout=30); r.raise_for_status(); return r.json()

@app.get("/api/satellite")
def satellite():
    u="https://stac.dataspace.copernicus.eu/v1/search"
    p={"collections":["sentinel-2-l2a"],"bbox":[77.45,28.75,77.95,29.20],
       "datetime":"2026-08-01T00:00:00Z/2026-08-17T23:59:59Z","limit":10,
       "query":{"eo:cloud_cover":{"lte":30}},
       "sortby":[{"field":"datetime","direction":"desc"}]}
    r=requests.post(u,json=p,timeout=30); r.raise_for_status()
    return [{"id":x.get("id"),"date":x.get("properties",{}).get("datetime"),
             "cloud":x.get("properties",{}).get("eo:cloud_cover")}
            for x in r.json().get("features",[])]
