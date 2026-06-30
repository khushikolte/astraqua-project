import os
import requests
import streamlit as st

API_BASE_URL = os.environ.get("AQFM_API_URL", "http://localhost:8000")


@st.cache_data(ttl=2, show_spinner=False)
def predict_from_controls(scenario: str, wifi: float, gps: float, battery: float, fleet_size: int):
    """
    Calls the FastAPI backend instead of loading the model file directly.
    Cached briefly so repeated reruns with identical slider values don't
    hammer the API, but updates quickly when the user moves a slider.
    """
    payload = {
        "wifi": wifi,
        "gps": gps,
        "battery": battery,
        "fleet_size": fleet_size,
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/predict/{scenario}/from-controls",
            json=payload,
            timeout=5,
        )
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.ConnectionError:
        return None, f"Could not reach the AQFM API at {API_BASE_URL}. Is the backend running?"
    except requests.exceptions.RequestException as e:
        return None, f"API error: {e}"


def check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None