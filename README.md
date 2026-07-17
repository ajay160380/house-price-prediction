<div align="center">

# EstateAI 🏡

**AI-Powered Bengaluru Real Estate Intelligence**

[![Live Demo](https://img.shields.io/badge/🚀_View_Live_Demo_on_Render-1DA1F2?style=for-the-badge&logo=render&logoColor=white)](https://house-price-prediction-l7qm.onrender.com)

---

</div>

## 📋 Project Overview

EstateAI is a full-stack SaaS dashboard for predicting house prices in Bengaluru using Machine Learning, enriched with real-time AI market insights. Built with a premium Glassmorphism UI and an interactive SPA experience.

---

## ✨ Key Features

- **🔮 Predictor Engine** — Scikit-Learn Linear Regression model covering **240+ localities** across Bengaluru with 95% confidence price range estimation.
- **🤖 AI Market Insights** — Integration with **Groq API (Llama-3)** for real-time investment scores, safety ratings, and intelligent neighborhood analysis.
- **💰 Financial Hub** — Interactive **EMI Calculator** with adjustable interest rates & tenure, plus a **Rental Yield Estimator** for instant ROI analysis.
- **🗺️ Interactive Maps** — Dynamic **Leaflet.js** mapping with Nominatim geocoding, fly-to animations, and location-aware markers.
- **🎨 Premium UI/UX** — Single Page Application (SPA) with dark-themed **Glassmorphism Bento Grid**, animated score rings, and responsive design.
- **📄 Client Reports** — White-label PDF report generation with property valuation, AI insights, and 5-year forecast data.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.14, Django 6.0 |
| **ML Engine** | Scikit-Learn (LinearRegression) |
| **AI Provider** | Groq API (Llama-3.1-8B) |
| **Frontend** | HTML5, Vanilla JS, CSS3 |
| **Visualization** | Chart.js, Leaflet.js |
| **PDF Engine** | html2pdf.js |
| **Server** | Gunicorn + Whitenoise |
| **Hosting** | Render.com |

---

## 📦 Local Installation

```bash
# Clone the repository
git clone https://github.com/ajay160380/house-price-prediction.git
cd "house price prediction system "

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo 'GROQ_API_KEY="your_groq_api_key_here"' > .env

# Run the development server
python manage.py runserver
```

Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## 🧠 ML Model

- **Algorithm:** Linear Regression (Scikit-Learn)
- **Features:** 243 dimensions (sqft, BHK, bathrooms, 240 location dummies)
- **Training Data:** Bengaluru house prices across 2,000+ data points
- **Accuracy:** ~85% R² score on holdout validation

---

## 🔒 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key for AI insights ([Get one here](https://console.groq.com)) |

Add to `.env` file in the project root (never commit this file).

---

## 📸 Screenshots

| Predictor Engine | Market Analytics |
|:----------------:|:----------------:|
| *Form inputs with real-time prediction & AI insights* | *5-year forecast charts & AI score rings* |

---

## 👨‍💻 Developer

**Ajay** — B.Tech student at **Babu Banarasi Das (BBD) University, Lucknow**

> This project was built as a portfolio demonstration of full-stack development, machine learning integration, and cloud deployment. It showcases expertise in Python/Django, Scikit-Learn, REST API design, and modern UI/UX principles.

---

<div align="center">

**⭐ Star this repo if you found it useful!**

</div>
