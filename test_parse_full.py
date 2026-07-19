import xml.etree.ElementTree as ET
import io
import requests
import math

CATEGORY_ORDER = ["school", "hospital", "metro", "park", "restaurant", "mall", "bus_stop"]

def _categorize_osm_element(tags):
    amenity = tags.get("amenity", "")
    shop = tags.get("shop", "")
    leisure = tags.get("leisure", "")
    highway = tags.get("highway", "")
    station = tags.get("station", "")
    railway = tags.get("railway", "")
    name = tags.get("name", "")

    if amenity == "school": return "school"
    if amenity in ("hospital", "clinic"): return "hospital"
    if amenity == "restaurant": return "restaurant"
    if shop == "mall": return "mall"
    if leisure == "park": return "park"
    if highway == "bus_stop": return "bus_stop"
    if station and ("metro" in station.lower() or "subway" in station.lower()): return "metro"
    if railway == "station" and "metro" in name.lower(): return "metro"
    return None

def _haversine(lat1, lon1, lat2, lon2):
    return 1.0 # mock

def _parse_osm_xml(xml_bytes, target_lat, target_lon):
    node_coords = {}
    node_tags = {}
    relevant_keys = {"amenity", "shop", "leisure", "highway", "station", "railway", "name"}
    with io.BytesIO(xml_bytes) as f:
        for event, elem in ET.iterparse(f, events=("end",)):
            if elem.tag == "node":
                node_id = elem.get("id")
                tags = {child.get("k"): child.get("v") for child in elem.findall("tag") if child.get("k") in relevant_keys}
                if tags:
                    try:
                        node_coords[node_id] = (float(elem.get("lat")), float(elem.get("lon")))
                        node_tags[node_id] = tags
                    except: pass
            elif elem.tag == "way":
                tags = {child.get("k"): child.get("v") for child in elem.findall("tag") if child.get("k") in relevant_keys}
                if tags:
                    nd_refs = [nd.get("ref") for nd in elem.findall("nd")]
                    coords = [node_coords[ref] for ref in nd_refs if ref in node_coords]
                    if coords:
                        node_coords[f"way_{elem.get('id')}"] = (sum(c[0] for c in coords)/len(coords), sum(c[1] for c in coords)/len(coords))
                        node_tags[f"way_{elem.get('id')}"] = tags
            elem.clear()

    results = {cat: [] for cat in CATEGORY_ORDER}
    for elem_id, tags in node_tags.items():
        cat = _categorize_osm_element(tags)
        if cat and "name" in tags:
            results[cat].append(tags["name"])
    return results

lat, lon = 12.9818, 77.5135
bbox_size = 0.012
bbox_str = f"{lon-bbox_size},{lat-bbox_size},{lon+bbox_size},{lat+bbox_size}"
url = f"https://api.openstreetmap.org/api/0.6/map?bbox={bbox_str}"
resp = requests.get(url)
res = _parse_osm_xml(resp.content, lat, lon)
print("TOTAL:", sum(len(v) for v in res.values()))
print(res)
