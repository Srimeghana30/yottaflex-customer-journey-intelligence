
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import get_db

app = FastAPI(
    title="YottaFlex Customer Journey Analytics",
    description="Cross-channel customer journey analytics platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)


def fetch_all(sql, params=()):
    conn = get_db()
    result = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(row) for row in result]


@app.get("/")
def home():
    return {
        "message": "Customer Journey Analytics API",
        "status": "running"
    }


@app.get("/api/summary")
def summary():
    result = fetch_all("""
        SELECT
            (SELECT COUNT(*) FROM customers) AS customers,
            (SELECT COUNT(*) FROM sessions) AS sessions,
            (SELECT COUNT(*) FROM journey_events) AS events,
            (SELECT COUNT(*) FROM orders) AS orders,
            (SELECT COUNT(*) FROM sessions WHERE is_bot=1) AS bots,
            (SELECT COUNT(*) FROM journey_events WHERE is_late=1) AS late_events,
            (SELECT COUNT(*) FROM journey_events WHERE is_duplicate=1) AS duplicates
    """)

    data = result[0]

    data["conversion_rate"] = round(
        data["orders"] / data["sessions"] * 100, 2
    ) if data["sessions"] else 0

    return data


@app.get("/api/funnel")
def funnel():
    result = fetch_all("""
        SELECT
            s.session_id,
            MAX(CASE WHEN e.event_type IN
                ('page_view','product_view') THEN 1 ELSE 0 END) AS viewed,
            MAX(CASE WHEN e.event_type='add_to_cart'
                THEN 1 ELSE 0 END) AS cart,
            MAX(CASE WHEN e.event_type='checkout_started'
                THEN 1 ELSE 0 END) AS checkout,
            MAX(CASE WHEN e.event_type='purchase'
                AND e.is_duplicate=0 THEN 1 ELSE 0 END) AS purchased
        FROM sessions s
        LEFT JOIN journey_events e
            ON s.session_id=e.session_id
        WHERE s.is_bot=0
        GROUP BY s.session_id
    """)

    stages = [
        ("Viewed", "viewed"),
        ("Added to cart", "cart"),
        ("Checkout", "checkout"),
        ("Purchased", "purchased")
    ]

    output = []
    previous = None

    for name, key in stages:
        count = sum(row[key] for row in result)

        output.append({
            "stage": name,
            "sessions": count,
            "dropoff": (
                max(previous - count, 0)
                if previous is not None else 0
            )
        })

        previous = count

    return output


@app.get("/api/journey-flow")
def journey_flow():
    # Get the journey progression for every non-bot session.
    result = fetch_all("""
        SELECT
            s.session_id,

            MAX(CASE WHEN e.event_type = 'page_view'
                THEN 1 ELSE 0 END) AS viewed,

            MAX(CASE WHEN e.event_type = 'product_view'
                THEN 1 ELSE 0 END) AS product_viewed,

            MAX(CASE WHEN e.event_type = 'add_to_cart'
                THEN 1 ELSE 0 END) AS cart,

            MAX(CASE WHEN e.event_type = 'checkout_started'
                THEN 1 ELSE 0 END) AS checkout,

            MAX(CASE WHEN e.event_type = 'purchase'
                AND e.is_duplicate = 0
                THEN 1 ELSE 0 END) AS purchased

        FROM sessions s
        LEFT JOIN journey_events e
            ON s.session_id = e.session_id

        WHERE s.is_bot = 0
        GROUP BY s.session_id
    """)

    # Node positions for the Sankey visualization.
    node_names = [
        "Page Viewed",
        "Product Viewed",
        "Added to Cart",
        "Checkout Started",
        "Purchased",
        "Drop-off after Product",
        "Drop-off after Cart",
        "Drop-off after Checkout"
    ]

    # Count actual session transitions.
    links = {
        "page_to_product": 0,
        "product_to_cart": 0,
        "product_to_dropoff": 0,
        "cart_to_checkout": 0,
        "cart_to_dropoff": 0,
        "checkout_to_purchase": 0,
        "checkout_to_dropoff": 0
    }

    for row in result:
        if row["viewed"] and row["product_viewed"]:
            links["page_to_product"] += 1

        if row["product_viewed"]:
            if row["cart"]:
                links["product_to_cart"] += 1
            else:
                links["product_to_dropoff"] += 1

        if row["cart"]:
            if row["checkout"]:
                links["cart_to_checkout"] += 1
            else:
                links["cart_to_dropoff"] += 1

        if row["checkout"]:
            if row["purchased"]:
                links["checkout_to_purchase"] += 1
            else:
                links["checkout_to_dropoff"] += 1

    # Recharts Sankey uses numeric source and target indexes.
    node_index = {
        name: index
        for index, name in enumerate(node_names)
    }

    raw_links = [
        ("Page Viewed", "Product Viewed", links["page_to_product"]),
        ("Product Viewed", "Added to Cart", links["product_to_cart"]),
        ("Product Viewed", "Drop-off after Product", links["product_to_dropoff"]),
        ("Added to Cart", "Checkout Started", links["cart_to_checkout"]),
        ("Added to Cart", "Drop-off after Cart", links["cart_to_dropoff"]),
        ("Checkout Started", "Purchased", links["checkout_to_purchase"]),
        ("Checkout Started", "Drop-off after Checkout", links["checkout_to_dropoff"])
    ]

    sankey_links = [
        {
            "source": node_index[source],
            "target": node_index[target],
            "value": value
        }
        for source, target, value in raw_links
        if value > 0
    ]

    return {
        "total_sessions": len(result),
        "nodes": [
            {"name": name}
            for name in node_names
        ],
        "links": sankey_links,
        "stage_counts": {
            "page_viewed": sum(r["viewed"] for r in result),
            "product_viewed": sum(r["product_viewed"] for r in result),
            "added_to_cart": sum(r["cart"] for r in result),
            "checkout_started": sum(r["checkout"] for r in result),
            "purchased": sum(r["purchased"] for r in result)
        }
    }


@app.get("/api/channels")
def channels():
    return fetch_all("""
        SELECT
            s.channel,
            COUNT(DISTINCT s.session_id) AS sessions,

            COUNT(DISTINCT CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM journey_events e
                    WHERE e.session_id = s.session_id
                    AND e.event_type = 'purchase'
                    AND e.is_duplicate = 0
                )
                THEN s.session_id
            END) AS purchases

        FROM sessions s
        WHERE s.is_bot = 0
        GROUP BY s.channel
    """)



@app.get("/api/anomalies")
def anomalies():
    return [
        {
            "type": "Bot traffic",
            "count": fetch_all(
                "SELECT COUNT(*) AS n FROM sessions WHERE is_bot=1"
            )[0]["n"]
        },
        {
            "type": "Delayed events",
            "count": fetch_all(
                "SELECT COUNT(*) AS n FROM journey_events WHERE is_late=1"
            )[0]["n"]
        },
        {
            "type": "Duplicate conversions",
            "count": fetch_all(
                "SELECT COUNT(*) AS n FROM journey_events WHERE is_duplicate=1"
            )[0]["n"]
        },
        {
            "type": "Unlinked identities",
            "count": fetch_all(
                "SELECT COUNT(*) AS n FROM sessions WHERE customer_id IS NULL"
            )[0]["n"]
        }
    ]


@app.get("/api/events")
def events(limit: int = 25):
    limit = max(1, min(limit, 100))

    return fetch_all("""
        SELECT
            event_id,
            session_id,
            channel,
            event_type,
            event_ts,
            ingestion_ts,
            is_late,
            is_duplicate
        FROM journey_events
        ORDER BY ingestion_ts DESC
        LIMIT ?
    """, (limit,))
