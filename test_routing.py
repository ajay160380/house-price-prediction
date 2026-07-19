import requests

API_KEY = "f10c50087c554ce39210d77d19ede592"
lat, lon = 12.926, 77.676
workplace = "Manyata Tech Park, Bangalore"

geo_url = f"https://api.geoapify.com/v1/geocode/search?text={requests.utils.quote(workplace)}&limit=1&apiKey={API_KEY}"
resp = requests.get(geo_url).json()
if not resp.get("features"):
    print("Geocode failed")
    exit()

dest_lon, dest_lat = resp["features"][0]["geometry"]["coordinates"]

route_url = f"https://api.geoapify.com/v1/routing?waypoints={lat},{lon}|{dest_lat},{dest_lon}&mode=drive&apiKey={API_KEY}"
route_resp = requests.get(route_url).json()
features = route_resp.get("features", [])
if features:
    props = features[0]["properties"]
    print("Distance:", props.get("distance"), "m")
    print("Time:", props.get("time"), "s")
else:
    print("Routing failed", route_resp)
