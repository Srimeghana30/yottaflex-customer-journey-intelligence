
import { useEffect, useState } from "react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

import JourneyFlow from "./JourneyFlow";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState({});
  const [funnel, setFunnel] = useState([]);
  const [channels, setChannels] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [events, setEvents] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        setError("");

        const [s, f, c, a, e] = await Promise.all([
          fetch(`${API}/api/summary`),
          fetch(`${API}/api/funnel`),
          fetch(`${API}/api/channels`),
          fetch(`${API}/api/anomalies`),
          fetch(`${API}/api/events?limit=10`)
        ]);

        if (![s, f, c, a, e].every(r => r.ok)) {
          throw new Error("API request failed");
        }

        setSummary(await s.json());
        setFunnel(await f.json());
        setChannels(await c.json());
        setAnomalies(await a.json());
        setEvents(await e.json());

      } catch (err) {
        console.error(err);
        setError("Backend unavailable. Start FastAPI and refresh.");
      }
    }

    loadDashboard();
  }, []);

  const cards = [
    ["Customers", summary.customers],
    ["Sessions", summary.sessions],
    ["Total Events", summary.events],
    ["Orders", summary.orders],
    ["Bot Sessions", summary.bots],
    ["Conversion Rate", `${summary.conversion_rate ?? 0}%`]
  ];

  const COLORS = ["#6475e8", "#16a085", "#efa942"];

  return (
    <div className="dashboard">

      {/* HEADER */}
      <header>
        <div>
          <p className="subtitle">
            YOTTAFLEX AI | RECRUITMENT PROJECT
          </p>

          <h1>Customer Journey Intelligence</h1>

          <p>
            Cross-channel analytics and friction detection
          </p>
        </div>

        <span className="status">
          ● SYSTEM ACTIVE
        </span>
      </header>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {/* KPI METRICS */}
      <section className="metrics">
        {cards.map(([label, value]) => (
          <div className="metric" key={label}>
            <p>{label}</p>
            <h2>{value ?? "Loading..."}</h2>
          </div>
        ))}
      </section>

      {/* NEW CUSTOMER JOURNEY SANKEY VISUALIZATION */}
      <JourneyFlow />

      {/* EXISTING ANALYTICS */}
      <section className="charts">

        {/* CONVERSION FUNNEL */}
        <div className="panel">
          <h3>Customer Conversion Funnel</h3>

          <p className="muted">
            Session progression excluding bots
          </p>

          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={funnel}>
              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="stage" />
              <YAxis />

              <Tooltip />

              <Bar
                dataKey="sessions"
                fill="#6475e8"
                radius={[6, 6, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>

          <div className="stage-list">
            {funnel.map(item => (
              <div key={item.stage}>
                <b>{item.sessions}</b>
                <span>{item.stage}</span>
                <small>Drop-off: {item.dropoff}</small>
              </div>
            ))}
          </div>
        </div>

        {/* CHANNEL DISTRIBUTION */}
        <div className="panel">
          <h3>Channel Distribution</h3>

          <p className="muted">
            Customer sessions by channel
          </p>

          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={channels}
                dataKey="sessions"
                nameKey="channel"
                outerRadius={100}
                label
              >
                {channels.map((item, index) => (
                  <Cell
                    key={item.channel}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>

              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* ANOMALY DETECTION */}
        <div className="panel">
          <h3>Friction & Anomaly Detection</h3>

          <p className="muted">
            Detected data quality exceptions
          </p>

          {anomalies.map(item => (
            <div className="anomaly" key={item.type}>
              <span>{item.type}</span>
              <b>{item.count}</b>
            </div>
          ))}
        </div>

        {/* DATA QUALITY */}
        <div className="panel">
          <h3>Data Quality Overview</h3>

          <p className="muted">
            Event validation indicators
          </p>

          <div className="anomaly">
            <span>Delayed events</span>
            <b>{summary.late_events ?? 0}</b>
          </div>

          <div className="anomaly">
            <span>Duplicate events</span>
            <b>{summary.duplicates ?? 0}</b>
          </div>

          <div className="anomaly">
            <span>Identity gaps</span>
            <b>
              {anomalies.find(
                x => x.type === "Unlinked identities"
              )?.count ?? 0}
            </b>
          </div>
        </div>

      </section>

      {/* RECENT EVENTS TABLE */}
      <section className="panel events-panel">
        <h3>Recent Customer Events</h3>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Event ID</th>
                <th>Channel</th>
                <th>Event Type</th>
                <th>Event Timestamp</th>
                <th>Ingestion Timestamp</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {events.map(event => (
                <tr key={event.event_id}>
                  <td>{event.event_id}</td>
                  <td>{event.channel}</td>
                  <td>{event.event_type}</td>
                  <td>{event.event_ts}</td>
                  <td>{event.ingestion_ts}</td>

                  <td>
                    {event.is_duplicate
                      ? "Duplicate"
                      : event.is_late
                      ? "Delayed"
                      : "Normal"}
                  </td>
                </tr>
              ))}

              {events.length === 0 && (
                <tr>
                  <td colSpan="6">
                    No events available.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* FOOTER */}
      <footer>
        YottaFlex AI | Customer Journey Intelligence |
        Synthetic Data Analytics
      </footer>

    </div>
  );
}

export default App;
