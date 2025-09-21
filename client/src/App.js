// App.js
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// Main dashboard component
function App() {
  // State for different dashboard sections
  const [caretakers, setCaretakers] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [summary, setSummary] = useState({ flags: 0, convos: 0, sentiment: "XX" });

  useEffect(() => {
    // --- Fetch caretakers from backend ---
    fetch("http://127.0.0.1:5000/people")
      .then((res) => res.json())
      .then(async (data) => {
        // For each caretaker, fetch their flag count in parallel
        const caretakersParsed = await Promise.all(
          data.map(async (p) => {
            const flagsRes = await fetch(`http://127.0.0.1:5000/flags/${p.name}`);
            const flagsJson = await flagsRes.json();
            const flags = flagsJson.total_flags || 0;

            return {
              name: p.name,
              conversations: p.conversations.length,
              role: p.role,
              alerts: flags,
            };
          })
        );
        setCaretakers(caretakersParsed);
      });

    // --- Fetch all conversations ---
    fetch("http://127.0.0.1:5000/conversations")
      .then((res) => res.json())
      .then((data) => {
        setConversations(data);

        // Filter only conversations from the last 72h
        const now = new Date();
        const seventyTwoHoursAgo = new Date(now.getTime() - 72 * 60 * 60 * 1000);

        const recentConvos = data.filter((conv) => {
          const startTime = new Date(conv.start_time);
          return startTime >= seventyTwoHoursAgo;
        });

        // Calculate dashboard summary stats
        const totalFlags = recentConvos.reduce(
          (sum, conv) => sum + (conv.flags ? conv.flags.length : 0),
          0
        );

        setSummary({
          flags: totalFlags,
          convos: recentConvos.length,
          sentiment: "XX", // placeholder for now
        });
      });
  }, []);

  const navigate = useNavigate();

  // Handle card clicks → navigate to detail pages
  const handleCardClick = (item, type) => {
    if (type === "caretaker") {
      navigate(`/person/${encodeURIComponent(item.name)}`);
    } else if (type === "conversation") {
      navigate(`/conversation/${encodeURIComponent(item._id)}`);
    }
  };

  // --- Theme + styles ---
  const dashboardStyle = {
    padding: "20px",
    background: "linear-gradient(to right, #f4ede4, #e5d4b3)",
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    fontFamily: "'Inter', sans-serif",
  };

  const containerStyle = { width: "100%", maxWidth: "1200px" };

  const titleStyle = {
    fontFamily: "'Cinzel Decorative', serif",
    fontSize: "3.5rem",
    fontWeight: "700",
    textAlign: "center",
    marginBottom: "30px",
    background: "linear-gradient(to right, #a16207, #3f2e1f)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    letterSpacing: "2px",
  };

  const sectionTitle = {
    color: "#3f2e1f",
    fontSize: "1.6rem",
    margin: "28px 0 16px",
    fontWeight: "700",
    borderBottom: "3px solid #a16207",
    display: "inline-block",
    paddingBottom: "4px",
  };

  const baseCardStyle = {
    width: "100%",
    borderRadius: "14px",
    marginBottom: "20px",
    backgroundColor: "#ffffff",
    boxShadow: "0 4px 14px rgba(0,0,0,0.08)",
    overflow: "hidden",
    transition: "transform 0.15s ease, box-shadow 0.15s ease",
  };

  const labelStyle = { fontSize: "0.9rem", color: "#7c6f64", marginBottom: "6px", fontWeight: "500" };
  const valueStyle = { fontSize: "2.6rem", fontWeight: "800", color: "#3f2e1f" };
  const nameStyle = { fontSize: "2.6rem", fontWeight: "800", color: "#a16207" };

  return (
    <div style={dashboardStyle}>
      <div style={containerStyle}>
        {/* Title */}
        <h1 style={titleStyle}>Elder-Guardian</h1>

        {/* Dashboard summary row */}
        <div
          style={{
            ...baseCardStyle,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "stretch",
            padding: "30px 0",
          }}
        >
          <div style={{ flex: "1", textAlign: "center" }}>
            <div style={labelStyle}>Flags (Last 72h)</div>
            <div style={valueStyle}>{summary.flags}</div>
          </div>
          <div style={{ flex: "1", textAlign: "center" }}>
            <div style={labelStyle}>Conversations (Last 72h)</div>
            <div style={valueStyle}>{summary.convos}</div>
          </div>
          <div style={{ flex: "1", textAlign: "center" }}>
            <div style={labelStyle}>Sentiment (Last 72h)</div>
            <div style={valueStyle}>{summary.sentiment}</div>
          </div>
        </div>

        {/* Caretakers list */}
        <h2 style={sectionTitle}>Caretakers</h2>
        {caretakers.map((c, i) => {
          const hasAlerts = c.alerts >= 1;
          return (
            <div
              key={i}
              onClick={() => handleCardClick(c, "caretaker")}
              style={{
                ...baseCardStyle,
                minHeight: hasAlerts ? "200px" : "160px",
                display: "flex",
                flexDirection: "column",
                cursor: "pointer",
              }}
            >
              {/* Warning banner */}
              {hasAlerts && (
                <div
                  style={{
                    backgroundColor: "#fef3c7",
                    color: "#92400e",
                    padding: "10px 16px",
                    fontSize: "1.1rem",
                    fontWeight: "600",
                    borderBottom: "1px solid #fcd34d",
                  }}
                >
                  ⚠️ {c.alerts} alert{c.alerts > 1 ? "s" : ""} for this caretaker
                </div>
              )}
              {/* Caretaker info row */}
              <div
                style={{
                  flex: "1",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "20px 32px",
                }}
              >
                <div style={{ flex: "1", ...nameStyle }}>{c.name}</div>
                <div style={{ textAlign: "center", flex: "1" }}>
                  <div style={labelStyle}>Conversations</div>
                  <div style={valueStyle}>{c.conversations}</div>
                </div>
                <div style={{ textAlign: "center", flex: "1" }}>
                  <div style={labelStyle}>Role</div>
                  <div style={valueStyle}>{c.role}</div>
                </div>
                <div style={{ textAlign: "center", flex: "1" }}>
                  <div style={labelStyle}>Alerts</div>
                  <div style={valueStyle}>{c.alerts}</div>
                </div>
              </div>
            </div>
          );
        })}

        {/* Conversations list */}
        <h2 style={sectionTitle}>Conversations</h2>
        {conversations.map((conv, i) => {
          const hasFlags = conv.flags && conv.flags.length > 0;
          return (
            <div
              key={i}
              onClick={() => handleCardClick(conv, "conversation")}
              style={{
                ...baseCardStyle,
                minHeight: hasFlags ? "200px" : "160px",
                display: "flex",
                flexDirection: "column",
                cursor: "pointer",
              }}
            >
              {/* Warning banner */}
              {hasFlags && (
                <div
                  style={{
                    backgroundColor: "#fef3c7",
                    color: "#92400e",
                    padding: "10px 16px",
                    fontSize: "1.1rem",
                    fontWeight: "600",
                    borderBottom: "1px solid #fcd34d",
                  }}
                >
                  ⚠️ {conv.flags.length} flag{conv.flags.length > 1 ? "s" : ""} in this conversation
                </div>
              )}
              {/* Conversation info row */}
              <div
                style={{
                  flex: "1",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "20px 32px",
                }}
              >
                <div style={{ flex: "1", ...nameStyle }}>
                  {new Date(conv.start_time).toLocaleString()}
                </div>
                <div style={{ textAlign: "center", flex: "1" }}>
                  <div style={labelStyle}>Flags</div>
                  <div style={valueStyle}>{conv.flags ? conv.flags.length : 0}</div>
                </div>
                <div style={{ textAlign: "center", flex: "1" }}>
                  <div style={labelStyle}>Sentiment</div>
                  <div style={valueStyle}>{conv.sentiment || "Unknown"}</div>
                </div>
              </div>
              {/* Summary section */}
              <div
                style={{
                  borderTop: "1px solid #f1f5f9",
                  padding: "14px 20px",
                  fontSize: "1.2rem",
                  color: "#5c5045",
                  backgroundColor: "#faf8f5",
                }}
              >
                <strong style={{ color: "#5c5045", marginRight: "8px" }}>Summary:</strong>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default App;
