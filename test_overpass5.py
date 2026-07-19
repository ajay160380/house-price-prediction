import requests
endpoint = "https://overpass-api.de/api/interpreter"
lat, lon = 13.1007, 77.5963
bbox = f"({lat-0.015},{lon-0.015},{lat+0.015},{lon+0.015})"
queries = [
    f'node["amenity"="school"]{bbox};',
    f'way["amenity"="school"]{bbox};',
]
full_query = f"[out:json][timeout:25];(\n" + "\n".join(queries) + f"\n);out center 150;"
try:
    resp = requests.post(endpoint, data={"data": full_query}, headers={"User-Agent": "EstateAI/2.0"}, timeout=30)
    data = resp.json()
    print("Found items:", len(data.get("elements", [])))
    print("Sample:", data.get("elements")[:2] if data.get("elements") else None)
except Exception as e:
    print("Error:", e)
