
import sqlite3
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB = BASE / "data" / "journey.db"
GROUND = BASE / "data" / "ground_truth.csv"


def validate():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys=ON")

    checks = []

    tables = {
        "customers": "customer_id",
        "sessions": "session_id",
        "pages": "page_id",
        "products": "product_id",
        "journey_events": "event_id",
        "carts": "cart_id",
        "orders": "order_id",
        "support_tickets": "ticket_id",
        "experiments": "experiment_id",
        "journey_outcomes": "outcome_id"
    }

    for table, key in tables.items():
        total, unique = conn.execute(
            f"SELECT COUNT(*), COUNT(DISTINCT {key}) FROM {table}"
        ).fetchone()

        checks.append((
            f"{table}: unique primary keys",
            total == unique,
            total
        ))

    foreign_errors = conn.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    checks.append((
        "Foreign key integrity",
        len(foreign_errors) == 0,
        len(foreign_errors)
    ))

    invalid_consent = conn.execute("""
        SELECT COUNT(*)
        FROM sessions s
        JOIN customers c ON s.customer_id=c.customer_id
        WHERE c.consent_to_link=0
    """).fetchone()[0]

    checks.append((
        "Consent-aware identity linking",
        invalid_consent == 0,
        invalid_consent
    ))

    bad_timestamps = conn.execute("""
        SELECT COUNT(*)
        FROM journey_events
        WHERE ingestion_ts < event_ts
    """).fetchone()[0]

    checks.append((
        "Timestamp consistency",
        bad_timestamps == 0,
        bad_timestamps
    ))

    ground_truth_exists = GROUND.exists()

    checks.append((
        "Separate ground truth file",
        ground_truth_exists,
        ground_truth_exists
    ))
    
    
    # Orders must belong to completed purchase journeys
    invalid_orders = conn.execute("""
        SELECT COUNT(*)
        FROM orders o
        WHERE NOT EXISTS (
            SELECT 1
            FROM journey_events e
            WHERE e.session_id = o.session_id
            AND e.event_type = 'purchase'
            AND e.is_duplicate = 0
        )
    """).fetchone()[0]

    checks.append((
        "Order and purchase reconciliation",
        invalid_orders == 0,
        invalid_orders
    ))

    # Every session must have exactly one outcome
    missing_outcomes = conn.execute("""
        SELECT COUNT(*)
        FROM sessions s
        LEFT JOIN journey_outcomes o
        ON s.session_id = o.session_id
        WHERE o.session_id IS NULL
    """).fetchone()[0]

    checks.append((
        "Session outcome completeness",
        missing_outcomes == 0,
        missing_outcomes
    ))

    # Duplicate events must have explicit anomaly labels
    invalid_duplicates = conn.execute("""
        SELECT COUNT(*)
        FROM journey_events
        WHERE is_duplicate = 1
        AND issue_type != 'duplicate_conversion'
    """).fetchone()[0]

    checks.append((
        "Duplicate event labelling",
        invalid_duplicates == 0,
        invalid_duplicates
    ))


    conn.close()

    for name, passed, value in checks:
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}: {value}")

    if not all(item[1] for item in checks):
        raise SystemExit("Validation failed")

    print("\nAll implemented validation checks passed.")


if __name__ == "__main__":
    validate()
