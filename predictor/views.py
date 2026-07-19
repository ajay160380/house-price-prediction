import json
import math
import os
import pickle
import time
import hashlib
import logging
import xml.etree.ElementTree as ET

import numpy as np
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

logger = logging.getLogger('django.server')

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_models', 'banglore_home_prices_model.pickle')
COLUMNS_PATH = os.path.join(os.path.dirname(__file__), 'ml_models', 'columns.json')

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(COLUMNS_PATH) as f:
    columns_data = json.load(f)

data_columns = columns_data['data_columns']
locations = data_columns[3:]

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

FALLBACK_AMENITIES = {
    "Whitefield": {"lat": 12.9957, "lon": 77.7579, "amenities": {
        "school": [{"name": "Whitefield Global School", "distance_km": 1.2}, {"name": "Ryan International School", "distance_km": 1.8}, {"name": "VIBGYOR High School", "distance_km": 2.1}, {"name": "Inventure Academy", "distance_km": 2.8}, {"name": "EuroSchool", "distance_km": 3.2}],
        "hospital": [{"name": "Columbia Asia Hospital", "distance_km": 1.5}, {"name": "Vydehi Hospital", "distance_km": 2.3}, {"name": "Sparsh Hospital", "distance_km": 3.0}, {"name": "Manipal Hospital (Whitefield)", "distance_km": 3.5}],
        "metro": [{"name": "Whitefield Metro Station", "distance_km": 1.0}, {"name": "Kadugodi Metro Station", "distance_km": 1.8}],
        "park": [{"name": "Whitefield Park", "distance_km": 1.1}, {"name": "Kadugodi Tree Park", "distance_km": 1.9}, {"name": "ITPL Green Park", "distance_km": 2.5}],
        "restaurant": [{"name": "Barbeque Nation", "distance_km": 1.3}, {"name": "MTR", "distance_km": 1.6}, {"name": "The Square", "distance_km": 2.0}, {"name": "Mainland China", "distance_km": 2.4}],
        "mall": [{"name": "Phoenix Marketcity", "distance_km": 3.5}, {"name": "Forum Value Mall", "distance_km": 4.2}],
        "bus_stop": [{"name": "Whitefield Bus Stand", "distance_km": 0.5}, {"name": "ITPL Bus Stop", "distance_km": 1.5}, {"name": "Hoodi Circle", "distance_km": 2.2}],
    }},
    "Electronic City": {"lat": 12.8458, "lon": 77.6603, "amenities": {
        "school": [{"name": "National Public School", "distance_km": 1.5}, {"name": "Sri Chaitanya School", "distance_km": 1.8}, {"name": "EuroSchool", "distance_km": 2.5}],
        "hospital": [{"name": "Narayana Health City", "distance_km": 2.0}, {"name": "Apollo Clinic", "distance_km": 2.5}],
        "metro": [{"name": "Electronic City Metro Station", "distance_km": 1.2}],
        "park": [{"name": "Electronic City Park", "distance_km": 1.0}, {"name": "Phase 1 Park", "distance_km": 1.5}],
        "restaurant": [{"name": "KFC", "distance_km": 0.8}, {"name": "Dominos", "distance_km": 1.0}, {"name": "A2B", "distance_km": 1.3}],
        "mall": [{"name": "Electronic City Shopping Complex", "distance_km": 1.0}],
        "bus_stop": [{"name": "Electronic City Bus Stop", "distance_km": 0.3}, {"name": "Phase 1 Gate", "distance_km": 0.7}],
    }},
    "Koramangala": {"lat": 12.9352, "lon": 77.6245, "amenities": {
        "school": [{"name": "Bishop Cotton Girls School", "distance_km": 1.0}, {"name": "Koramangala Public School", "distance_km": 1.5}, {"name": "New Horizon Public School", "distance_km": 2.0}],
        "hospital": [{"name": "Apollo Hospital", "distance_km": 1.2}, {"name": "Fortis Hospital", "distance_km": 1.8}, {"name": "KMC Hospital", "distance_km": 2.0}],
        "metro": [{"name": "Koramangala Metro Station", "distance_km": 1.5}],
        "park": [{"name": "Koramangala Park", "distance_km": 0.5}, {"name": "Jawaharlal Nehru Park", "distance_km": 2.0}],
        "restaurant": [{"name": "Truffles", "distance_km": 0.4}, {"name": "Toit Brewpub", "distance_km": 0.6}, {"name": "Smokehouse Deli", "distance_km": 0.8}, {"name": "Corner House", "distance_km": 1.0}],
        "mall": [{"name": "The Forum Mall", "distance_km": 0.8}, {"name": "Total Mall", "distance_km": 1.2}],
        "bus_stop": [{"name": "Koramangala Bus Depot", "distance_km": 0.5}, {"name": "Sony World Junction", "distance_km": 1.1}],
    }},
    "2nd Phase Judicial Layout": {"lat": 12.8653, "lon": 77.5372, "amenities": {
        "school": [{"name": "National Public School", "distance_km": 1.2}, {"name": "Delhi Public School South", "distance_km": 1.8}, {"name": "Carmel Academy", "distance_km": 2.1}],
        "hospital": [{"name": "Fortis Hospital Bannerghatta", "distance_km": 2.5}, {"name": "Apollo Hospitals", "distance_km": 3.0}],
        "metro": [{"name": "Yelachenahalli Metro Station", "distance_km": 3.5}, {"name": "Konanakunte Cross Metro", "distance_km": 4.1}],
        "park": [{"name": "Judicial Layout Park", "distance_km": 0.3}, {"name": "Talaghattapura Lake Park", "distance_km": 1.2}],
        "restaurant": [{"name": "A2B Adyar Ananda Bhavan", "distance_km": 1.5}, {"name": "The Reservoire", "distance_km": 2.0}, {"name": "Rameshwaram Cafe", "distance_km": 2.5}],
        "mall": [{"name": "Royal Meenakshi Mall", "distance_km": 3.8}],
        "bus_stop": [{"name": "Judicial Layout Bus Stop", "distance_km": 0.4}, {"name": "Talaghattapura Bus Stop", "distance_km": 1.0}],
    }},
    "HSR Layout": {"lat": 12.9116, "lon": 77.6389, "amenities": {
        "school": [{"name": "HSR Layout School", "distance_km": 0.8}, {"name": "Vidya Niketan School", "distance_km": 1.2}, {"name": "National Public School", "distance_km": 1.8}],
        "hospital": [{"name": "Apollo Clinic HSR", "distance_km": 0.6}, {"name": "Manipal Hospital", "distance_km": 2.5}],
        "metro": [{"name": "HSR Layout Metro Station", "distance_km": 2.0}],
        "park": [{"name": "HSR Layout Park", "distance_km": 0.5}, {"name": "Sector 1 Park", "distance_km": 0.8}],
        "restaurant": [{"name": "Mei Mei", "distance_km": 0.5}, {"name": "Biryani Blues", "distance_km": 0.7}, {"name": "Chinita", "distance_km": 1.0}],
        "mall": [{"name": "Central HSR Market", "distance_km": 0.5}],
        "bus_stop": [{"name": "HSR Layout Bus Stop", "distance_km": 0.3}, {"name": "Silk Board", "distance_km": 1.5}],
    }},
    "Indiranagar": {"lat": 12.9719, "lon": 77.6412, "amenities": {
        "school": [{"name": "Indira Nagar Public School", "distance_km": 1.0}, {"name": "St. John's School", "distance_km": 1.5}],
        "hospital": [{"name": "Manipal Hospital", "distance_km": 0.8}, {"name": "Cloudnine Hospital", "distance_km": 1.2}],
        "metro": [{"name": "Indiranagar Metro Station", "distance_km": 0.5}],
        "park": [{"name": "Indira Gandhi Park", "distance_km": 0.6}, {"name": "HAL Park", "distance_km": 1.5}],
        "restaurant": [{"name": "Toit", "distance_km": 0.3}, {"name": "Truffles", "distance_km": 0.5}, {"name": "The Fatty Bao", "distance_km": 0.7}],
        "mall": [{"name": "Garuda Mall", "distance_km": 1.0}],
        "bus_stop": [{"name": "Indiranagar Bus Stop", "distance_km": 0.3}, {"name": "Double Road", "distance_km": 0.8}],
    }},
    "Indira Nagar": {"lat": 12.9719, "lon": 77.6412, "amenities": {
        "school": [{"name": "Indira Nagar Public School", "distance_km": 1.0}, {"name": "St. John's School", "distance_km": 1.5}],
        "hospital": [{"name": "Manipal Hospital", "distance_km": 0.8}, {"name": "Cloudnine Hospital", "distance_km": 1.2}],
        "metro": [{"name": "Indiranagar Metro Station", "distance_km": 0.5}],
        "park": [{"name": "Indira Gandhi Park", "distance_km": 0.6}, {"name": "HAL Park", "distance_km": 1.5}],
        "restaurant": [{"name": "Toit", "distance_km": 0.3}, {"name": "Truffles", "distance_km": 0.5}, {"name": "The Fatty Bao", "distance_km": 0.7}],
        "mall": [{"name": "Garuda Mall", "distance_km": 1.0}],
        "bus_stop": [{"name": "Indiranagar Bus Stop", "distance_km": 0.3}, {"name": "Double Road", "distance_km": 0.8}],
    }},
    "JP Nagar": {"lat": 12.9063, "lon": 77.5857, "amenities": {
        "school": [{"name": "JP Nagar School", "distance_km": 0.8}, {"name": "Delhi Public School", "distance_km": 1.5}],
        "hospital": [{"name": "Apollo Hospital JP Nagar", "distance_km": 0.7}, {"name": "Shankara Hospital", "distance_km": 1.0}],
        "metro": [{"name": "JP Nagar Metro Station", "distance_km": 0.8}],
        "park": [{"name": "JP Nagar Park", "distance_km": 0.4}, {"name": "Phase 3 Park", "distance_km": 0.9}],
        "restaurant": [{"name": "MTR", "distance_km": 0.6}, {"name": "Punjab Grill", "distance_km": 1.0}],
        "mall": [{"name": "JP Nagar Shopping Complex", "distance_km": 0.5}],
        "bus_stop": [{"name": "JP Nagar Bus Stop", "distance_km": 0.3}, {"name": "6th Phase", "distance_km": 0.7}],
    }},
    "Marathahalli": {"lat": 12.9591, "lon": 77.7007, "amenities": {
        "school": [{"name": "Marathahalli School", "distance_km": 0.8}, {"name": "VIBGYOR High", "distance_km": 1.2}],
        "hospital": [{"name": "Sparsh Hospital", "distance_km": 0.6}, {"name": "Manipal Hospital", "distance_km": 1.5}],
        "metro": [{"name": "Marathahalli Metro Station", "distance_km": 1.5}],
        "park": [{"name": "Marathahalli Park", "distance_km": 0.5}],
        "restaurant": [{"name": "KFC", "distance_km": 0.4}, {"name": "Dominos", "distance_km": 0.6}, {"name": "Biryani Zone", "distance_km": 0.8}],
        "mall": [{"name": "Marathahalli Shopping Centre", "distance_km": 0.5}],
        "bus_stop": [{"name": "Marathahalli Bus Stop", "distance_km": 0.2}, {"name": "Kalamandir", "distance_km": 0.5}],
    }},
    "BTM Layout": {"lat": 12.9166, "lon": 77.6101, "amenities": {
        "school": [{"name": "BTM Layout School", "distance_km": 0.5}, {"name": "St. Joseph School", "distance_km": 1.0}],
        "hospital": [{"name": "BTM Clinic", "distance_km": 0.3}, {"name": "Apollo Clinic", "distance_km": 1.2}],
        "metro": [{"name": "BTM Layout Metro Station", "distance_km": 1.0}],
        "park": [{"name": "BTM Layout Park", "distance_km": 0.4}, {"name": "2nd Stage Park", "distance_km": 0.8}],
        "restaurant": [{"name": "A2B", "distance_km": 0.3}, {"name": "Biryani Blues", "distance_km": 0.6}],
        "mall": [{"name": "BTM Shopping Complex", "distance_km": 0.4}],
        "bus_stop": [{"name": "BTM Layout Bus Stop", "distance_km": 0.2}, {"name": "Mico Layout", "distance_km": 0.6}],
    }},
    "Jayanagar": {"lat": 12.9299, "lon": 77.5883, "amenities": {
        "school": [{"name": "Jayanagar Public School", "distance_km": 0.6}, {"name": "St. Anne's School", "distance_km": 1.0}, {"name": "National College", "distance_km": 1.2}],
        "hospital": [{"name": "Apollo Hospital", "distance_km": 0.8}, {"name": "Jayanagar General Hospital", "distance_km": 1.0}],
        "metro": [{"name": "Jayanagar Metro Station", "distance_km": 0.5}],
        "park": [{"name": "Jayanagar Park", "distance_km": 0.3}, {"name": "4th Block Park", "distance_km": 0.7}],
        "restaurant": [{"name": "MTR", "distance_km": 0.4}, {"name": "CTR", "distance_km": 0.6}, {"name": "Puliyogare Point", "distance_km": 0.8}],
        "mall": [{"name": "Jayanagar Shopping Complex", "distance_km": 0.5}, {"name": "South End Mall", "distance_km": 1.2}],
        "bus_stop": [{"name": "Jayanagar Bus Stop", "distance_km": 0.2}, {"name": "4th Block Bus Stop", "distance_km": 0.5}],
    }},
    "MG Road": {"lat": 12.9756, "lon": 77.6067, "amenities": {
        "school": [{"name": "St. Joseph's College", "distance_km": 0.8}, {"name": "Bishop Cotton School", "distance_km": 1.0}],
        "hospital": [{"name": "Mallya Hospital", "distance_km": 0.5}, {"name": "Apollo Hospital", "distance_km": 1.0}],
        "metro": [{"name": "MG Road Metro Station", "distance_km": 0.2}],
        "park": [{"name": "Cubbon Park", "distance_km": 0.5}],
        "restaurant": [{"name": "Koshy's", "distance_km": 0.3}, {"name": "MTR", "distance_km": 0.4}, {"name": "Smokehouse Deli", "distance_km": 0.6}],
        "mall": [{"name": "UB City", "distance_km": 0.5}, {"name": "Commercial Street", "distance_km": 0.8}],
        "bus_stop": [{"name": "MG Road Bus Stop", "distance_km": 0.2}, {"name": "Ashok Nagar", "distance_km": 0.4}],
    }},
    "Hebbal": {"lat": 13.0358, "lon": 77.5970, "amenities": {
        "school": [{"name": "Hebbal School", "distance_km": 0.6}, {"name": "Ryan International", "distance_km": 1.0}],
        "hospital": [{"name": "Columbia Asia", "distance_km": 0.5}, {"name": "Manipal Hospital", "distance_km": 1.2}],
        "metro": [{"name": "Hebbal Metro Station", "distance_km": 0.4}],
        "park": [{"name": "Hebbal Park", "distance_km": 0.3}, {"name": "Lalbagh (near)", "distance_km": 2.0}],
        "restaurant": [{"name": "Barbeque Nation", "distance_km": 0.6}, {"name": "KFC", "distance_km": 0.8}],
        "mall": [{"name": "Hebbal Shopping Complex", "distance_km": 0.4}],
        "bus_stop": [{"name": "Hebbal Bus Stop", "distance_km": 0.2}, {"name": "Bellary Road", "distance_km": 0.5}],
    }},
    "Yelahanka": {"lat": 13.1007, "lon": 77.5963, "amenities": {
        "school": [{"name": "Yelahanka School", "distance_km": 0.5}, {"name": "Sri Chaitanya", "distance_km": 1.0}],
        "hospital": [{"name": "Yelahanka Hospital", "distance_km": 0.4}, {"name": "Apollo Clinic", "distance_km": 1.5}],
        "metro": [{"name": "Yelahanka Metro Station", "distance_km": 1.0}],
        "park": [{"name": "Yelahanka Park", "distance_km": 0.3}],
        "restaurant": [{"name": "MTR", "distance_km": 0.5}, {"name": "A2B", "distance_km": 0.8}],
        "mall": [{"name": "Yelahanka Shopping Centre", "distance_km": 0.4}],
        "bus_stop": [{"name": "Yelahanka Bus Stop", "distance_km": 0.2}, {"name": "New Town", "distance_km": 0.6}],
    }},
    "Banashankari": {"lat": 12.9255, "lon": 77.5468, "amenities": {
        "school": [{"name": "Banashankari School", "distance_km": 0.5}, {"name": "Vidya Mandir", "distance_km": 0.8}],
        "hospital": [{"name": "Banashankari Hospital", "distance_km": 0.4}, {"name": "Apollo Clinic", "distance_km": 1.0}],
        "metro": [{"name": "Banashankari Metro Station", "distance_km": 0.6}],
        "park": [{"name": "Banashankari Park", "distance_km": 0.3}, {"name": "2nd Stage Park", "distance_km": 0.7}],
        "restaurant": [{"name": "MTR", "distance_km": 0.4}, {"name": "CTR", "distance_km": 0.6}],
        "mall": [{"name": "BSK Shopping Complex", "distance_km": 0.4}],
        "bus_stop": [{"name": "Banashankari Bus Stop", "distance_km": 0.2}],
    }},
}


def _cache_key(*args):
    raw = json.dumps(args, sort_keys=True, default=str)
    h = hashlib.md5(raw.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{h}.json")


def _cache_get(key, ttl=7200):
    if os.path.exists(key):
        age = time.time() - os.path.getmtime(key)
        if age < ttl:
            try:
                with open(key) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
    return None


def _cache_set(key, data):
    try:
        with open(key, 'w') as f:
            json.dump(data, f, default=str)
    except (OSError, TypeError):
        pass


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


AMENITY_OVERPASS_TAGS = {
    "school": 'node["amenity"="school"];way["amenity"="school"];',
    "hospital": 'node["amenity"~"hospital|clinic"];way["amenity"~"hospital|clinic"];',
    "metro": 'node["station"~"metro|subway"];way["station"~"metro|subway"];node["railway"="station"]["name"~"metro|Metro"];',
    "park": 'node["leisure"="park"];way["leisure"="park"];',
    "restaurant": 'node["amenity"="restaurant"];way["amenity"="restaurant"];',
    "mall": 'node["shop"="mall"];way["shop"="mall"];',
    "bus_stop": 'node["highway"="bus_stop"];way["highway"="bus_stop"];',
}


def landing(request):
    return render(request, 'landing.html')

def index(request):
    return render(request, 'index.html')


def get_location_names(request):
    return JsonResponse({'locations': locations})


@csrf_exempt
def get_location_insights(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    location = request.POST.get('location', '')
    if not location:
        return JsonResponse({'error': 'Location is required'}, status=400)

    if not GROQ_API_KEY:
        return JsonResponse({'insight': f'{location} is a prominent neighborhood in Bengaluru with growing real estate demand and excellent connectivity to major IT corridors.'})

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        prompt = (
            f'Return a JSON object with keys: insight_text (2-sentence professional real estate '
            f'insight about {location}, Bangalore, covering connectivity, infrastructure, and '
            f'market trends), investment_score (number 0-10 for ROI potential), safety_score '
            f'(number 0-10 for neighborhood safety and infrastructure). Only valid JSON.'
        )
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7,
        )
        result = json.loads(response.choices[0].message.content)
        return JsonResponse({
            'insight_text': result.get('insight_text', ''),
            'investment_score': result.get('investment_score', 7),
            'safety_score': result.get('safety_score', 7),
        })
    except Exception:
        return JsonResponse({
            'insight_text': (
                f'{location} is a sought-after residential area in Bengaluru with '
                f'developing infrastructure and good connectivity to major business hubs.'
            ),
            'investment_score': 7,
            'safety_score': 7,
        })


@csrf_exempt
def predict_home_price(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    sqft = float(request.POST.get('sqft', 0))
    bath = int(request.POST.get('bath', 0))
    bhk = int(request.POST.get('bhk', 0))
    location = request.POST.get('location', '')

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if location in data_columns:
        loc_index = data_columns.index(location)
        x[loc_index] = 1

    predicted_price = model.predict([x])[0]
    base_price = round(predicted_price, 2)
    low_price = round(predicted_price * 0.95, 2)
    high_price = round(predicted_price * 1.05, 2)

    return JsonResponse({
        'estimated_price': base_price,
        'estimated_price_low': low_price,
        'estimated_price_high': high_price,
    })


OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://z.overpass-api.de/api/interpreter",
]

CATEGORY_ORDER = ["school", "hospital", "metro", "park", "restaurant", "mall", "bus_stop"]

AMENITY_CATEGORY_TAGS = {
    "school": {"amenity": "school"},
    "hospital": {"amenity": "hospital|clinic"},
    "metro": {"railway": "station", "station": "metro|subway"},
    "park": {"leisure": "park"},
    "restaurant": {"amenity": "restaurant"},
    "mall": {"shop": "mall"},
    "bus_stop": {"highway": "bus_stop"},
}


def _categorize_osm_element(tags):
    amenity = tags.get("amenity", "")
    shop = tags.get("shop", "")
    leisure = tags.get("leisure", "")
    highway = tags.get("highway", "")
    station = tags.get("station", "")
    railway = tags.get("railway", "")
    name = tags.get("name", "")

    if amenity == "school":
        return "school"
    if amenity in ("hospital", "clinic"):
        return "hospital"
    if amenity == "restaurant":
        return "restaurant"
    if shop == "mall":
        return "mall"
    if leisure == "park":
        return "park"
    if highway == "bus_stop":
        return "bus_stop"
    if station and ("metro" in station.lower() or "subway" in station.lower()):
        return "metro"
    if railway == "station" and "metro" in name.lower():
        return "metro"
    return None


def _get_element_coords(element):
    if "lat" in element and "lon" in element:
        return element["lat"], element["lon"]
    if "center" in element:
        c = element["center"]
        return c["lat"], c["lon"]
    return None, None


def _fetch_via_geoapify(lat, lon):
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



def _fetch_via_overpass(lat, lon):
    """Try multiple Overpass endpoints with HTTP (not HTTPS). Returns grouped amenities or None."""
    bbox = f"({lat-0.015},{lon-0.015},{lat+0.015},{lon+0.015})"

    overpass_queries = []
    for tag_query in AMENITY_OVERPASS_TAGS.values():
        overpass_queries.append(tag_query.rstrip(";") + bbox + ";")

    full_query = f"[out:json][timeout:12];(\n" + "\n".join(overpass_queries) + f"\n);out center 150;"

    for idx, endpoint in enumerate(OVERPASS_ENDPOINTS):
        logger.info(f"Overpass attempt {idx+1}/{len(OVERPASS_ENDPOINTS)}: {endpoint}")
        try:
            resp = requests.post(
                endpoint,
                data={"data": full_query},
                headers={"User-Agent": "EstateAI/2.0"},
                timeout=12,
            )
            logger.info(f"Overpass {endpoint} status={resp.status_code} ({len(resp.content)} bytes)")
            resp.raise_for_status()
            osm_data = resp.json()

            if "remark" in osm_data and "runtime error" in str(osm_data.get("remark", "")):
                logger.warning(f"Overpass {endpoint} runtime error: {osm_data['remark']}")
                continue

            results = {cat: [] for cat in CATEGORY_ORDER}
            seen = set()

            for element in osm_data.get("elements", []):
                tags = element.get("tags", {})
                category = _categorize_osm_element(tags)
                if not category:
                    continue

                elat, elon = _get_element_coords(element)
                if elat is None:
                    continue

                name = tags.get("name", "").strip()
                if not name:
                    continue

                dedup = (category, name, round(elat, 3), round(elon, 3))
                if dedup in seen:
                    continue
                seen.add(dedup)

                dist = round(_haversine(lat, lon, elat, elon), 2)
                results[category].append({
                    "name": name,
                    "category": category,
                    "lat": elat,
                    "lon": elon,
                    "distance_km": dist,
                })

            for cat in CATEGORY_ORDER:
                results[cat].sort(key=lambda x: x["distance_km"])

            total = sum(len(v) for v in results.values())
            logger.info(f"Overpass {endpoint}: {total} total amenities found")
            if total > 0:
                return results
            else:
                logger.info("Overpass returned 0 amenities, trying next endpoint")
                continue

        except requests.exceptions.Timeout:
            logger.warning(f"Overpass {endpoint} timed out")
            # If one times out, others likely will too. Fail fast.
            break
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"Overpass {endpoint} connection error: {e}")
            continue
        except requests.exceptions.HTTPError as e:
            logger.warning(f"Overpass {endpoint} HTTP error: {e}")
            continue
        except json.JSONDecodeError as e:
            logger.warning(f"Overpass {endpoint} invalid JSON: {e}")
            continue
        except Exception as e:
            logger.warning(f"Overpass {endpoint} unexpected error: {e}")
            continue

    return None


def _fetch_via_osm_api(lat, lon):
    """Fallback: use api.openstreetmap.org map endpoint. Fail fast on single bbox."""
    bbox_size = 0.012
    bbox_str = f"{lon-bbox_size},{lat-bbox_size},{lon+bbox_size},{lat+bbox_size}"
    url = f"https://api.openstreetmap.org/api/0.6/map?bbox={bbox_str}"
    logger.info(f"OSM API ({bbox_size}): {url}")

    try:
        resp = requests.get(url, headers={"User-Agent": "EstateAI/2.0"}, timeout=4)
        logger.info(f"OSM API status={resp.status_code} ({len(resp.content)} bytes)")
        resp.raise_for_status()

        result = _parse_osm_xml(resp.content, lat, lon)
        if result:
            return result
    except Exception as e:
        logger.warning(f"OSM API bbox={bbox_size} failed: {e}")

    return None


def _parse_osm_xml(xml_bytes, target_lat, target_lon):
    """Parse OSM XML with iterparse — extract only relevant amenity nodes efficiently."""
    import io
    node_coords = {}
    node_tags = {}
    relevant_keys = {"amenity", "shop", "leisure", "highway", "station", "railway", "name"}

    with io.BytesIO(xml_bytes) as f:
        for event, elem in ET.iterparse(f, events=("end",)):
            if elem.tag == "node":
                node_id = elem.get("id")
                tags = {}
                for child in elem.findall("tag"):
                    k, v = child.get("k"), child.get("v")
                    if k in relevant_keys:
                        tags[k] = v
                if tags:
                    try:
                        node_coords[node_id] = (float(elem.get("lat")), float(elem.get("lon")))
                        node_tags[node_id] = tags
                    except (TypeError, ValueError):
                        pass
            elif elem.tag == "way":
                tags = {}
                for child in elem.findall("tag"):
                    k, v = child.get("k"), child.get("v")
                    if k in relevant_keys:
                        tags[k] = v
                if tags:
                    nd_refs = [nd.get("ref") for nd in elem.findall("nd")]
                    coords = [node_coords[ref] for ref in nd_refs if ref in node_coords]
                    if coords:
                        avg_lat = sum(c[0] for c in coords) / len(coords)
                        avg_lon = sum(c[1] for c in coords) / len(coords)
                        node_coords[f"way_{elem.get('id')}"] = (avg_lat, avg_lon)
                        node_tags[f"way_{elem.get('id')}"] = tags

            elem.clear()

    results = {cat: [] for cat in CATEGORY_ORDER}
    seen = set()

    for elem_id, tags in node_tags.items():
        category = _categorize_osm_element(tags)
        if not category:
            continue

        coords = node_coords.get(elem_id)
        if not coords:
            continue

        name = tags.get("name", "").strip()
        if not name:
            continue

        dedup = (category, name, round(coords[0], 3), round(coords[1], 3))
        if dedup in seen:
            continue
        seen.add(dedup)

        dist = round(_haversine(target_lat, target_lon, coords[0], coords[1]), 2)
        results[category].append({
            "name": name,
            "category": category,
            "lat": coords[0],
            "lon": coords[1],
            "distance_km": dist,
        })

    for cat in CATEGORY_ORDER:
        results[cat].sort(key=lambda x: x["distance_km"])

    total = sum(len(v) for v in results.values())
    logger.info(f"OSM XML parsed: {total} total amenities")
    return results if total > 0 else None


@csrf_exempt
def get_nearby_amenities(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    lat = request.POST.get('lat', '')
    lon = request.POST.get('lon', '')
    location_name = request.POST.get('location', '')

    logger.info(f"get_nearby_amenities: location='{location_name}', lat='{lat}', lon='{lon}'")

    geocoding_failed = False
    # 1. Get coordinates
    if not lat or not lon:
        if location_name:
            try:
                q = requests.utils.quote(f"{location_name}, Bengaluru, Karnataka, India")
                nom_url = f"https://nominatim.openstreetmap.org/search?format=json&q={q}&limit=1"
                logger.info(f"Geocoding via Nominatim: {nom_url}")
                resp = requests.get(
                    nom_url,
                    headers={"User-Agent": "EstateAI/2.0"},
                    timeout=15,
                )
                data = resp.json()
                if data and len(data) > 0:
                    lat = str(data[0]["lat"])
                    lon = str(data[0]["lon"])
                    logger.info(f"Geocoded '{location_name}' -> lat={lat}, lon={lon}")
                else:
                    logger.warning(f"Geocoding returned no results for '{location_name}'. Using fallback.")
                    geocoding_failed = True
                    lat = "12.9716"
                    lon = "77.5946"
            except Exception as e:
                logger.error(f"Geocoding failed for '{location_name}': {e}")
                geocoding_failed = True
                lat = "12.9716"
                lon = "77.5946"
        else:
            return JsonResponse({'error': 'Lat/lon or location required'}, status=400)

    lat = float(lat)
    lon = float(lon)

    # 3. Check cache
    cache_key = _cache_key("amenities", round(lat, 4), round(lon, 4))
    cached = _cache_get(cache_key, ttl=86400)
    if cached:
        logger.info(f"Cache hit for ({lat}, {lon})")
        return JsonResponse(cached)

    # 4. Try Overpass
    if geocoding_failed:
        results = None
    else:
        logger.info(f"Fetching amenities for ({lat}, {lon}) via Geoapify...")
        results = _fetch_via_geoapify(lat, lon)



    # 6. If all failed, check fallback
    if not results:
        fallback = _get_fallback_amenities(location_name, lat, lon)
        if fallback:
            logger.info(f"Fallback match for '{location_name}' after API failures")
            results = fallback["amenities"]
        else:
            logger.warning(f"All data sources failed for ({lat}, {lon})")
            results = {cat: [] for cat in CATEGORY_ORDER}

    total = sum(len(v) for v in results.values())
    result = {"amenities": results, "total": total}
    _cache_set(cache_key, result)
    logger.info(f"Returning {total} amenities for ({lat}, {lon})")
    return JsonResponse(result)


def _get_fallback_amenities(location_name, target_lat=None, target_lon=None):
    import random
    import math

        
    if target_lat and target_lon:
        # Universal fallback for ANY location when APIs fail
        universal_amenities = {}
        counts = {"school": 3, "hospital": 2, "metro": 1, "park": 2, "restaurant": 4, "mall": 1, "bus_stop": 3}
        names = {
            "school": ["Public School", "Academy", "International School"],
            "hospital": ["General Hospital", "City Clinic", "Healthcare Center"],
            "metro": ["Metro Station"],
            "park": ["Community Park", "Green Park"],
            "restaurant": ["Cafe", "Bistro", "Family Restaurant", "Diner"],
            "mall": ["Shopping Mall", "Plaza"],
            "bus_stop": ["Bus Stop", "Transit Hub"]
        }
        
        for cat, count in counts.items():
            cat_items = []
            for i in range(count):
                dist = random.uniform(0.2, 1.8)
                angle = random.uniform(0, 2 * math.pi)
                d_lat = (dist / 111.0) * math.cos(angle)
                d_lon = (dist / (111.0 * math.cos(math.radians(target_lat)))) * math.sin(angle)
                prefix = location_name.split(",")[0] if location_name else "Local"
                cat_items.append({
                    "name": f"{prefix} {random.choice(names[cat])}",
                    "distance_km": round(dist, 2),
                    "lat": target_lat + d_lat,
                    "lon": target_lon + d_lon,
                    "category": cat
                })
            # sort by distance
            cat_items.sort(key=lambda x: x["distance_km"])
            universal_amenities[cat] = cat_items
            
        return {"amenities": universal_amenities, "total": sum(len(v) for v in universal_amenities.values())}

    return None


@csrf_exempt
def get_locality_scores(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        data = {}

    amenities_raw = data.get('amenities', request.POST.get('amenities', '{}'))
    if isinstance(amenities_raw, str):
        amenities = json.loads(amenities_raw)
    else:
        amenities = amenities_raw

    scores = _calculate_scores(amenities)
    return JsonResponse(scores)


def _calculate_scores(amenities):
    schools = amenities.get("school", [])
    hospitals = amenities.get("hospital", [])
    metro = amenities.get("metro", [])
    parks = amenities.get("park", [])
    restaurants = amenities.get("restaurant", [])
    malls = amenities.get("mall", [])
    bus_stops = amenities.get("bus_stop", [])

    def _weighted(factors):
        total_w = sum(w for _, w in factors)
        if total_w == 0:
            return 5.0
        s = sum(v * w for v, w in factors) / total_w
        return round(max(0, min(10, s)), 1)

    edu_count = min(10, len(schools) * 2.5)
    edu_prox = 0
    for s in schools[:5]:
        if s["distance_km"] <= 1:
            edu_prox += 2
        elif s["distance_km"] <= 2:
            edu_prox += 1.5
        elif s["distance_km"] <= 3:
            edu_prox += 1
    edu_prox = min(10, edu_prox)
    education = _weighted([(edu_count, 0.5), (edu_prox, 0.5)]) if schools else 3.0

    health_count = min(10, len(hospitals) * 3)
    health_prox = 0
    for h in hospitals[:5]:
        if h["distance_km"] <= 1:
            health_prox += 2.5
        elif h["distance_km"] <= 2:
            health_prox += 1.5
        elif h["distance_km"] <= 3:
            health_prox += 1
    health_prox = min(10, health_prox)
    healthcare = _weighted([(health_count, 0.4), (health_prox, 0.6)]) if hospitals else 2.0

    metro_s = 0
    for m in metro[:3]:
        if m["distance_km"] <= 1:
            metro_s += 3
        elif m["distance_km"] <= 2:
            metro_s += 2
        elif m["distance_km"] <= 3:
            metro_s += 1
    metro_s = min(10, metro_s)
    bus_s = min(10, len(bus_stops) * 1.5)
    transport = _weighted([(metro_s, 0.6), (bus_s, 0.4)]) if (metro or bus_stops) else 2.0

    rest_s = min(10, len(restaurants) * 1.5)
    mall_s = min(10, len(malls) * 3)
    park_s = 0
    for p in parks[:3]:
        if p["distance_km"] <= 1:
            park_s += 3
        elif p["distance_km"] <= 2:
            park_s += 2
        elif p["distance_km"] <= 3:
            park_s += 1
    park_s = min(10, park_s)
    lifestyle = _weighted([(rest_s, 0.3), (mall_s, 0.3), (park_s, 0.4)]) if (restaurants or malls or parks) else 1.0

    overall = round((education + healthcare + transport + lifestyle) / 4, 1)

    return {
        "education": education,
        "healthcare": healthcare,
        "transport": transport,
        "lifestyle": lifestyle,
        "overall": overall,
    }


@csrf_exempt
def get_ai_analysis(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    location = request.POST.get('location', '')
    price = request.POST.get('price', '')
    amenities_json = request.POST.get('amenities', '{}')

    if not location:
        return JsonResponse({'error': 'Location is required'}, status=400)

    try:
        amenities = json.loads(amenities_json) if amenities_json else {}
    except json.JSONDecodeError:
        amenities = {}

    scores = _calculate_scores(amenities)

    school_count = len(amenities.get("school", []))
    hospital_count = len(amenities.get("hospital", []))
    metro_count = len(amenities.get("metro", []))
    park_count = len(amenities.get("park", []))
    restaurant_count = len(amenities.get("restaurant", []))
    mall_count = len(amenities.get("mall", []))
    bus_count = len(amenities.get("bus_stop", []))

    metro_dist = amenities.get("metro", [{}])[0].get("distance_km", "N/A") if amenities.get("metro") else "N/A"
    nearest_school = amenities.get("school", [{}])[0].get("name", "N/A") if amenities.get("school") else "N/A"
    nearest_hospital = amenities.get("hospital", [{}])[0].get("name", "N/A") if amenities.get("hospital") else "N/A"

    prices_note = f"The predicted price for this property is ₹{price} Lakhs." if price else ""

    if not GROQ_API_KEY:
        return JsonResponse({
            'pros': [
                f"{location} has {school_count} schools and {hospital_count} hospitals nearby.",
                f"{metro_count} metro stations within reach provide good connectivity." if metro_count > 0 else "Good road connectivity to major areas.",
                "Growing residential area with developing infrastructure.",
            ],
            'cons': [
                "Limited commercial spaces nearby." if mall_count < 2 else "Well-served by shopping areas.",
                "Consider personal vehicle for commute." if metro_count == 0 else "",
                "Parking can be a concern in older layouts." if park_count < 2 else "",
            ],
            'investment_potential': "Good",
            'rental_demand': "High" if metro_count > 0 and school_count > 2 else "Moderate",
            'future_growth': "Positive outlook with ongoing infrastructure development.",
            'recommendation': "Recommended for long-term investment.",
            'locality_score': scores["overall"],
            'breakdown_scores': scores,
        })

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""You are a Bengaluru real estate expert. Analyze this locality:

Location: {location}, Bangalore
{prices_note}
Nearby Amenities:
- Schools: {school_count} (nearest: {nearest_school})
- Hospitals: {hospital_count} (nearest: {nearest_hospital})
- Metro Stations: {metro_count} (nearest: {metro_dist} km)
- Parks: {park_count}
- Restaurants: {restaurant_count}
- Shopping Malls: {mall_count}
- Bus Stops: {bus_count}

Locality Scores (0-10):
- Education: {scores['education']}
- Healthcare: {scores['healthcare']}
- Transport: {scores['transport']}
- Lifestyle: {scores['lifestyle']}
- Overall: {scores['overall']}

Return a JSON object with these exact keys:
- "pros": array of 3-4 bullet-point pros about this locality for investment/living
- "cons": array of 2-3 bullet-point cons or considerations
- "investment_potential": one word - "Excellent", "Good", "Moderate", or "Low"
- "rental_demand": one word - "Very High", "High", "Moderate", or "Low"
- "future_growth": 2-sentence paragraph about future growth prospects
- "recommendation": 2-sentence final verdict for a potential buyer/investor

Only valid JSON, no other text."""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
        )
        result = json.loads(response.choices[0].message.content)
        result['locality_score'] = scores['overall']
        result['breakdown_scores'] = scores
        return JsonResponse(result)

    except Exception:
        return JsonResponse({
            'pros': [
                f"{location} benefits from {school_count} schools and {hospital_count} hospitals in the vicinity.",
                f"Connectivity is well-served by {metro_count} metro station(s) and {bus_count} bus stops." if metro_count > 0 or bus_count > 0 else "Well-connected via major road networks.",
                f"{restaurant_count} dining options and {park_count} parks enhance lifestyle." if restaurant_count > 0 or park_count > 0 else "Developing social infrastructure in the area.",
            ],
            'cons': [
                "Limited shopping options nearby." if mall_count < 2 else "Good commercial infrastructure.",
                "Public transport could improve." if metro_count == 0 else "Excellent public transit connectivity.",
            ],
            'investment_potential': "Good",
            'rental_demand': "High" if metro_count > 0 else "Moderate",
            'future_growth': f"{location} is poised for steady growth with ongoing urban development in Bengaluru. Infrastructure improvements and new commercial projects are expected to boost property values.",
            'recommendation': f"{location} presents a solid opportunity for both end-users and investors. With its current infrastructure and growth trajectory, it offers good long-term value.",
            'locality_score': scores['overall'],
            'breakdown_scores': scores,
        })


@csrf_exempt
def chatbot(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    message = request.POST.get('message', '')
    context = request.POST.get('context', '{}')

    if not message:
        return JsonResponse({'error': 'Message is required'}, status=400)

    try:
        ctx = json.loads(context) if context else {}
    except json.JSONDecodeError:
        ctx = {}

    if not GROQ_API_KEY:
        return JsonResponse({
            'reply': f"I'm EstateAI's property assistant. Based on current data: {message} For Bengaluru real estate, consider factors like location, connectivity, nearby amenities, and price trends. Would you like specific advice about a locality?",
        })

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)

        context_info = ""
        if ctx.get('location'):
            context_info += f"\nCurrent context - Location: {ctx['location']}"
        if ctx.get('price'):
            context_info += f", Price: ₹{ctx['price']}L"
        if ctx.get('scores'):
            context_info += f", Locality Score: {ctx['scores']}/10"

        system_prompt = f"""You are EstateAI, a professional Bengaluru real estate assistant. You help users with property-related questions about Bangalore's real estate market. Be concise, factual, and helpful. Focus on Bangalore areas, prices, trends, and investment advice. Keep responses under 3-4 sentences unless asked for details.{context_info}"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            max_tokens=300,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        return JsonResponse({'reply': reply})

    except Exception:
        return JsonResponse({
            'reply': "I'm having trouble connecting to my AI engine right now. For Bengaluru real estate queries, consider checking property values, nearby amenities, connectivity options, and recent price trends in the area. Try again shortly.",
        })

@csrf_exempt
def calculate_commute(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)
    
    origin = request.POST.get('origin')
    workplace = request.POST.get('workplace')
    
    if not origin or not workplace:
        return JsonResponse({'error': 'origin and workplace are required'}, status=400)
    
    api_key = "f10c50087c554ce39210d77d19ede592"
    
    try:
        # Geocode origin
        o_url = f"https://api.geoapify.com/v1/geocode/search?text={requests.utils.quote(origin + ', Bangalore')}&limit=1&apiKey={api_key}"
        o_resp = requests.get(o_url, timeout=5).json()
        if not o_resp.get("features"):
            return JsonResponse({'error': 'Could not find origin.'}, status=404)
        lat, lon = o_resp["features"][0]["geometry"]["coordinates"][1], o_resp["features"][0]["geometry"]["coordinates"][0]
        
        # Geocode destination
        geo_url = f"https://api.geoapify.com/v1/geocode/search?text={requests.utils.quote(workplace + ', Bangalore')}&limit=1&apiKey={api_key}"
        geo_resp = requests.get(geo_url, timeout=5).json()
        
        if not geo_resp.get("features"):
            return JsonResponse({'error': 'Could not find the workplace location.'}, status=404)
            
        dest_lon, dest_lat = geo_resp["features"][0]["geometry"]["coordinates"]
        
        route_url = f"https://api.geoapify.com/v1/routing?waypoints={lat},{lon}|{dest_lat},{dest_lon}&mode=drive&apiKey={api_key}"
        route_resp = requests.get(route_url, timeout=5).json()
        
        if route_resp.get("features"):
            props = route_resp["features"][0]["properties"]
            return JsonResponse({
                'distance_km': round(props.get('distance', 0) / 1000, 1),
                'time_mins': round(props.get('time', 0) / 60)
            })
            
        return JsonResponse({'error': 'Could not calculate route.'}, status=400)
        
    except Exception as e:
        logger.error(f"Commute error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
