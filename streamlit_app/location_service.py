import os
import json
import time
from typing import Optional

import requests

from utils import cached_api_call

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "EstateAI/2.0"

LOCATIONS_FILE = os.path.join(
    os.path.dirname(__file__), '..', 'predictor', 'ml_models', 'columns.json'
)

with open(LOCATIONS_FILE) as f:
    _columns_data = json.load(f)

ALL_LOCATIONS = sorted(_columns_data['data_columns'][3:])


def get_all_locations() -> list[str]:
    return ALL_LOCATIONS


def is_valid_location(name: str) -> bool:
    return name in ALL_LOCATIONS


@cached_api_call(ttl_seconds=86400)
def geocode_location(location_name: str) -> Optional[dict]:
    query = f"{location_name}, Bengaluru, Karnataka, India"
    try:
        resp = requests.get(
            NOMINATIM_URL,
            params={"q": query, "format": "json", "limit": 1},
            headers={"User-Agent": USER_AGENT},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        if data and len(data) > 0:
            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"]),
                "display_name": data[0].get("display_name", location_name),
            }
        return None
    except requests.RequestException:
        return None


def get_bangalore_center() -> dict:
    return {"lat": 12.9716, "lon": 77.5946, "display_name": "Bengaluru, Karnataka, India"}
