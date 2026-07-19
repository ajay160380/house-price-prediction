import requests
lat, lon = 12.9818, 77.5135
bbox_size = 0.012
bbox_str = f"{lon-bbox_size},{lat-bbox_size},{lon+bbox_size},{lat+bbox_size}"
url = f"https://api.openstreetmap.org/api/0.6/map?bbox={bbox_str}"
try:
    resp = requests.get(url, headers={"User-Agent": "EstateAI/2.0"}, timeout=30)
    print(resp.status_code, len(resp.content))
except Exception as e:
    print(e)
