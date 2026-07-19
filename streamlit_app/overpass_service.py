import time
from typing import Optional

import requests

from utils import cached_api_call, haversine

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_TIMEOUT = 90
USER_AGENT = "EstateAI/2.0"
MAX_RETRIES = 2

AMENITY_MAP = {
    "school": "school",
    "hospital": "hospital|clinic",
    "metro": "station",
    "park": "park",
    "restaurant": "restaurant",
    "mall": "mall",
    "bus_stop": "bus_stop",
}

AMENITY_DISPLAY = {
    "school": "Schools",
    "hospital": "Hospitals",
    "metro": "Metro Stations",
    "park": "Parks",
    "restaurant": "Restaurants",
    "mall": "Shopping Malls",
    "bus_stop": "Bus Stops",
}


def _build_overpass_query(lat: float, lon: float, radius: int = 1500) -> str:
    filters = []
    for category, tags in AMENITY_MAP.items():
        for tag in tags.split("|"):
            if category == "metro":
                filters.append(
                    f'  node["{tag}"~"metro|subway"](around:{radius},{lat},{lon});\n'
                    f'  way["{tag}"~"metro|subway"](around:{radius},{lat},{lon});'
                )
            elif category == "mall":
                filters.append(
                    f'  node["shop"="mall"](around:{radius},{lat},{lon});\n'
                    f'  way["shop"="mall"](around:{radius},{lat},{lon});'
                )
            elif category == "bus_stop":
                filters.append(
                    f'  node["highway"="bus_stop"](around:{radius},{lat},{lon});\n'
                    f'  way["highway"="bus_stop"](around:{radius},{lat},{lon});'
                )
            else:
                filters.append(
                    f'  node["amenity"="{tag}"](around:{radius},{lat},{lon});\n'
                    f'  way["amenity"="{tag}"](around:{radius},{lat},{lon});'
                )

    query = "[out:json];(\n" + "\n".join(filters) + "\n);out center 20;"
    return query


def _categorize_element(element: dict) -> Optional[str]:
    tags = element.get("tags", {})
    amenity = tags.get("amenity", "")
    shop = tags.get("shop", "")
    highway = tags.get("highway", "")

    if highway == "bus_stop":
        return "bus_stop"
    if shop == "mall":
        return "mall"
    if amenity == "school":
        return "school"
    if amenity in ("hospital", "clinic"):
        return "hospital"
    if amenity == "park":
        return "park"
    if amenity == "restaurant":
        return "restaurant"
    if amenity in ("station", "subway") or "metro" in str(tags):
        return "metro"
    return None


def _get_element_coords(element: dict) -> Optional[tuple[float, float]]:
    if "lat" in element and "lon" in element:
        return (element["lat"], element["lon"])
    if "center" in element:
        return (element["center"]["lat"], element["center"]["lon"])
    return None


@cached_api_call(ttl_seconds=86400)
def fetch_amenities(lat: float, lon: float, radius: int = 1500) -> list[dict]:
    query = _build_overpass_query(lat, lon, radius)

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(
                OVERPASS_URL,
                params={"data": query},
                headers={"User-Agent": USER_AGENT},
                timeout=OVERPASS_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()

            if "remark" in data and "runtime error" in str(data.get("remark", "")):
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2)
                    continue
                return []

            amenities = []
            seen = set()
            for element in data.get("elements", []):
                category = _categorize_element(element)
                if not category:
                    continue
                coords = _get_element_coords(element)
                if not coords:
                    continue
                name = element.get("tags", {}).get("name", "").strip()
                if not name:
                    continue

                dedup_key = (category, name, round(coords[0], 4), round(coords[1], 4))
                if dedup_key in seen:
                    continue
                seen.add(dedup_key)

                distance = haversine(lat, lon, coords[0], coords[1])
                amenities.append({
                    "name": name,
                    "category": category,
                    "lat": coords[0],
                    "lon": coords[1],
                    "distance_km": round(distance, 2),
                })

            amenities.sort(key=lambda x: x["distance_km"])
            return amenities

        except requests.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            return []

    return []


def get_amenities_by_category(
    lat: float, lon: float, radius: int = 1500
) -> dict[str, list[dict]]:
    all_amenities = fetch_amenities(lat, lon, radius)
    grouped = {cat: [] for cat in AMENITY_MAP}
    for a in all_amenities:
        cat = a["category"]
        if cat in grouped:
            grouped[cat].append(a)
    return grouped
