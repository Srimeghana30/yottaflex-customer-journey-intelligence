# Customer Journey Intelligence Platform

### YottaFlex AI Recruitment Project

An end-to-end Customer Journey Intelligence platform that generates, stores, validates, and analyses synthetic customer journey data. It helps understand customer behaviour, conversion performance, journey drop-offs, channel distribution, and data-quality issues through an interactive analytics dashboard.

## 1. Project Overview

Customers interact with businesses through different touchpoints, such as websites, mobile applications, purchases, and customer support.

Understanding these interactions helps businesses identify where customers experience friction and where they abandon their journey.

This project provides a data-driven approach to analysing customer journeys. It combines a Python-based backend, a relational database, a synthetic data generator, and a React dashboard.

## 2. Key Features

- **Synthetic Data Generation:** Generate reproducible customer, session, event, product, cart, order, and support-ticket data.
- **Customer Journey Analytics:** Analyse customer progression through different journey stages.
- **Conversion Funnel:** Track progression from page views to product views, cart additions, checkout, and purchases.
- **Journey Flow Visualisation:** Visualise customer progression and drop-offs using a Sankey chart.
- **Channel Analytics:** Compare customer sessions across available channels.
- **Anomaly Detection:** Identify data-quality exceptions such as delayed events, duplicate events, bot sessions, and identity gaps where supported by the generated data.
- **Data Quality Monitoring:** Review event and timestamp-related data-quality indicators.
- **Recent Events:** Inspect customer events, timestamps, channels, and event status.
- **Data Validation:** Run validation checks on generated data and database relationships.
- **Ground Truth Dataset:** Maintain a separate ground-truth dataset for evaluation and verification.

## 3. Technology Stack

| Component | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Database | SQLite, SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Frontend | React, Vite, JavaScript |
| Data Visualisation | Recharts |
| API Testing | FastAPI Swagger UI |
| Version Control | Git, GitHub |

## 4. Project Structure

```text
YottaFlexAI/
│
├── backend/
│   ├── app/
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── data/
│   │   └── generated datasets
│   │
│   ├── generate_data.py
│   └── validate_data.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── JourneyFlow.jsx
│   │
│   ├── package.json
│   └── index.html
│
├── docs/
│
├── README.md
└── .gitignore
```

*Note: This structure is illustrative. Keep the filenames and folders consistent with your actual project.*

## 5. Getting Started

### Prerequisites

Install the following before running the project:

- Python 3.12 or a compatible Python version
- Node.js and npm
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/yottaflex-customer-journey-intelligence.git
cd yottaflex-customer-journey-intelligence
```

### Step 2: Set Up the Backend

Open a terminal in the project root:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Generate the datasets if they are not already included or if you want to regenerate them:

```bash
python generate_data.py
```

Run data validation:

```bash
python validate_data.py
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend URL: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### Step 3: Set Up the Frontend

Open another terminal:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend URL: http://localhost:5173

Keep both backend and frontend servers running while using the dashboard.

## 6. API Endpoints

| Endpoint
