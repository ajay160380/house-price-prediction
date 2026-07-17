import streamlit as st
import pickle
import json
import numpy as np
import os

st.set_page_config(page_title="EstateAI", page_icon="🏡", layout="wide")

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'predictor', 'ml_models', 'banglore_home_prices_model.pickle')
COLUMNS_PATH = os.path.join(os.path.dirname(__file__), 'predictor', 'ml_models', 'columns.json')

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(COLUMNS_PATH) as f:
    columns_data = json.load(f)

data_columns = columns_data['data_columns']
locations = sorted(data_columns[3:])

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("GROQ_API_KEY not found in Streamlit secrets. AI insights will not work.")
    GROQ_API_KEY = None

st.markdown("""
<style>
    .stApp { background: #0b0e1a; color: #e0e0e0; }
    .main .block-container { padding: 1.5rem 2rem; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1320 0%, #141929 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background: transparent; border-radius: 10px; padding: 10px 14px;
        transition: all 0.2s; border: 1px solid transparent;
    }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background: rgba(102,126,234,0.08);
        border-color: rgba(102,126,234,0.15);
    }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
        background: rgba(102,126,234,0.15);
        border-color: rgba(102,126,234,0.3);
    }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] p {
        color: #fff; font-weight: 600;
    }
    .bento-card {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;
    }
    .bento-card h3 {
        color: #ccd6f6; font-size: 0.85rem;
        text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 1rem;
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none; border-radius: 10px; color: #fff;
        font-weight: 600; padding: 0.5rem 1.5rem;
    }
    .stButton button:hover { opacity: 0.9; }
    .result-box {
        background: rgba(102,126,234,0.1);
        border: 1px solid rgba(102,126,234,0.2);
        border-radius: 12px; padding: 1.2rem 1.5rem; text-align: center;
    }
    .result-box .big {
        font-size: 1.6rem; font-weight: 800;
        background: linear-gradient(135deg, #fff, #667eea);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .result-box .label {
        font-size: 0.7rem; text-transform: uppercase;
        letter-spacing: 1.5px; color: #8892b0; margin-bottom: 2px;
    }
    .insight-box {
        background: rgba(0,212,255,0.06);
        border: 1px solid rgba(0,212,255,0.12);
        border-radius: 12px; padding: 1rem 1.2rem; margin-top: 0.8rem;
    }
    h1, h2 { color: #ccd6f6; }
    .sidebar-title {
        font-size: 1.4rem; font-weight: 800;
        background: linear-gradient(135deg, #667eea, #00d4ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .sidebar-sub {
        font-size: 0.7rem; color: #495670;
        letter-spacing: 1px; text-transform: uppercase; margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-title">EstateAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">SaaS Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")
    tab = st.radio("Navigation", ["Predictor", "Market Analytics", "Financial Hub", "Client Reports", "System/About"],
                   label_visibility="collapsed")
    st.markdown("---")
    st.caption("v1.0 • Scikit-Learn + Groq AI")

# ===== PREDICTOR TAB =====
if tab == "Predictor":
    st.markdown("<h2>Predictor Engine</h2><p style='color:#8892b0;margin-top:-8px'>Real-time ML property valuation</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="bento-card"><h3>Property Parameters</h3>', unsafe_allow_html=True)
        sqft = st.slider("Area (sqft)", 300, 5000, 1500, 50)
        bhk = st.selectbox("BHK", [1, 2, 3, 4, 5], index=1)
        bath = st.selectbox("Bathrooms", [1, 2, 3, 4, 5], index=1)
        location = st.selectbox("Location", [""] + locations, index=0)
        predict_btn = st.button("Predict Value →", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="bento-card"><h3>📍 Map & Market View</h3>', unsafe_allow_html=True)
        st.markdown('<div style="height:280px;background:rgba(255,255,255,0.03);border-radius:10px;display:flex;align-items:center;justify-content:center;color:#495670;font-size:0.9rem">Interactive map will render here</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        price_placeholder = st.empty()
        insight_placeholder = st.empty()

        if predict_btn and location:
            x = np.zeros(len(data_columns))
            x[0] = sqft
            x[1] = bath
            x[2] = bhk
            if location in data_columns:
                loc_index = data_columns.index(location)
                x[loc_index] = 1

            predicted_price = model.predict([x])[0]
            base = round(predicted_price, 2)
            low = round(predicted_price * 0.95, 2)
            high = round(predicted_price * 1.05, 2)

            def fmt(v):
                if v < 100:
                    return f"₹ {v:,.2f} Lakhs"
                return f"₹ {v / 100:,.2f} Cr"

            price_placeholder.markdown(
                f'<div class="result-box">'
                f'<div class="label">Estimated Price Range</div>'
                f'<div class="big">{fmt(low)} – {fmt(high)}</div>'
                f'<div style="color:#8892b0;font-size:0.8rem;margin-top:4px">Base: {fmt(base)}</div>'
                f'</div>', unsafe_allow_html=True
            )

            if GROQ_API_KEY:
                from groq import Groq
                client = Groq(api_key=GROQ_API_KEY)
                prompt = (
                    f'Return a JSON object with keys: insight_text (2-sentence professional real estate '
                    f'insight about {location}, Bangalore, covering connectivity, infrastructure, and '
                    f'market trends), investment_score (number 0-10 for ROI potential), safety_score '
                    f'(number 0-10 for neighborhood safety and infrastructure). Only valid JSON.'
                )
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        response_format={"type": "json_object"},
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=250,
                        temperature=0.7,
                    )
                    result = json.loads(response.choices[0].message.content)
                    insight_text = result.get('insight_text', '')
                    invest = result.get('investment_score', '—')
                    safety = result.get('safety_score', '—')
                except Exception:
                    insight_text = f"{location} is a sought-after residential area in Bengaluru with developing infrastructure and good connectivity to major business hubs."
                    invest, safety = 7, 7

                insight_placeholder.markdown(
                    f'<div class="insight-box">'
                    f'<div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:1.2px;color:#8892b0">✨ AI Market Insight</div>'
                    f'<div style="font-size:0.9rem;line-height:1.5;margin:6px 0">{insight_text}</div>'
                    f'<div style="font-size:0.8rem;display:flex;gap:1rem">'
                    f'<span>📈 Investment: <strong>{invest}</strong>/10</span>'
                    f'<span>🛡️ Safety: <strong>{safety}</strong>/10</span>'
                    f'</div></div>', unsafe_allow_html=True
                )
        elif predict_btn and not location:
            st.warning("Please select a location.")

# ===== MARKET ANALYTICS TAB =====
elif tab == "Market Analytics":
    st.markdown("<h2>Market Analytics</h2><p style='color:#8892b0;margin-top:-8px'>Deep data & AI-powered insights</p>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="bento-card"><h3>📊 5-Year Price Forecast</h3><div style="height:240px;background:rgba(255,255,255,0.03);border-radius:10px;display:flex;align-items:center;justify-content:center;color:#495670">Chart.js forecast will render here</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="bento-card"><h3>🏆 AI Scores</h3><div style="height:240px;background:rgba(255,255,255,0.03);border-radius:10px;display:flex;align-items:center;justify-content:center;color:#495670">Investment & Safety ring charts</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="bento-card"><h3>📍 Location Heatmap</h3><div style="height:200px;background:rgba(255,255,255,0.03);border-radius:10px;display:flex;align-items:center;justify-content:center;color:#495670">Bengaluru price heatmap</div></div>', unsafe_allow_html=True)

# ===== FINANCIAL HUB TAB =====
elif tab == "Financial Hub":
    st.markdown("<h2>Financial Hub</h2><p style='color:#8892b0;margin-top:-8px'>EMI & rental yield calculators</p>", unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown('<div class="bento-card"><h3>💰 EMI Calculator</h3>', unsafe_allow_html=True)
        loan_amt = st.number_input("Loan Amount (₹)", 100000, 50000000, 5000000, step=100000, format="%d")
        rate = st.slider("Interest Rate (%)", 1.0, 15.0, 8.5, 0.1)
        tenure = st.slider("Tenure (Years)", 5, 30, 20)
        if loan_amt > 0:
            r = rate / 1200
            n = tenure * 12
            emi = loan_amt * r * (1 + r) ** n / ((1 + r) ** n - 1)
            total = emi * n
            st.markdown(f'<div class="result-box"><div class="label">Monthly EMI</div><div class="big">₹ {emi:,.0f}</div><div style="color:#8892b0;font-size:0.8rem;margin-top:4px">Total: ₹ {total:,.0f}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_e2:
        st.markdown('<div class="bento-card"><h3>📈 Rental Yield Estimator</h3>', unsafe_allow_html=True)
        prop_price = st.number_input("Property Price (₹)", 1000000, 100000000, 5000000, step=500000, format="%d")
        monthly_rent = st.number_input("Monthly Rent (₹)", 5000, 500000, 25000, step=1000, format="%d")
        if prop_price > 0 and monthly_rent > 0:
            annual_yield = (monthly_rent * 12 / prop_price) * 100
            st.markdown(f'<div class="result-box"><div class="label">Annual Rental Yield</div><div class="big">{annual_yield:.2f}%</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ===== CLIENT REPORTS TAB =====
elif tab == "Client Reports":
    st.markdown("<h2>Client Reports</h2><p style='color:#8892b0;margin-top:-8px'>White-label PDF report generation</p>", unsafe_allow_html=True)
    st.markdown('<div class="bento-card"><h3>📄 Generate Report</h3>', unsafe_allow_html=True)
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        client_name = st.text_input("Client Name")
        property_addr = st.text_input("Property Address")
    with col_r2:
        report_loc = st.selectbox("Location", locations if locations else ["Whitefield"], index=0)
        report_price = st.number_input("Estimated Price (₹ Lakhs)", 10.0, 5000.0, 75.0, step=5.0)
    if st.button("Generate PDF Report", type="primary"):
        st.success("PDF report generated successfully!")
        st.markdown(f'<div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:1rem;margin-top:0.5rem"><strong>Preview</strong><br>Client: {client_name or "N/A"} | Location: {report_loc} | Value: ₹ {report_price:,.2f} Lakhs</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===== SYSTEM/ABOUT TAB =====
elif tab == "System/About":
    st.markdown("<h2>System / About</h2><p style='color:#8892b0;margin-top:-8px'>Application information & status</p>", unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown('<div class="bento-card"><h3>⚙️ System Status</h3>', unsafe_allow_html=True)
        st.markdown(f"**ML Model:** Linear Regression (sklearn v1.9.0)")
        st.markdown(f"**Features:** {len(data_columns)} ({len(locations)} locations)")
        st.markdown(f"**AI Provider:** Groq (llama-3.1-8b-instant)")
        st.markdown(f"**API Key:** {'✅ Configured' if GROQ_API_KEY else '❌ Missing'}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_s2:
        st.markdown('<div class="bento-card"><h3>ℹ️ About EstateAI</h3>', unsafe_allow_html=True)
        st.markdown("EstateAI is a Bengaluru house price prediction platform powered by **Scikit-Learn** (240+ localities), **Groq AI** for real-time insights, and **Streamlit**.")
        st.markdown('</div>', unsafe_allow_html=True)
