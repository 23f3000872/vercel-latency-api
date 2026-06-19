from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA = [
    {"region":"apac","latency_ms":226.51,"uptime_pct":98.819},
    {"region":"apac","latency_ms":183.58,"uptime_pct":97.669},
    {"region":"apac","latency_ms":159.7,"uptime_pct":97.488},
    {"region":"apac","latency_ms":101.52,"uptime_pct":99.29},
    {"region":"apac","latency_ms":209.27,"uptime_pct":99.149},
    {"region":"apac","latency_ms":175.37,"uptime_pct":98.566},
    {"region":"apac","latency_ms":150.81,"uptime_pct":98.456},
    {"region":"apac","latency_ms":122.39,"uptime_pct":98.149},
    {"region":"apac","latency_ms":173.45,"uptime_pct":97.672},
    {"region":"apac","latency_ms":116.77,"uptime_pct":99.331},
    {"region":"apac","latency_ms":150.35,"uptime_pct":98.239},
    {"region":"apac","latency_ms":111.29,"uptime_pct":98.425},

    {"region":"emea","latency_ms":116.81,"uptime_pct":99.143},
    {"region":"emea","latency_ms":181.38,"uptime_pct":99.123},
    {"region":"emea","latency_ms":219.44,"uptime_pct":99.134},
    {"region":"emea","latency_ms":181.14,"uptime_pct":97.286},
    {"region":"emea","latency_ms":216.52,"uptime_pct":98.811},
    {"region":"emea","latency_ms":202.39,"uptime_pct":97.229},
    {"region":"emea","latency_ms":128.33,"uptime_pct":99.179},
    {"region":"emea","latency_ms":184.59,"uptime_pct":99.223},
    {"region":"emea","latency_ms":124.22,"uptime_pct":98.187},
    {"region":"emea","latency_ms":149.54,"uptime_pct":99.19},
    {"region":"emea","latency_ms":195.28,"uptime_pct":97.829},
    {"region":"emea","latency_ms":217.76,"uptime_pct":97.595},

    {"region":"amer","latency_ms":176.61,"uptime_pct":98.924},
    {"region":"amer","latency_ms":185.24,"uptime_pct":97.427},
    {"region":"amer","latency_ms":123.4,"uptime_pct":97.141},
    {"region":"amer","latency_ms":126.83,"uptime_pct":99.155},
    {"region":"amer","latency_ms":122.49,"uptime_pct":98.344},
    {"region":"amer","latency_ms":212.57,"uptime_pct":98.421},
    {"region":"amer","latency_ms":153.22,"uptime_pct":97.457},
    {"region":"amer","latency_ms":187.47,"uptime_pct":98.302},
    {"region":"amer","latency_ms":99.44,"uptime_pct":97.25},
    {"region":"amer","latency_ms":210.05,"uptime_pct":98.107},
    {"region":"amer","latency_ms":127.66,"uptime_pct":98.444},
    {"region":"amer","latency_ms":148.0,"uptime_pct":97.825},
]

@app.post("/api/latency")
def latency(payload: dict):
    regions = payload.get("regions", [])
    threshold = payload.get("threshold_ms", 180)

    result = {}

    for region in regions:
        rows = [r for r in DATA if r["region"] == region]

        latencies = [r["latency_ms"] for r in rows]
        uptimes = [r["uptime_pct"] for r in rows]

        result[region] = {
            "avg_latency": round(sum(latencies) / len(latencies), 2),
            "p95_latency": round(float(np.percentile(latencies, 95)), 2),
            "avg_uptime": round(sum(uptimes) / len(uptimes), 3),
            "breaches": sum(1 for r in rows if r["latency_ms"] > threshold)
        }

    return result
