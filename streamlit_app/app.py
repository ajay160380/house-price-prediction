import streamlit as st
import streamlit.components.v1 as components

from prediction import get_locations, predict_price
from location_service import geocode_location, get_bangalore_center, is_valid_location
from overpass_service import get_amenities_by_category, AMENITY_DISPLAY
from advisor import calculate_all_scores, generate_recommendation
from dashboard import (
    create_score_gauge, create_radar_chart, create_amenity_bar_chart,
    create_price_range_chart, create_comparison_chart,
)
from utils import format_indian_currency, indian_number_format, load_css, amenity_icon

st.set_page_config(
    page_title="EstateAI - Bengaluru Real Estate Intelligence",
    page_icon="\U0001F3E0",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(load_css(), unsafe_allow_html=True)

LOCATIONS = get_locations()

BANGALORE_CENTER = get_bangalore_center()

SCORE_COLORS = {
    "education": "#667eea",
    "healthcare": "#28a745",
    "transport": "#00d4ff",
    "lifestyle": "#ff6b6b",
    "overall": "#764ba2",
}

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "selected_location" not in st.session_state:
    st.session_state.selected_location = None
if "amenities" not in st.session_state:
    st.session_state.amenities = None
if "scores" not in st.session_state:
    st.session_state.scores = None
if "advisor_report" not in st.session_state:
    st.session_state.advisor_report = None
if "location_coords" not in st.session_state:
    st.session_state.location_coords = None
if "prediction_key" not in st.session_state:
    st.session_state.prediction_key = 0


def run_prediction(location: str, sqft: float, bhk: int, bath: int):
    with st.spinner("Analyzing market data..."):
        try:
            st.session_state.prediction_result = predict_price(location, sqft, bath, bhk)
            st.session_state.selected_location = location
            st.session_state.prediction_key += 1
        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
            st.session_state.prediction_result = None


def load_amenities(lat: float, lon: float):
    with st.spinner("Fetching nearby amenities..."):
        try:
            st.session_state.amenities = get_amenities_by_category(lat, lon)
            if st.session_state.amenities:
                total = sum(len(v) for v in st.session_state.amenities.values())
                if total == 0:
                    st.warning("Amenity data is currently unavailable. The Overpass API may be busy. Try again later.")
            st.session_state.scores = calculate_all_scores(st.session_state.amenities)
        except Exception:
            st.warning("Failed to fetch amenities. The free Overpass API may be rate-limited. Scores will use defaults.")
            st.session_state.amenities = {cat: [] for cat in [
                "school", "hospital", "metro", "park", "restaurant", "mall", "bus_stop"
            ]}
            st.session_state.scores = calculate_all_scores(st.session_state.amenities)


def run_advisor(location: str, price: float, budget: float):
    if st.session_state.amenities and st.session_state.scores:
        st.session_state.advisor_report = generate_recommendation(
            location=location,
            predicted_price=price,
            amenities=st.session_state.amenities,
            budget=budget,
            scores=st.session_state.scores,
        )


def render_leaflet_map(lat: float, lon: float, location_name: str, amenities: dict = None):
    markers = []
    markers.append({
        "lat": lat, "lon": lon,
        "name": location_name,
        "type": "property",
        "color": "#667eea",
        "icon": "home"
    })

    if amenities:
        category_colors = {
            "school": "#FFD700", "hospital": "#FF4444", "metro": "#00AAFF",
            "park": "#44BB44", "restaurant": "#FF8800", "mall": "#FF69B4",
            "bus_stop": "#888888",
        }
        category_icons = {
            "school": "school", "hospital": "hospital", "metro": "subway",
            "park": "park", "restaurant": "restaurant", "mall": "shopping",
            "bus_stop": "bus",
        }
        for cat, items in amenities.items():
            for item in items[:5]:
                markers.append({
                    "lat": item["lat"],
                    "lon": item["lon"],
                    "name": item["name"],
                    "type": cat,
                    "color": category_colors.get(cat, "#FFFFFF"),
                    "icon": category_icons.get(cat, "info"),
                })

    markers_json = str(markers).replace("'", '"')

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body {{ margin: 0; padding: 0; }}
            #map {{ width: 100%; height: 550px; border-radius: 14px; }}
            .leaflet-container {{ background: #0a0a12 !important; }}
            .leaflet-popup-content-wrapper {{ 
                background: #1a1a2e !important; color: #e8e8f0 !important; 
                border: 1px solid rgba(255,255,255,0.1) !important;
                border-radius: 8px !important; font-size: 13px;
            }}
            .leaflet-popup-tip {{ background: #1a1a2e !important; }}
            .leaflet-control-zoom a {{
                background: rgba(255,255,255,0.06) !important;
                color: #e8e8f0 !important;
                border-color: rgba(255,255,255,0.1) !important;
            }}
            .custom-icon {{
                display: flex; align-items: center; justify-content: center;
                width: 28px; height: 28px; border-radius: 50%;
                border: 2px solid rgba(255,255,255,0.3);
                font-size: 14px; font-weight: bold;
                box-shadow: 0 2px 8px rgba(0,0,0,0.4);
            }}
            .property-icon {{
                width: 36px; height: 36px; border-radius: 8px;
                display: flex; align-items: center; justify-content: center;
                font-size: 18px; border: 2px solid white;
                box-shadow: 0 4px 16px rgba(102,126,234,0.4);
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map', {{
                zoomControl: false,
                attributionControl: false
            }}).setView([{lat}, {lon}], 14);

            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                maxZoom: 19
            }}).addTo(map);

            L.control.zoom({{ position: 'bottomright' }}).addTo(map);

            var markers = {markers_json};

            markers.forEach(function(m) {{
                var color = m.color;
                var size = m.type === 'property' ? 14 : 11;
                var iconHtml;
                if (m.type === 'property') {{
                    iconHtml = '<div class="property-icon" style="background: ' + color + ';">🏠</div>';
                }} else {{
                    iconHtml = '<div class="custom-icon" style="background: ' + color + '; width: ' + (size*2) + 'px; height: ' + (size*2) + 'px; font-size: ' + (size) + 'px;">●</div>';
                }}
                var icon = L.divIcon({{
                    html: iconHtml,
                    iconSize: [36, 36],
                    iconAnchor: [18, 18],
                    popupAnchor: [0, -18],
                    className: ''
                }});
                var marker = L.marker([m.lat, m.lon], {{ icon: icon }}).addTo(map);
                marker.bindPopup('<strong>' + m.name + '</strong><br>' + m.type.charAt(0).toUpperCase() + m.type.slice(1));
            }});

            setTimeout(function() {{ map.invalidateSize(); }}, 200);
        </script>
    </body>
    </html>
    """
    components.html(html, height=560)


def render_dashboard_tab():
    st.markdown("<div class='card'><div class='card-title'>\U0001F4CA Property Dashboard</div>", unsafe_allow_html=True)

    pred = st.session_state.prediction_result
    scores = st.session_state.scores
    amenities = st.session_state.amenities
    loc = st.session_state.selected_location

    if not pred:
        st.info("Run a prediction first to see the dashboard.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Predicted Price", format_indian_currency(pred["estimated_price"]))
    with col2:
        st.metric("Price Range", f"{format_indian_currency(pred['estimated_price_low'])} - {format_indian_currency(pred['estimated_price_high'])}")
    with col3:
        school_count = len(amenities.get("school", [])) if amenities else 0
        st.metric("Nearby Schools", str(school_count))
    with col4:
        hospital_count = len(amenities.get("hospital", [])) if amenities else 0
        st.metric("Nearby Hospitals", str(hospital_count))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metro_dist = amenities.get("metro", [{}])[0].get("distance_km", "N/A") if amenities else "N/A"
        metro_dist_str = f"{metro_dist} km" if isinstance(metro_dist, float) else metro_dist
        st.metric("Nearest Metro", metro_dist_str)
    with col2:
        if scores:
            st.metric("Locality Score", f"{scores['overall']}/10")
    with col3:
        if scores:
            st.metric("Education Score", f"{scores['education']}/10")
    with col4:
        if scores:
            st.metric("Healthcare Score", f"{scores['healthcare']}/10")

    col1, col2 = st.columns(2)
    with col1:
        if scores:
            st.metric("Transport Score", f"{scores['transport']}/10")
    with col2:
        if scores:
            st.metric("Lifestyle Score", f"{scores['lifestyle']}/10")

    if st.session_state.advisor_report:
        rec = st.session_state.advisor_report
        st.metric("Investment Recommendation", rec["recommendation"])
        st.metric("Investment Potential", rec["investment_potential"])

    st.markdown("</div>", unsafe_allow_html=True)

    if scores:
        st.markdown("<div class='card'><div class='card-title'>\U0001F4CA Score Breakdown</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(create_radar_chart(scores), use_container_width=True)
        with c2:
            st.plotly_chart(create_amenity_bar_chart(amenities), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if pred:
        st.markdown("<div class='card'><div class='card-title'>\U0001F4B0 Price Range</div>", unsafe_allow_html=True)
        st.plotly_chart(
            create_price_range_chart(
                pred["estimated_price_low"],
                pred["estimated_price"],
                pred["estimated_price_high"],
            ),
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_advisor_tab():
    st.markdown("<div class='card'><div class='card-title'>\U0001F9E0 AI Locality Advisor Report</div>", unsafe_allow_html=True)

    if not st.session_state.prediction_result:
        st.info("Run a prediction first to get the AI locality report.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    pred = st.session_state.prediction_result
    loc = st.session_state.selected_location

    budget = st.number_input(
        "Your Budget (\u20b9 Lakhs)",
        min_value=10.0,
        max_value=5000.0,
        value=float(pred["estimated_price"]),
        step=10.0,
        format="%.2f",
        key="advisor_budget",
    )

    if st.button("Generate AI Report", use_container_width=True):
        run_advisor(loc, pred["estimated_price"], budget)

    if st.session_state.advisor_report:
        rec = st.session_state.advisor_report

        overall = rec["overall_score"]
        if overall >= 8:
            score_label = "\U0001F7E2 Excellent"
            score_color = "#28a745"
        elif overall >= 6:
            score_label = "\U0001F7E1 Good"
            score_color = "#FFD700"
        elif overall >= 4:
            score_label = "\U0001F7E0 Average"
            score_color = "#FF8800"
        else:
            score_label = "\U0001F534 Poor"
            score_color = "#FF4444"

        st.markdown(
            f"<div style='text-align:center; margin:16px 0;'>"
            f"<span style='font-size:48px; font-weight:800; color:{score_color};'>{overall}</span>"
            f"<span style='font-size:16px; color:#999aaf;'>/10</span><br>"
            f"<span style='font-size:18px; color:{score_color}; font-weight:600;'>{score_label}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='card'><div class='card-title'>\U0001F4C8 Investment</div>"
                        f"<p style='font-size:20px; color:#e8e8f0;'>{rec['investment_potential']}</p></div>",
                        unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='card'><div class='card-title'>\U0001F3E2 Rental Demand</div>"
                        f"<p style='font-size:20px; color:#e8e8f0;'>{rec['rental_demand']}</p></div>",
                        unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='card'><div class='card-title'>\U0001F4CD Recommendation</div>"
                        f"<p style='font-size:20px; color:#e8e8f0;'>{rec['recommendation']}</p></div>",
                        unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='card'><div class='card-title'>\U0001F46A Family Friendly</div>"
                        f"<p style='font-size:20px; color:#e8e8f0;'>{rec['family_friendliness']}</p></div>",
                        unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='card'><div class='card-title'>\U0001F310 Connectivity</div>"
                        f"<p style='font-size:20px; color:#e8e8f0;'>{rec['connectivity']}</p></div>",
                        unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='card'><div class='card-title'>\U0001F4C5 Future Growth</div>"
                        f"<p style='font-size:20px; color:#e8e8f0;'>{rec['future_growth']}</p></div>",
                        unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>\u2705 Pros</div>", unsafe_allow_html=True)
        for p in rec["pros"]:
            st.markdown(f"\u2705 {p}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>\u26A0\uFE0F Cons</div>", unsafe_allow_html=True)
        for c in rec["cons"]:
            st.markdown(f"\u26A0\uFE0F {c}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_nearby_tab():
    st.markdown("<div class='card'><div class='card-title'>\U0001F4CD Nearby Amenities</div>", unsafe_allow_html=True)

    if not st.session_state.amenities:
        st.info("Run a prediction to discover nearby amenities.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    amenities = st.session_state.amenities
    all_items = []
    for cat, items in amenities.items():
        for item in items:
            all_items.append(item)

    total_items = len(all_items)
    category_counts = {AMENITY_DISPLAY.get(cat, cat): len(items) for cat, items in amenities.items()}

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Total Amenities Found", str(total_items))
        st.markdown("**Breakdown:**")
        for cat_name, count in category_counts.items():
            if count > 0:
                st.markdown(f"- {cat_name}: {count}")

    with col2:
        st.plotly_chart(create_amenity_bar_chart(amenities), use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    search_cat = st.selectbox(
        "Filter by category",
        ["All"] + list(AMENITY_DISPLAY.values()),
        key="amenity_filter",
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for cat, items in amenities.items():
        display_name = AMENITY_DISPLAY.get(cat, cat)
        if search_cat != "All" and search_cat != display_name:
            continue
        if items:
            st.markdown(f"<div class='card-title'>{amenity_icon(cat)} {display_name} ({len(items)})</div>",
                        unsafe_allow_html=True)
            for item in items[:10]:
                dist_str = f"{item['distance_km']} km" if item['distance_km'] < 1 else f"{item['distance_km']} km"
                st.markdown(
                    f"<div style='display:flex; justify-content:space-between; align-items:center; "
                    f"padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.04);'>"
                    f"<span style='color:#e8e8f0;'>{item['name']}</span>"
                    f"<span style='color:#999aaf; font-size:12px;'>{dist_str}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            if len(items) > 10:
                st.caption(f"... and {len(items) - 10} more")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='card-title'>\U0001F3DF\uFE0F Amenity Scores</div>", unsafe_allow_html=True)
    if st.session_state.scores:
        scores = st.session_state.scores
        cols = st.columns(len(scores))
        for i, (key, label) in enumerate([
            ("education", "Education"), ("healthcare", "Healthcare"),
            ("transport", "Transport"), ("lifestyle", "Lifestyle"),
            ("overall", "Overall"),
        ]):
            with cols[i]:
                val = scores.get(key, 0)
                st.markdown(f"<div style='text-align:center;'>", unsafe_allow_html=True)
                st.markdown(
                    f"<span style='font-size:28px; font-weight:700; color:{SCORE_COLORS.get(key, '#667eea')};'>{val}</span>"
                    f"<span style='color:#999aaf;'>/10</span><br>"
                    f"<span style='font-size:11px; color:#999aaf; text-transform:uppercase;'>{label}</span>",
                    unsafe_allow_html=True,
                )
                st.progress(val / 10)
                st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_compare_tab():
    st.markdown("<div class='card'><div class='card-title'>\U0001F500 Compare Localities</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        loc1 = st.selectbox("Location 1", LOCATIONS, index=LOCATIONS.index("Whitefield") if "Whitefield" in LOCATIONS else 0, key="comp_loc1")
        sqft1 = st.number_input("Area (sqft)", min_value=300, max_value=10000, value=1200, step=50, key="comp_sqft1")
        bhk1 = st.selectbox("BHK", [1, 2, 3, 4, 5], index=1, key="comp_bhk1")
        bath1 = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1, key="comp_bath1")

    with col2:
        loc2 = st.selectbox("Location 2", LOCATIONS, index=LOCATIONS.index("Electronic City") if "Electronic City" in LOCATIONS else 0, key="comp_loc2")
        sqft2 = st.number_input("Area (sqft)", min_value=300, max_value=10000, value=1200, step=50, key="comp_sqft2")
        bhk2 = st.selectbox("BHK", [1, 2, 3, 4, 5], index=1, key="comp_bhk2")
        bath2 = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1, key="comp_bath2")

    if st.button("Compare Localities", use_container_width=True):
        with st.spinner("Comparing localities..."):
            try:
                result1 = predict_price(loc1, sqft1, bath1, bhk1)
                result2 = predict_price(loc2, sqft2, bath2, bhk2)

                coords1 = geocode_location(loc1)
                coords2 = geocode_location(loc2)

                amenities1 = {}
                amenities2 = {}
                scores1 = {}
                scores2 = {}

                if coords1:
                    amenities1 = get_amenities_by_category(coords1["lat"], coords1["lon"])
                    scores1 = calculate_all_scores(amenities1)
                if coords2:
                    amenities2 = get_amenities_by_category(coords2["lat"], coords2["lon"])
                    scores2 = calculate_all_scores(amenities2)

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"<div class='card'><h3 style='color:#667eea;'>{loc1}</h3>", unsafe_allow_html=True)
                    st.metric("Predicted Price", format_indian_currency(result1["estimated_price"]))
                    if scores1:
                        st.metric("Locality Score", f"{scores1.get('overall', 'N/A')}/10")
                    st.markdown(f"**Schools:** {len(amenities1.get('school', []))}")
                    st.markdown(f"**Hospitals:** {len(amenities1.get('hospital', []))}")
                    st.markdown(f"**Metro Stations:** {len(amenities1.get('metro', []))}")
                    st.markdown("</div>", unsafe_allow_html=True)

                with c2:
                    st.markdown(f"<div class='card'><h3 style='color:#00d4ff;'>{loc2}</h3>", unsafe_allow_html=True)
                    st.metric("Predicted Price", format_indian_currency(result2["estimated_price"]))
                    if scores2:
                        st.metric("Locality Score", f"{scores2.get('overall', 'N/A')}/10")
                    st.markdown(f"**Schools:** {len(amenities2.get('school', []))}")
                    st.markdown(f"**Hospitals:** {len(amenities2.get('hospital', []))}")
                    st.markdown(f"**Metro Stations:** {len(amenities2.get('metro', []))}")
                    st.markdown("</div>", unsafe_allow_html=True)

                if scores1 and scores2:
                    st.plotly_chart(
                        create_comparison_chart(scores1, scores2, loc1, loc2),
                        use_container_width=True,
                    )

                price_diff = result2["estimated_price"] - result1["estimated_price"]
                if price_diff > 0:
                    st.info(f"{loc2} is \u20b9{abs(price_diff):.2f}L more expensive than {loc1}")
                else:
                    st.info(f"{loc1} is \u20b9{abs(price_diff):.2f}L more expensive than {loc2}")

            except Exception as e:
                st.error(f"Comparison failed: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)


def render_about_tab():
    st.markdown("""
    <div class='card'>
        <div class='card-title'>ℹ️ About EstateAI</div>
        <p><strong>EstateAI</strong> is a production-ready AI-powered Bengaluru Real Estate Intelligence Platform.</p>
        <p>Built with:</p>
        <ul>
            <li><strong>Machine Learning:</strong> Scikit-learn Linear Regression model trained on Bengaluru housing data</li>
            <li><strong>Geospatial:</strong> OpenStreetMap, Leaflet, Nominatim API for location data</li>
            <li><strong>Amenities:</strong> Overpass API for real-time nearby amenity data</li>
            <li><strong>Visualization:</strong> Plotly for interactive charts and dashboards</li>
            <li><strong>AI Advisor:</strong> Rule-based intelligent analysis engine</li>
        </ul>
        <p style='margin-top:12px; color:#999aaf; font-size:12px;'>Version 2.0 · Bengaluru, India</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    st.sidebar.markdown(
        "<div style='display:flex; align-items:center; gap:10px; margin-bottom:24px;'>"
        "<div style='width:38px;height:38px;border-radius:10px;"
        "background:linear-gradient(135deg,#667eea,#764ba2);"
        "display:flex;align-items:center;justify-content:center;font-size:18px;'>🏡</div>"
        "<div><h2 style='font-size:17px;font-weight:700;margin:0;"
        "background:linear-gradient(135deg,#fff,#00d4ff);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>EstateAI</h2>"
        "<span style='font-size:10px;color:#999aaf;'>Real Estate Intelligence</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigation",
        ["Property Predictor", "Dashboard", "Nearby Amenities",
         "AI Advisor", "Compare Localities", "About"],
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")

    with st.sidebar:
        st.markdown(
            "<div style='font-size:10px;color:#999aaf;text-align:center;padding-top:12px;'>"
            "EstateAI v2.0 · Enterprise</div>",
            unsafe_allow_html=True,
        )

    if page == "Property Predictor":
        st.markdown(
            "<h1 style='font-size:24px; font-weight:700; margin-bottom:4px;'>"
            "\U0001F3E0 Property Price Predictor</h1>"
            "<p style='color:#999aaf; margin-bottom:20px;'>ML-powered Bengaluru real estate valuation</p>",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([1, 1.5])

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>Property Parameters</div>", unsafe_allow_html=True)

            with st.form(key="prediction_form"):
                location = st.selectbox(
                    "Location",
                    LOCATIONS,
                    index=LOCATIONS.index("Whitefield") if "Whitefield" in LOCATIONS else 0,
                    placeholder="Select a locality...",
                    key="predict_location",
                )

                sqft = st.number_input(
                    "Area (sqft)",
                    min_value=300.0,
                    max_value=10000.0,
                    value=1500.0,
                    step=50.0,
                    format="%.0f",
                )

                col_bhk, col_bath = st.columns(2)
                with col_bhk:
                    bhk = st.selectbox("BHK", [1, 2, 3, 4, 5], index=1)
                with col_bath:
                    bath = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1)

                submitted = st.form_submit_button("Predict Price \u2192", use_container_width=True)

            if submitted:
                if not location:
                    st.error("Please select a location.")
                else:
                    run_prediction(location, sqft, bhk, bath)

                    coords = geocode_location(location)
                    if coords:
                        st.session_state.location_coords = coords
                        load_amenities(coords["lat"], coords["lon"])
                    else:
                        st.session_state.location_coords = get_bangalore_center()

            if st.session_state.prediction_result:
                pred = st.session_state.prediction_result
                st.markdown(
                    f"<div style='margin-top:16px; padding:14px; border-radius:10px; "
                    f"background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); "
                    f"text-align:center;'>"
                    f"<div style='font-size:10px; text-transform:uppercase; letter-spacing:1.5px; "
                    f"color:#999aaf;'>Estimated Price Range</div>"
                    f"<div style='font-size:22px; font-weight:800; background:linear-gradient(135deg,#fff,#00d4ff); "
                    f"-webkit-background-clip:text;-webkit-text-fill-color:transparent; "
                    f"margin:4px 0;'>{format_indian_currency(pred['estimated_price_low'])} — {format_indian_currency(pred['estimated_price_high'])}</div>"
                    f"<div style='font-size:12px; color:#999aaf;'>Base: {format_indian_currency(pred['estimated_price'])}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            coords = st.session_state.location_coords or get_bangalore_center()
            amenities = st.session_state.amenities
            render_leaflet_map(
                coords["lat"], coords["lon"],
                st.session_state.selected_location or "Bengaluru",
                amenities,
            )

            if st.session_state.scores:
                scores = st.session_state.scores
                cols = st.columns(5)
                for i, (key, label) in enumerate([
                    ("education", "Education"), ("healthcare", "Healthcare"),
                    ("transport", "Transport"), ("lifestyle", "Lifestyle"),
                    ("overall", "Overall"),
                ]):
                    with cols[i]:
                        val = scores.get(key, 0)
                        st.markdown(
                            f"<div style='text-align:center;'>"
                            f"<span style='font-size:20px; font-weight:700; "
                            f"color:{SCORE_COLORS.get(key, '#667eea')};'>{val}</span>"
                            f"<span style='color:#999aaf; font-size:10px;'>/10</span><br>"
                            f"<span style='font-size:9px; color:#999aaf; text-transform:uppercase;'>{label}</span>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )

    elif page == "Dashboard":
        render_dashboard_tab()

    elif page == "Nearby Amenities":
        render_nearby_tab()

    elif page == "AI Advisor":
        render_advisor_tab()

    elif page == "Compare Localities":
        render_compare_tab()

    elif page == "About":
        render_about_tab()


if __name__ == "__main__":
    main()
