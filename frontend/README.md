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

*The structure above is a guide to the main project files. Keep the actual filenames and folders in your repository consistent with your implementation.*

## 5. Getting Started

### Prerequisites

Install the following before running the project:

- Python 3.12 or a compatible Python version
- Node.js and npm
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/yottaflex-customer-journey-intelligence.git
cd yottaflex-customer-journey-intelligence
```

### Step 2: Set up the backend

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

Backend URL:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### Step 3: Set up the frontend

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

Frontend URL:

`http://localhost:5173`

Keep both backend and frontend servers running while using the dashboard.

## 6. API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Backend health or root response |
| `GET /api/summary` | Customer journey summary and KPI metrics |
| `GET /api/funnel` | Customer conversion funnel |
| `GET /api/channels` | Session distribution by channel |
| `GET /api/anomalies` | Detected anomalies and data-quality indicators |
| `GET /api/events` | Recent customer events |
| `GET /api/journey-flow` | Customer journey flow and drop-off data |

Interactive API documentation is available at `/docs`.

## 7. Data Generation and Validation

The project uses synthetic customer journey data rather than real customer information.

The data-generation process uses a fixed random seed to support reproducibility. The generated datasets cover customer profiles, sessions, journey events, products, carts, orders, support tickets, experiments, and journey outcomes.

The validation script checks important data-integrity conditions, including database relationships, consent-related identity checks, timestamp ordering, and dataset availability.

A separate ground-truth dataset is maintained for evaluation.

## 8. Dashboard Modules

1. **Overview:** Customer, session, event, order, bot-session, and conversion metrics.
2. **Customer Journey Flow:** Visual representation of journey stages and drop-offs.
3. **Conversion Funnel:** Analysis of progression through purchase stages.
4. **Channel Distribution:** Comparison of sessions across channels.
5. **Friction and Anomaly Detection:** Visibility into detected data-quality exceptions.
6. **Data Quality Overview:** Monitoring of delayed events, duplicate events, and identity gaps.
7. **Recent Customer Events:** Inspection of recent event records.

## 9. Screenshots

Add screenshots of your completed dashboard here.

For example:

```markdown
![Customer Journey Dashboard](docs/dashboard.png)
```

You can add more screenshots for the journey flow, funnel, and anomaly sections.

## 10. Current Dataset Note

The included datasets are synthetic and intended for development, demonstration, and evaluation. Results and metrics describe the generated dataset and should not be interpreted as real-world business performance.

## 11. Future Enhancements

- Advanced cross-channel identity resolution.
- Customer-level journey timelines.
- Experiment performance analysis.
- More detailed drop-off investigation.
- Additional anomaly detection and monitoring.
- Production database and deployment integration.

## 12. AI Assistance Disclosure

AI assistance was used during development for guidance, debugging, code review, and documentation support. The project was implemented, tested, and reviewed as part of the recruitment assignment.

## 13. Author

**Ayyagari Sri Meghana Supriya**

GitHub: https://github.com/Srimeghana30

---

**Project:** Customer Journey Intelligence Platform  
**Organisation:** YottaFlex AI  
**Purpose:** Recruitment Project
