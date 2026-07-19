import json
from typing import Optional


def _weighted_score(factors: dict[str, tuple[float, float]]) -> float:
    total_weight = sum(w for _, w in factors.values())
    if total_weight == 0:
        return 5.0
    score = sum(v * w for v, w in factors.values()) / total_weight
    return round(max(0, min(10, score)), 1)


def calculate_education_score(amenities: dict) -> float:
    schools = amenities.get("school", [])
    if not schools:
        return 3.0
    count_score = min(10, len(schools) * 2.5)
    proximity_score = 0
    for s in schools[:5]:
        if s["distance_km"] <= 1:
            proximity_score += 2
        elif s["distance_km"] <= 2:
            proximity_score += 1.5
        elif s["distance_km"] <= 3:
            proximity_score += 1
    proximity_score = min(10, proximity_score)
    return _weighted_score({
        "count": (count_score, 0.5),
        "proximity": (proximity_score, 0.5),
    })


def calculate_healthcare_score(amenities: dict) -> float:
    hospitals = amenities.get("hospital", [])
    if not hospitals:
        return 2.0
    count_score = min(10, len(hospitals) * 3)
    proximity_score = 0
    for h in hospitals[:5]:
        if h["distance_km"] <= 1:
            proximity_score += 2.5
        elif h["distance_km"] <= 2:
            proximity_score += 1.5
        elif h["distance_km"] <= 3:
            proximity_score += 1
    proximity_score = min(10, proximity_score)
    return _weighted_score({
        "count": (count_score, 0.4),
        "proximity": (proximity_score, 0.6),
    })


def calculate_transport_score(amenities: dict) -> float:
    metro = amenities.get("metro", [])
    bus_stops = amenities.get("bus_stop", [])
    metro_score = 0
    for m in metro[:3]:
        if m["distance_km"] <= 1:
            metro_score += 3
        elif m["distance_km"] <= 2:
            metro_score += 2
        elif m["distance_km"] <= 3:
            metro_score += 1
    metro_score = min(10, metro_score)
    bus_score = min(10, len(bus_stops) * 1.5)
    if not metro and not bus_stops:
        return 2.0
    return _weighted_score({
        "metro": (metro_score, 0.6),
        "bus": (bus_score, 0.4),
    })


def calculate_lifestyle_score(amenities: dict) -> float:
    restaurants = amenities.get("restaurant", [])
    malls = amenities.get("mall", [])
    parks = amenities.get("park", [])

    restaurant_score = min(10, len(restaurants) * 1.5)
    mall_score = min(10, len(malls) * 3)
    park_score = 0
    for p in parks[:3]:
        if p["distance_km"] <= 1:
            park_score += 3
        elif p["distance_km"] <= 2:
            park_score += 2
        elif p["distance_km"] <= 3:
            park_score += 1
    park_score = min(10, park_score)

    if not restaurants and not malls and not parks:
        return 1.0

    return _weighted_score({
        "restaurants": (restaurant_score, 0.3),
        "malls": (mall_score, 0.3),
        "parks": (park_score, 0.4),
    })


def calculate_overall_score(scores: dict[str, float]) -> float:
    values = list(scores.values())
    return round(sum(values) / len(values), 1)


def calculate_all_scores(amenities: dict) -> dict[str, float]:
    scores = {
        "education": calculate_education_score(amenities),
        "healthcare": calculate_healthcare_score(amenities),
        "transport": calculate_transport_score(amenities),
        "lifestyle": calculate_lifestyle_score(amenities),
    }
    scores["overall"] = calculate_overall_score(scores)
    return scores


def generate_recommendation(
    location: str,
    predicted_price: float,
    amenities: dict,
    budget: float,
    scores: dict[str, float],
) -> dict:
    metro = amenities.get("metro", [])
    schools = amenities.get("school", [])
    hospitals = amenities.get("hospital", [])
    restaurants = amenities.get("restaurant", [])

    pros = []
    cons = []

    if scores["education"] >= 7:
        pros.append("Excellent educational infrastructure with reputed schools nearby.")
    elif scores["education"] >= 5:
        pros.append("Adequate schooling options available in the vicinity.")
    else:
        cons.append("Limited educational institutions nearby; may require commuting.")

    if scores["healthcare"] >= 7:
        pros.append("Well-served by hospitals and healthcare facilities.")
    elif scores["healthcare"] >= 5:
        pros.append("Basic healthcare facilities accessible within reasonable distance.")
    else:
        cons.append("Healthcare facilities are limited; nearest hospital may be far.")

    if scores["transport"] >= 7:
        pros.append("Excellent connectivity with metro and bus services.")
    elif scores["transport"] >= 5:
        pros.append("Decent public transport connectivity available.")
    else:
        cons.append("Public transport connectivity is limited; personal vehicle recommended.")

    if scores["lifestyle"] >= 7:
        pros.append("Vibrant lifestyle with restaurants, malls, and parks nearby.")
    elif scores["lifestyle"] >= 5:
        pros.append("Moderate lifestyle amenities available.")
    else:
        cons.append("Limited entertainment and dining options in the area.")

    if metro and metro[0]["distance_km"] <= 2:
        pros.append(f"Metro station '{metro[0]['name']}' is only {metro[0]['distance_km']} km away.")
    else:
        cons.append("No metro station within walking distance.")

    if predicted_price <= budget * 1.1:
        pros.append("Property price is within your budget range.")
    else:
        cons.append(f"Property price exceeds budget by {((predicted_price / budget) - 1) * 100:.1f}%.")

    if scores["overall"] >= 7:
        investment_potential = "High"
        rental_demand = "Strong"
    elif scores["overall"] >= 5:
        investment_potential = "Moderate"
        rental_demand = "Average"
    else:
        investment_potential = "Low"
        rental_demand = "Weak"

    family_friendly = "Yes" if scores["education"] >= 6 and scores["healthcare"] >= 6 else "Moderate"

    if scores["transport"] >= 7:
        connectivity = "Excellent"
    elif scores["transport"] >= 5:
        connectivity = "Good"
    else:
        connectivity = "Fair"

    if scores["overall"] >= 8:
        recommendation = "Highly Recommended"
    elif scores["overall"] >= 6:
        recommendation = "Recommended"
    elif scores["overall"] >= 4:
        recommendation = "Consider with Caution"
    else:
        recommendation = "Not Recommended"

    growth_potential = "High"
    if scores["overall"] >= 7:
        growth_potential = "High - strong fundamentals and growing demand"
    elif scores["overall"] >= 5:
        growth_potential = "Moderate - steady appreciation expected"
    else:
        growth_potential = "Limited - may not see significant appreciation"

    return {
        "pros": pros[:5],
        "cons": cons[:5],
        "investment_potential": investment_potential,
        "rental_demand": rental_demand,
        "family_friendliness": family_friendly,
        "connectivity": connectivity,
        "recommendation": recommendation,
        "future_growth": growth_potential,
        "overall_score": scores["overall"],
    }
