# Customer Journey Intelligence Platform

### YottaFlex AI Recruitment Project

An end-to-end customer journey analytics platform that generates, stores, validates, and analyses synthetic customer interaction data. The dashboard helps explore customer behaviour, conversion performance, journey drop-offs, channel activity, and data-quality issues.

## 1. Project Overview

Customers interact with businesses through multiple touchpoints, including websites, mobile applications, purchases, and customer support. Analysing these interactions helps teams understand how customers move through a journey and where they leave before completing a purchase.

This project combines a Python FastAPI backend, a SQLite database, a reproducible synthetic-data generator, and a React dashboard.

> **Data note:** This project uses synthetic data and does not contain real customer records.

## 2. Key Features

- **Synthetic Data Generation:** Generate reproducible customer, session, event, product, cart, order, support-ticket, experiment, and journey-outcome records.
- **Customer Journey Analytics:** Analyse progression through page views, product views, cart additions, checkout, and purchases.
- **Conversion Funnel:** Compare the number of non-bot sessions reaching each funnel stage and calculate stage drop-offs.
- **Journey Flow Visualisation:** Explore journey transitions and drop-offs through a Sankey chart.
- **Channel Analytics:** Compare sessions by their initial channel and inspect the channel recorded on individual events.
- **Anomaly Monitoring:** Identify bot sessions, delayed events, duplicate conversion events, and sessions without a linked customer identity.
- **Ground-Truth Labels:** Store generated labels for bot traffic, late ingestion, duplicate conversions, unlinked identities, and synthetic identity-collision scenarios.
- **Data Validation:** Check primary-key uniqueness, foreign-key integrity, consent-aware identity linking, timestamp consistency, order-to-purchase reconciliation, session outcomes, and duplicate-event labels.
- **Recent Events:** Inspect event identifiers, session identifiers, channels, event types, timestamps, and anomaly flags.

## 3. Technology Stack

| Component | Technologies |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Database | SQLite |
| Data Processing | Pandas, NumPy |
| Frontend | React, JavaScript, Vite |
| Data Visualisation | Recharts |
| API Documentation | FastAPI Swagger UI |
| Version Control | Git, GitHub |

## 4. Project Structure

```text
yottaflex-customer-journey-intelligence/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── main.py
│   ├── data/
│   │   ├── journey.db
│   │   └── ground_truth.csv
│   ├── generate_data.py
│   ├── validate_data.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   ├── main.jsx
│   │   └── JourneyFlow.jsx
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## 5. Getting Started

### Prerequisites

Install the following:

- Python 3.12 or a compatible Python version
- Node.js and npm
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/Srimeghana30/yottaflex-customer-journey-intelligence.git
cd yottaflex-customer-journey-intelligence
```

### Step 2: Set Up and Run the Backend

From the project root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

The repository includes the generated SQLite database and ground-truth CSV. To regenerate the synthetic data, run:

```powershell
python generate_data.py
```

The generator accepts optional session-count and seed arguments:

```powershell
python generate_data.py --sessions 1000 --seed 20261022
```

**Important:** Regenerating the data replaces the generated database records and rewrites `backend/data/ground_truth.csv`.

Run data validation:

```powershell
python validate_data.py
```

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

- Backend URL: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs

### Step 3: Set Up and Run the Frontend

Open a second terminal at the repository root:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL: http://localhost:5173

Keep both the backend and frontend development servers running while using the dashboard.

## 6. API Endpoints

The backend exposes the following read endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns the API status message. |
| GET | `/api/summary` | Returns customer, session, event, order, bot, delayed-event, and duplicate-event totals, plus the overall order-to-session percentage. |
| GET | `/api/funnel` | Returns funnel-stage session counts and drop-offs. Bot sessions are excluded. |
| GET | `/api/journey-flow` | Returns non-bot journey stage counts and Sankey nodes and links for transitions and drop-offs. |
| GET | `/api/channels` | Returns non-bot session and purchase counts grouped by the session's initial channel. |
| GET | `/api/anomalies` | Returns counts for bot traffic, delayed events, duplicate conversions, and unlinked customer identities. |
| GET | `/api/events?limit=25` | Returns the most recently ingested events. The optional `limit` parameter is restricted to 1–100 and defaults to 25. |

You can test these endpoints through Swagger UI at http://127.0.0.1:8000/docs.

### Metric Interpretation

- The summary conversion percentage is calculated as **orders ÷ all sessions × 100**.
- The funnel and journey-flow endpoints exclude bot sessions.
- Channel grouping uses the session's initial channel. Individual journey events also store their own channel, so event-level channel values may differ during a session.
- Duplicate purchase events are flagged separately and are not counted as additional purchases in the funnel or channel purchase counts.

## 7. Data Generation and Validation

The data generator uses a fixed default random seed (`20261022`) so the same inputs produce reproducible synthetic data. You can change the number of sessions with `--sessions` and the seed with `--seed`.

The generated ground-truth CSV contains these fields:

| Field | Description |
|---|---|
| `record_id` | Event or session record identifier associated with the label. |
| `session_id` | Related session identifier. |
| `issue_type` | Generated issue category. |
| `expected_reason` | Explanation of the expected issue or handling. |

The validation script checks database keys and relationships, consent-aware customer linking, event timestamp order, order and purchase consistency, session outcome completeness, and duplicate-event labels. It exits with a validation error if an implemented check fails.

## 8. Running the Project Again

For future runs, start the backend and frontend in separate terminals.

**Terminal 1 — Backend**

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

**Terminal 2 — Frontend**

```powershell
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

## 9. Repository

GitHub: https://github.com/Srimeghana30/yottaflex-customer-journey-intelligence
