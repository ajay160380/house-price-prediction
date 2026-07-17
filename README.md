<div align="center">

# 🏡 EstateAI

### 🤖 AI-Powered Bengaluru Real Estate Intelligence

<p align="center">
<img src="assets/demo.gif" width="100%" alt="EstateAI Demo"/>
</p>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://house-price-prediction-l7qm.onrender.com)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/ajay160380/house-price-prediction)

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)


</div>

---

# 📖 Project Overview

**EstateAI** is an AI-powered Full Stack Real Estate Intelligence Platform that predicts Bengaluru property prices using Machine Learning while leveraging **Groq Llama-3 AI** to provide neighborhood intelligence, investment insights, financial analysis, and interactive visualizations.

The application combines **Machine Learning**, **Artificial Intelligence**, **Interactive Maps**, and **Financial Analytics** into one premium Glassmorphism dashboard.

---

# 🚀 Features

- 🏠 AI House Price Prediction
- 🤖 Groq AI Market Insights
- 📍 Interactive Maps (Leaflet.js)
- 📊 Dynamic Charts
- 💰 EMI Calculator
- 📈 Rental Yield Calculator
- 📄 PDF Report Generator
- 🌙 Glassmorphism Dark UI
- 📱 Fully Responsive
- ⚡ Lightning Fast SPA

---

# 🏗️ Complete System Architecture

```mermaid
flowchart TD

A[👤 User]

A --> B[🌐 Frontend<br>HTML CSS JavaScript]

B --> C[Django Backend API]

C --> D[Machine Learning Model]

C --> E[Groq AI API]

D --> F[Price Prediction]

E --> G[AI Market Insights]

F --> H[Dashboard]

G --> H

H --> I[Charts]

H --> J[Interactive Maps]

H --> K[PDF Report]

H --> L[Financial Calculator]
```

---

# 🧠 Machine Learning Pipeline

```mermaid
flowchart LR

A[Housing Dataset]

A --> B[Data Cleaning]

B --> C[Feature Engineering]

C --> D[One Hot Encoding]

D --> E[Train Test Split]

E --> F[Linear Regression]

F --> G[Model Evaluation]

G --> H[Saved Model]

H --> I[Django API]
```

---

# ⚡ Application Workflow

```mermaid
graph LR

User --> Input

Input --> Django

Django --> ML

ML --> Prediction

Prediction --> Groq

Groq --> Insights

Insights --> Dashboard

Dashboard --> Charts

Dashboard --> Maps

Dashboard --> PDF

Dashboard --> User
```

---

# 📊 Model Performance

| Metric | Value |
|---------|-------|
| Algorithm | Multiple Linear Regression |
| Dataset | 2,000+ Records |
| Features | 243 |
| Locations | 240+ |
| Validation Score | **~85% R²** |
| Prediction | Real-Time |

---

# 🛠️ Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | Python, Django 6 |
| Machine Learning | Scikit-Learn, NumPy, Pandas |
| AI | Groq API (Llama-3.1-8B) |
| Frontend | HTML5, CSS3, JavaScript |
| Charts | Chart.js |
| Maps | Leaflet.js |
| Deployment | Render, Gunicorn, WhiteNoise |

---

# 📂 Project Structure

```text
EstateAI
│
├── predictor/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── model/
├── dataset/
├── requirements.txt
├── manage.py
└── README.md
```

---

# 📸 Application Preview

| Home | Prediction |
|------|------------|
| ![](assets/home.png) | ![](assets/predict.png) |

| AI Insights | PDF Report |
|--------------|------------|
| ![](assets/insights.png) | ![](assets/report.png) |

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/ajay160380/house-price-prediction.git

cd house-price-prediction
```

## Create Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create Environment Variable

Create a **.env** file.

```env
GROQ_API_KEY=your_api_key_here
```

## Run Server

```bash
python manage.py runserver
```

Open

```
http://localhost:8000
```

---

# 🌍 Live Demo

### 🚀 https://house-price-prediction-l7qm.onrender.com

---

# 🛣️ Future Roadmap

- ✅ House Price Prediction
- ✅ Groq AI Integration
- ✅ Interactive Maps
- ✅ PDF Reports
- ✅ Financial Dashboard
- 🔄 Authentication
- 🔄 PostgreSQL
- 🔄 Docker
- 🔄 Recommendation Engine
- 🔄 AI Chat Assistant
- 🔄 Property Image Search

---

# 👨‍💻 Developer

## Ajay Vishwakarma

🎓 **B.Tech CSE (AI)**

🏫 **Babu Banarasi Das University, Lucknow**

### Skills

- Python
- Django
- Machine Learning
- Artificial Intelligence
- SQL
- JavaScript
- REST APIs
- Full Stack Development

This project demonstrates production-ready skills in:

- Full Stack Development
- Machine Learning
- AI Integration
- REST API Development
- Modern UI/UX
- Cloud Deployment

---

<div align="center">

# ⭐ If you like this project, give it a Star ⭐

Made with ❤️ by **Ajay Vishwakarma**

</div>
