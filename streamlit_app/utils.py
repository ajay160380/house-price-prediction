import os
import json
import time
import hashlib
import functools
from typing import Any, Optional

import streamlit as st

CACHE_DIR = os.path.join(os.path.dirname(__file__), '.cache')
os.makedirs(CACHE_DIR, exist_ok=True)


def cache_key(*args, **kwargs) -> str:
    raw = json.dumps((args, sorted(kwargs.items())), sort_keys=True, default=str)
    return hashlib.md5(raw.encode()).hexdigest()


def cached_api_call(ttl_seconds: int = 3600):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = cache_key(func.__name__, *args, **kwargs)
            cache_file = os.path.join(CACHE_DIR, f"{key}.json")
            if os.path.exists(cache_file):
                age = time.time() - os.path.getmtime(cache_file)
                if age < ttl_seconds:
                    with open(cache_file) as f:
                        return json.load(f)
            result = func(*args, **kwargs)
            try:
                with open(cache_file, 'w') as f:
                    json.dump(result, f, default=str)
            except (OSError, TypeError):
                pass
            return result
        return wrapper
    return decorator


def format_indian_currency(value_lakhs: float) -> str:
    if value_lakhs < 100:
        return f"\u20b9 {value_lakhs:,.2f} Lakhs"
    return f"\u20b9 {value_lakhs / 100:,.2f} Cr"


def indian_number_format(num: float) -> str:
    num_str = str(round(num))
    last_three = num_str[-3:]
    rest = num_str[:-3]
    if rest:
        groups = []
        while len(rest) > 2:
            groups.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.append(rest)
        groups.reverse()
        return ",".join(groups) + "," + last_three
    return last_three


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    import math
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def load_css() -> str:
    return """
    <style>
        .stApp { background-color: #0a0a12; }
        .stButton>button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; border: none; border-radius: 10px;
            padding: 8px 24px; font-weight: 600; transition: all 0.2s;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 24px rgba(102,126,234,0.3);
        }
        .stSelectbox>div>div, .stNumberInput>div>div, .stSlider>div {
            background: rgba(255,255,255,0.05) !important;
            border: 1.5px solid rgba(255,255,255,0.1) !important;
            border-radius: 9px !important;
        }
        .stSelectbox>div>div>div, .stNumberInput input {
            color: #e8e8f0 !important;
        }
        .stSlider label, .stSelectbox label, .stNumberInput label {
            color: #e8e8f0 !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 28px !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #fff, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 11px !important;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: #999aaf !important;
        }
        .card {
            background: rgba(255,255,255,0.04);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 14px;
            padding: 22px 24px;
            margin-bottom: 16px;
        }
        .card-title {
            font-size: 11px; text-transform: uppercase;
            letter-spacing: 1.2px; color: #999aaf;
            margin-bottom: 14px; font-weight: 600;
        }
        .badge {
            display: inline-block; padding: 3px 12px;
            border-radius: 7px; font-size: 12px; font-weight: 600;
            background: rgba(102,126,234,0.15); color: #667eea;
        }
        h1, h2, h3, h4 { color: #e8e8f0 !important; }
        p, li, span { color: #999aaf !important; }
        a { color: #00d4ff !important; }
        .stProgress > div > div {
            background: linear-gradient(90deg, #667eea, #00d4ff) !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            padding: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            color: #999aaf;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
        }
        footer { display: none; }
        @media (max-width: 768px) {
            .card { padding: 16px; }
        }
        .stAlert {
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 10px !important;
        }
        .stSpinner > div {
            border-color: #667eea !important;
            border-top-color: transparent !important;
        }
    </style>
    """


def amenity_icon(category: str) -> str:
    icons = {
        "school": "\U0001F3EB",
        "hospital": "\U0001F3E5",
        "metro": "\U0001F687",
        "park": "\U0001F333",
        "restaurant": "\U0001F372",
        "mall": "\U0001F3EC",
        "bus_stop": "\U0001F68C",
    }
    return icons.get(category, "\U0001F4CD")
