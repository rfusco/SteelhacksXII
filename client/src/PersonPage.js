// PersonPage.js
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
function sentimentLabel(score) {
  if (score <= -0.6) return "Terrible";
  if (score <= -0.2) return "Bad";
  if (score < 0.2) return "Fair";
  if (score < 0.6) return "Good";
  return "Excellent";
}

function PersonPage() {
  const { personName } = useParams();
  const [personData, setPersonData] = useState(null);
  const [conversations, setConversations] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchPerson() {
      try {
        const res = await fetch(`http://127.0.0.1:5000/person/${personName}`);
        const data = await res.json();
        if (data.error) {
          setPersonData({ error: data.error });
          return;
        }

        const person = data.person || data;
        const flagsRes = await fetch(`http://127.0.0.1:5000/flags/${person.name}`);
        const flagsJson = await flagsRes.json();

        setPersonData({
          name: person.name,
          conversations: person.conversations ? person.conversations.length : 0,
          role: person.role || "Unknown",
          alerts: flagsJson.total_flags || 0,
        });

        const convRes = await fetch(`http://127.0.0.1:5000/conversations/${person.name}`);
        const convData = await convRes.json();
        setConversations(convData);
      } catch {
        setPersonData({ error: "Failed to fetch caretaker details" });
      }
    }
    if (personName) fetchPerson();
  }, [personName]);

  const pageStyle = {
    padding: "20px",
    background: "linear-gradient(to right, #f4ede4, #e5d4b3)",
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    fontFamily: "'Inter', sans-serif",
  };

  const containerStyle = { width: "100%", maxWidth: "1200px" };

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
  };

  const labelStyle = { fontSize: "0.9rem", color: "#7c6f64", marginBottom: "6px", fontWeight: "500" };
  const valueStyle = { fontSize: "2.4rem", fontWeight: "800", color: "#3f2e1f" };
  const nameStyle = { fontSize: "2.6rem", fontWeight: "800", color: "#a16207" };

  if (!personData) return <div style={{ padding: "20px" }}>Loading...</div>;
  if (personData.error) return <div style={{ padding: "20px", color: "red" }}>{personData.error}</div>;

  return (
    <div style={pageStyle}>
      <div style={containerStyle}>
        <h2 style={sectionTitle}>Care Partner Detail</h2>
        <div
          style={{
            ...baseCardStyle,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "stretch",
            padding: "20px 0",
          }}
        >
          <div style={{ flex: "1", textAlign: "center" }}>
            <div style={labelStyle}>Name</div>
            <div style={valueStyle}>{personData.name}</div>
          </div>
          <div style={{ flex: "1", textAlign: "center" }}>
            <div style={labelStyle}>Conversations</div>
            <div style={valueStyle}>{personData.conversations}</div>
          </div>
          <div style={{ flex: "1", textAlign: "center" }}>
            <div style={labelStyle}>Role</div>
            <div style={valueStyle}>{personData.role}</div>
          </div>
          <div style={{ flex: "1", textAlign: "center" }}>
            <div style={labelStyle}>Alerts</div>
            <div style={valueStyle}>{personData.alerts}</div>
          </div>
        </div>

        <h2 style={sectionTitle}>Conversations</h2>
        {conversations.map((conv, i) => {
          const hasFlags = conv.flags && conv.flags.length > 0;
          return (
            <div
              key={i}
              style={{
                ...baseCardStyle,
                display: "flex",
                flexDirection: "column",
                cursor: "pointer",
              }}
              onClick={() => navigate(`/conversation/${conv._id}`)}
            >
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
              <div
                style={{
                  flex: "1",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "20px 32px",
                }}
              >
                <div style={{ flex: "1", ...nameStyle }}>{new Date(conv.start_time).toLocaleString()}</div>
                <div style={{ textAlign: "center", flex: "1" }}>
                  <div style={labelStyle}>Flags</div>
                  <div style={valueStyle}>{conv.flags ? conv.flags.length : 0}</div>
                </div>
                  <div style={{ textAlign: "center", flex: "1" }}>
                    <div style={labelStyle}>Sentiment</div>
                    <div style={valueStyle}>
                      {conv.sentiment != null
                        ? `${conv.sentiment.toFixed(2)} (${sentimentLabel(conv.sentiment)})`
                        : "Unknown"}
                    </div>
                  </div>
              </div>
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

export default PersonPage;
