import requests
import sys
from predictor.views import _parse_osm_xml

lat, lon = 12.9818, 77.5135
bbox_size = 0.012
bbox_str = f"{lon-bbox_size},{lat-bbox_size},{lon+bbox_size},{lat+bbox_size}"
url = f"https://api.openstreetmap.org/api/0.6/map?bbox={bbox_str}"
resp = requests.get(url, headers={"User-Agent": "EstateAI/2.0"}, timeout=30)
res = _parse_osm_xml(resp.content, lat, lon)
print("TOTAL:", sum(len(v) for v in res.values()) if res else 0)
print(res)
