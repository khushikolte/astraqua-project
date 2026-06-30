import os
from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

MODEL_DIR = os.environ.get("AQFM_MODEL_DIR", "models")

MODEL_FILES = {
    "gps_lost": "gps_lost.pt",
    "comms_down": "comms_down.pt",
    "battery_critical": "battery_critical.pt",
}

PILLAR_NAMES = [
    "GPS-Denied Operation",
    "Multi-Agent Coordination",
    "Edge AI Decision Making",
    "Predictive Maintenance",
]

models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    for name, filename in MODEL_FILES.items():
        path = os.path.join(MODEL_DIR, filename)
        if not os.path.exists(path):
            raise RuntimeError(f"Model file not found: {path}")
        model = torch.jit.load(path)
        model.eval()
        models[name] = model
    print(f"Loaded {len(models)} models: {list(models.keys())}")
    yield
    models.clear()


app = FastAPI(title="AQFM Scenario API", version="1.0.0", lifespan=lifespan)

# Allow the WordPress site / Streamlit app to call this from a browser.
# Lock this down to your real domain(s) before going live.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class FleetState(BaseModel):
    # 32-dim vector. If you'd rather send named fields (wifi, gps, battery, etc.)
    # add a /predict/from-controls endpoint that builds this vector server-side —
    # see the version below.
    vector: list[float] = Field(..., min_length=32, max_length=32)


class PredictionResponse(BaseModel):
    scenario: str
    confidences: dict[str, float]
    raw: list[float]


class ControlState(BaseModel):
    wifi: float = Field(100, ge=0, le=100)
    gps: float = Field(100, ge=0, le=100)
    battery: float = Field(90, ge=0, le=100)
    fleet_size: int = Field(5, ge=1, le=8)


def vector_from_controls(state: ControlState) -> list[float]:
    """
    Turns the dashboard's simple sliders into the 32-dim input vector
    the model expects. This mirrors the structure used in generate_data.py:
    idx 0-3 = GPS channels, 4-7 = comms channels, 8-15 = battery channels,
    16-31 = filled with neutral noise for the remaining sensors.
    """
    import random

    vec = [random.random() for _ in range(32)]

    gps_level = state.gps / 100
    wifi_level = state.wifi / 100
    battery_level = state.battery / 100

    for i in range(0, 4):
        vec[i] = gps_level
    for i in range(4, 8):
        vec[i] = wifi_level
    for i in range(8, 16):
        vec[i] = battery_level

    return vec


@app.get("/health")
def health():
    return {"status": "ok", "models_loaded": list(models.keys())}


@app.get("/scenarios")
def list_scenarios():
    return {"scenarios": list(models.keys())}


@app.post("/predict/{scenario}", response_model=PredictionResponse)
def predict(scenario: str, state: FleetState):
    if scenario not in models:
        raise HTTPException(status_code=404, detail=f"Unknown scenario '{scenario}'")

    x = torch.tensor([state.vector], dtype=torch.float32)

    with torch.no_grad():
        output = models[scenario](x)[0].tolist()

    return PredictionResponse(
        scenario=scenario,
        confidences=dict(zip(PILLAR_NAMES, output)),
        raw=output,
    )


@app.post("/predict/{scenario}/from-controls", response_model=PredictionResponse)
def predict_from_controls(scenario: str, controls: ControlState):
    if scenario not in models:
        raise HTTPException(status_code=404, detail=f"Unknown scenario '{scenario}'")

    vec = vector_from_controls(controls)
    x = torch.tensor([vec], dtype=torch.float32)

    with torch.no_grad():
        output = models[scenario](x)[0].tolist()

    return PredictionResponse(
        scenario=scenario,
        confidences=dict(zip(PILLAR_NAMES, output)),
        raw=output,
    )