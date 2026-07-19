import xml.etree.ElementTree as ET
import io
import requests

lat, lon = 12.9818, 77.5135
bbox_size = 0.012
bbox_str = f"{lon-bbox_size},{lat-bbox_size},{lon+bbox_size},{lat+bbox_size}"
url = f"https://api.openstreetmap.org/api/0.6/map?bbox={bbox_str}"
resp = requests.get(url)
xml_bytes = resp.content

relevant_keys = {"amenity", "shop", "leisure", "highway", "station", "railway", "name"}
found_amenities = []
with io.BytesIO(xml_bytes) as f:
    for event, elem in ET.iterparse(f, events=("end",)):
        if elem.tag == "node":
            tags = {child.get("k"): child.get("v") for child in elem.findall("tag") if child.get("k") in relevant_keys}
            if tags and tags.get("name"):
                if any(k in tags for k in ["amenity", "shop", "leisure", "highway", "station", "railway"]):
                    found_amenities.append(tags)
        elem.clear()

print("Found amenities with names:", len(found_amenities))
print("Sample:", found_amenities[:5])
