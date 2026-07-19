import requests
endpoint = "https://overpass-api.de/api/interpreter"
query = "[out:json][timeout:10];node(12.96,77.49,12.99,77.52);out center 5;"
try:
    resp = requests.post(endpoint, data={"data": query}, headers={"User-Agent": "EstateAI/2.0"}, timeout=10)
    print(resp.status_code, resp.content[:200])
except Exception as e:
    print(e)
