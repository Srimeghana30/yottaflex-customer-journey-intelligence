
import random
import csv
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.database import get_db, create_tables

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

CHANNELS = ["web", "app", "support"]
CUSTOMER_CHANNELS = ["web", "app"]

random.seed(20261022)


def generate(sessions_count=1000, seed=20261022):
    random.seed(seed)
    create_tables()

    DATA.mkdir(exist_ok=True)

    conn = get_db()
    cur = conn.cursor()

    # Clear generated records in dependency order
    for table in [
        "journey_outcomes",
        "experiment_assignments",
        "support_tickets",
        "orders",
        "carts",
        "journey_events",
        "sessions",
        "products",
        "pages",
        "customers",
        "experiments"
    ]:
        cur.execute(f"DELETE FROM {table}")

    # Fixed reference time supports reproducibility
    now = datetime(2026, 10, 1, tzinfo=timezone.utc)

    # --------------------------------------------------
    # MASTER DATA
    # --------------------------------------------------

    customers = []

    customer_count = max(101, sessions_count // 2)

    for i in range(1, customer_count + 1):
        cid = f"CUS-{i:06d}"
        consent = random.choice([0, 1])

        customers.append({
            "id": cid,
            "consent": consent
        })

        cur.execute(
            """
            INSERT INTO customers
            VALUES (?, ?, ?, ?)
            """,
            (
                cid,
                consent,
                random.choice(["new", "returning", "loyal"]),
                now.isoformat()
            )
        )

    pages = [
        ("PAG-001", "Home", "landing"),
        ("PAG-002", "Product", "product"),
        ("PAG-003", "Cart", "cart"),
        ("PAG-004", "Checkout", "checkout"),
        ("PAG-005", "Support", "support")
    ]

    products = [
        ("PRD-001", "Headphones", 89.0),
        ("PRD-002", "Smart Watch", 129.0),
        ("PRD-003", "Backpack", 49.0)
    ]

    cur.executemany(
        "INSERT INTO pages VALUES (?, ?, ?)",
        pages
    )

    cur.executemany(
        "INSERT INTO products VALUES (?, ?, ?)",
        products
    )

    cur.execute(
        """
        INSERT INTO experiments
        VALUES (?, ?, ?, ?)
        """,
        (
            "EXP-2026-000001",
            "Checkout Optimization",
            "2026-10-01",
            "2026-12-31"
        )
    )

    truth = []

    # Device identifiers previously associated with customers.
    # Reusing one across different customers creates a labelled
    # synthetic identity-collision scenario.
    known_devices = []

    total_events = 0
    cross_channel_sessions = 0

    # --------------------------------------------------
    # SESSION AND EVENT DATA
    # --------------------------------------------------

    for i in range(1, sessions_count + 1):

        sid = f"SES-2026-{i:06d}"

        selected_customer = random.choice(customers)

        consent = selected_customer["consent"]

        # Identity linking is allowed only with consent.
        customer_id = (
            selected_customer["id"]
            if consent == 1 and random.random() > 0.20
            else None
        )

        start = now - timedelta(
            minutes=random.randint(1, 40000)
        )

        initial_channel = random.choice(CUSTOMER_CHANNELS)

        is_bot = int(random.random() < 0.05)

        # ----------------------------------------------
        # Synthetic identity collision
        # ----------------------------------------------

        device_id = f"DEV-{random.randint(1, 100):04d}"

        identity_collision = False

        if known_devices and random.random() < 0.02:

            possible_matches = [
                item for item in known_devices
                if item["customer_id"] != selected_customer["id"]
            ]

            if possible_matches:
                previous = random.choice(possible_matches)
                device_id = previous["device_id"]
                identity_collision = True

        known_devices.append({
            "device_id": device_id,
            "customer_id": selected_customer["id"]
        })

        cur.execute(
            """
            INSERT INTO sessions
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                sid,
                customer_id,
                initial_channel,
                device_id,
                start.isoformat(),
                is_bot
            )
        )

        cur.execute(
            """
            INSERT INTO experiment_assignments
            VALUES (?, ?, ?)
            """,
            (
                "EXP-2026-000001",
                sid,
                random.choice(["control", "variant"])
            )
        )

        if identity_collision:
            truth.append([
                sid,
                sid,
                "incorrect_identity_merge",
                "Shared device identifier across different customer identities; do not merge without reliable identity evidence"
            ])

        # ----------------------------------------------
        # Journey progression
        # ----------------------------------------------

        progress = random.choices(
            [1, 2, 3, 4],
            weights=[30, 30, 20, 20]
        )[0]

        if is_bot:
            progress = 1

        journey = [
            "page_view",
            "product_view"
        ]

        if progress >= 2:
            journey.append("add_to_cart")

        if progress >= 3:
            journey.append("checkout_started")

        if progress >= 4:
            journey.append("purchase")

        has_support = random.random() < 0.08

        if has_support:
            journey.append("support_contact")

        # Expand each session to 20 base events.
        # This supports a target of approximately 2 million
        # events for 100,000 sessions.
        filler_events = [
            "page_view",
            "product_view"
        ]

        while len(journey) < 20:
            insert_at = random.randint(1, len(journey))
            journey.insert(
                insert_at,
                random.choice(filler_events)
            )

        # ----------------------------------------------
        # Cross-channel event assignment
        # ----------------------------------------------

        event_channels = []

        for j in range(20):

            if j == 0:
                channel = initial_channel

            elif j == 7:
                # Switch between web and app
                channel = (
                    "app" if initial_channel == "web"
                    else "web"
                )

            elif j == 14:
                # Continue journey through support channel
                channel = "support"

            else:
                channel = random.choice(CHANNELS)

            event_channels.append(channel)

        if len(set(event_channels)) > 1:
            cross_channel_sessions += 1

        # ----------------------------------------------
        # Generate events
        # ----------------------------------------------

        for j, event_type in enumerate(journey, start=1):

            event_id = f"EVT-{sid}-{j:06d}"

            event_time = start + timedelta(
                seconds=j * random.randint(30, 120)
            )

            ingestion_time = event_time + timedelta(
                seconds=random.randint(10, 120)
            )

            is_late = int(random.random() < 0.05)

            if is_late:
                ingestion_time += timedelta(minutes=10)

            is_duplicate = int(
                event_type == "purchase"
                and random.random() < 0.10
            )

            event_channel = event_channels[j - 1]

            page_id = random.choice(pages)[0]

            product_id = (
                random.choice(products)[0]
                if event_type in [
                    "product_view",
                    "add_to_cart",
                    "purchase"
                ]
                else None
            )

            issue = (
                "late_ingestion" if is_late
                else "duplicate_conversion" if is_duplicate
                else None
            )

            cur.execute(
                """
                INSERT INTO journey_events
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    sid,
                    page_id,
                    product_id,
                    event_type,
                    event_channel,
                    event_time.isoformat(),
                    ingestion_time.isoformat(),
                    is_late,
                    0,
                    issue
                )
            )

            total_events += 1

            if is_late:
                truth.append([
                    event_id,
                    sid,
                    "late_ingestion",
                    "Ingestion delayed over five minutes; order by event time for journey reconstruction"
                ])

            # Duplicate conversion is a separate labelled event.
            if is_duplicate:

                duplicate_id = f"EVT-{sid}-{j + 100000:06d}"

                cur.execute(
                    """
                    INSERT INTO journey_events
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        duplicate_id,
                        sid,
                        page_id,
                        product_id,
                        event_type,
                        event_channel,
                        event_time.isoformat(),
                        ingestion_time.isoformat(),
                        0,
                        1,
                        "duplicate_conversion"
                    )
                )

                total_events += 1

                truth.append([
                    duplicate_id,
                    sid,
                    "duplicate_conversion",
                    "Repeated purchase event; count the underlying conversion only once"
                ])

        # ----------------------------------------------
        # Orders
        # ----------------------------------------------

        if progress == 4 and not is_bot:

            order_id = f"ORD-{i:06d}"

            total = round(random.uniform(20, 200), 2)

            cur.execute(
                """
                INSERT INTO orders
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    order_id,
                    sid,
                    customer_id,
                    total,
                    "paid",
                    start.isoformat()
                )
            )

        # ----------------------------------------------
        # Carts
        # ----------------------------------------------

        if progress >= 2:

            cart_id = f"CART-{i:06d}"

            cur.execute(
                """
                INSERT INTO carts
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    cart_id,
                    sid,
                    customer_id,
                    "converted" if progress == 4 else "abandoned",
                    start.isoformat()
                )
            )

        # ----------------------------------------------
        # Support tickets
        # ----------------------------------------------

        if has_support:

            cur.execute(
                """
                INSERT INTO support_tickets
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    f"TKT-{i:06d}",
                    sid,
                    customer_id,
                    "payment_or_delivery",
                    "open",
                    start.isoformat()
                )
            )

        # ----------------------------------------------
        # Journey outcome
        # ----------------------------------------------

        outcome = (
            "converted"
            if progress == 4 and not is_bot
            else "abandoned"
        )

        stage = {
            1: "view",
            2: "cart",
            3: "checkout",
            4: "purchase"
        }[progress]

        cur.execute(
            """
            INSERT INTO journey_outcomes
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                f"OUT-{sid}",
                sid,
                outcome,
                stage,
                now.isoformat()
            )
        )

        # ----------------------------------------------
        # Ground-truth labels
        # ----------------------------------------------

        if is_bot:
            truth.append([
                sid,
                sid,
                "bot_traffic",
                "Exclude bot session from customer conversion analytics"
            ])

        if customer_id is None:
            truth.append([
                sid,
                sid,
                "identity_not_linked",
                "Anonymous identity must not be linked without consent"
            ])

        # Periodic commits reduce the amount of pending work
        if i % 5000 == 0:
            conn.commit()
            print(
                f"Generated {i:,}/{sessions_count:,} sessions "
                f"| {total_events:,} events"
            )

    conn.commit()
    conn.close()

    # ----------------------------------------------
    # Ground truth CSV
    # ----------------------------------------------

    with open(
        DATA / "ground_truth.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "record_id",
            "session_id",
            "issue_type",
            "expected_reason"
        ])

        writer.writerows(truth)

    print("\nDATA GENERATION COMPLETED")
    print("-------------------------")
    print(f"Sessions: {sessions_count:,}")
    print(f"Base and duplicate events: {total_events:,}")
    print(f"Cross-channel sessions: {cross_channel_sessions:,}")
    print(f"Ground-truth records: {len(truth):,}")
    print(f"Random seed: {seed}")
    print(f"Ground truth: {DATA / 'ground_truth.csv'}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--sessions",
        type=int,
        default=1000
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=20261022
    )

    args = parser.parse_args()

    generate(args.sessions, args.seed)
