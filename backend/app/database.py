
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "journey.db"


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    schema = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        consent_to_link INTEGER NOT NULL,
        segment TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS pages (
        page_id TEXT PRIMARY KEY,
        page_name TEXT NOT NULL,
        page_type TEXT
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT,
        price REAL
    );

    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        customer_id TEXT,
        channel TEXT,
        device_id TEXT,
        started_at TEXT,
        is_bot INTEGER DEFAULT 0,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS journey_events (
        event_id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        page_id TEXT,
        product_id TEXT,
        event_type TEXT,
        channel TEXT,
        event_ts TEXT,
        ingestion_ts TEXT,
        is_late INTEGER DEFAULT 0,
        is_duplicate INTEGER DEFAULT 0,
        issue_type TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(session_id),
        FOREIGN KEY(page_id) REFERENCES pages(page_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );

    CREATE TABLE IF NOT EXISTS carts (
        cart_id TEXT PRIMARY KEY,
        session_id TEXT,
        customer_id TEXT,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(session_id),
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        session_id TEXT,
        customer_id TEXT,
        order_total REAL,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(session_id),
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS support_tickets (
        ticket_id TEXT PRIMARY KEY,
        session_id TEXT,
        customer_id TEXT,
        issue_category TEXT,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(session_id),
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS experiments (
        experiment_id TEXT PRIMARY KEY,
        experiment_name TEXT,
        start_date TEXT,
        end_date TEXT
    );

    CREATE TABLE IF NOT EXISTS experiment_assignments (
        experiment_id TEXT,
        session_id TEXT,
        variant TEXT,
        PRIMARY KEY(experiment_id, session_id),
        FOREIGN KEY(experiment_id) REFERENCES experiments(experiment_id),
        FOREIGN KEY(session_id) REFERENCES sessions(session_id)
    );

    CREATE TABLE IF NOT EXISTS journey_outcomes (
        outcome_id TEXT PRIMARY KEY,
        session_id TEXT UNIQUE,
        outcome TEXT,
        completed_stage TEXT,
        generated_at TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(session_id)
    );

    CREATE INDEX IF NOT EXISTS idx_events_session
    ON journey_events(session_id);

    CREATE INDEX IF NOT EXISTS idx_events_timestamp
    ON journey_events(event_ts);
    """

    cursor.executescript(schema)
    conn.commit()
    conn.close()

    print("Database and all 10 core entities created successfully.")


if __name__ == "__main__":
    create_tables()
