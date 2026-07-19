import re

with open("predictor/views.py", "r") as f:
    content = f.read()

geoapify_func = """def _fetch_via_geoapify(lat, lon):
    api_key = "f10c50087c554ce39210d77d19ede592"
    categories = "education.school,healthcare,public_transport.subway,leisure.park,catering.restaurant,commercial.shopping_mall,public_transport.bus"
    url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},2000&limit=50&apiKey={api_key}"
    
    logger.info(f"Fetching Geoapify for ({lat}, {lon})")
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        
        results = {cat: [] for cat in CATEGORY_ORDER}
        seen = set()
        
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            cats = props.get("categories", [])
            
            my_cat = None
            if "education.school" in cats: my_cat = "school"
            elif "healthcare.hospital" in cats or "healthcare.clinic" in cats or "healthcare" in cats: my_cat = "hospital"
            elif "public_transport.subway" in cats: my_cat = "metro"
            elif "leisure.park" in cats: my_cat = "park"
            elif "catering.restaurant" in cats or "catering" in cats: my_cat = "restaurant"
            elif "commercial.shopping_mall" in cats: my_cat = "mall"
            elif "public_transport.bus" in cats or "public_transport.platform" in cats: my_cat = "bus_stop"
            
            if not my_cat: continue
            
            name = props.get("name")
            if not name: continue
            
            coords = feature.get("geometry", {}).get("coordinates", [])
            if len(coords) < 2: continue
            flon, flat = coords[0], coords[1]
            
            dedup = (my_cat, name, round(flat, 3), round(flon, 3))
            if dedup in seen: continue
            seen.add(dedup)
            
            dist = round(_haversine(lat, lon, flat, flon), 2)
            results[my_cat].append({
                "name": name,
                "category": my_cat,
                "lat": flat,
                "lon": flon,
                "distance_km": dist
            })
            
        for cat in CATEGORY_ORDER:
            results[cat].sort(key=lambda x: x["distance_km"])
            
        total = sum(len(v) for v in results.values())
        if total > 0:
            return results
    except Exception as e:
        logger.warning(f"Geoapify API failed: {e}")
        
    return None

"""

# Replace the Overpass call
content = content.replace("logger.info(f\"Fetching amenities for ({lat}, {lon}) via Overpass...\")", "logger.info(f\"Fetching amenities for ({lat}, {lon}) via Geoapify...\")")
content = content.replace("results = _fetch_via_overpass(lat, lon)", "results = _fetch_via_geoapify(lat, lon)")

# Insert the new function right before _fetch_via_overpass
content = content.replace("def _fetch_via_overpass(lat, lon):", geoapify_func + "\n\ndef _fetch_via_overpass(lat, lon):")

with open("predictor/views.py", "w") as f:
    f.write(content)
