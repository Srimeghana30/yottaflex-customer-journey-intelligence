
import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  Sankey,
  Tooltip
} from "recharts";

function JourneyFlow() {
  const [flow, setFlow] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function loadFlow() {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        "http://127.0.0.1:8000/api/journey-flow"
      );

      if (!response.ok) {
        throw new Error("Unable to load journey data");
      }

      const data = await response.json();
      setFlow(data);
    } catch (err) {
      setError("Could not load customer journey data. Check your backend.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadFlow();
  }, []);

  const stages = [
    ["Page viewed", "page_viewed"],
    ["Product viewed", "product_viewed"],
    ["Added to cart", "added_to_cart"],
    ["Checkout started", "checkout_started"],
    ["Purchased", "purchased"]
  ];

  return (
    <section className="content-card journey-flow-card">
      <div className="card-heading">
        <div>
          <h3>Customer Journey Flow</h3>
          <p>
            Visualizing customer progression and drop-offs
          </p>
        </div>

        <button
          className="journey-refresh"
          onClick={loadFlow}
          disabled={loading}
        >
          {loading ? "Loading..." : "↻ Refresh"}
        </button>
      </div>

      {loading && (
        <div className="journey-message">
          Loading customer journey...
        </div>
      )}

      {error && (
        <div className="journey-error">
          {error}
        </div>
      )}

      {flow && !loading && (
        <>
          <div className="journey-summary">
            <div>
              <span>Non-bot sessions</span>
              <strong>
                {flow.total_sessions.toLocaleString("en-IN")}
              </strong>
            </div>

            <div>
              <span>Converted sessions</span>
              <strong>
                {flow.stage_counts.purchased.toLocaleString("en-IN")}
              </strong>
            </div>

            <div>
              <span>Conversion rate</span>
              <strong>
                {flow.total_sessions
                  ? (
                      flow.stage_counts.purchased /
                      flow.total_sessions *
                      100
                    ).toFixed(2)
                  : "0.00"}%
              </strong>
            </div>
          </div>

          <div className="journey-chart">
            <ResponsiveContainer width="100%" height={390}>
              <Sankey
                data={flow}
                dataKey="value"
                nameKey="name"
                nodePadding={30}
                nodeWidth={15}
                margin={{
                  top: 15,
                  right: 135,
                  bottom: 15,
                  left: 15
                }}
                link={{
                  stroke: "#9587ed",
                  strokeOpacity: 0.32
                }}
                node={{
                  stroke: "#ffffff",
                  strokeWidth: 2,
                  fill: "#7866f6"
                }}
              >
                <Tooltip />
              </Sankey>
            </ResponsiveContainer>
          </div>

          <div className="journey-stage-grid">
            {stages.map(([label, key], index) => (
              <div className="journey-stage" key={key}>
                <span>0{index + 1}</span>
                <strong>
                  {flow.stage_counts[key].toLocaleString("en-IN")}
                </strong>
                <small>{label}</small>
              </div>
            ))}
          </div>
        </>
      )}
    </section>
  );
}

export default JourneyFlow;
