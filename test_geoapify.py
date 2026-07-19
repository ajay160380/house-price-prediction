import requests
import json

API_KEY = "f10c50087c554ce39210d77d19ede592"
lat = 12.926
lon = 77.676
categories = "education.school,healthcare.hospital,public_transport.subway,leisure.park,catering.restaurant,commercial.shopping_mall,public_transport.bus"
url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},2000&limit=50&apiKey={API_KEY}"

try:
    resp = requests.get(url)
    data = resp.json()
    for feature in data.get("features", [])[:5]:
        props = feature.get("properties", {})
        print(props.get("name"), props.get("categories"))
except Exception as e:
    print("Error:", e)
