import React, { useEffect, useState } from "react";

function App() {
  const [caretakers, setCaretakers] = useState([]);
  const [conversations, setConversations] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/people")
      .then((res) => res.json())
      .then((data) => setCaretakers(data));

    fetch("http://127.0.0.1:5000/conversations")
      .then((res) => res.json())
      .then((data) => setConversations(data));
  }, []);

  const handleCardClick = (item, type) => {
    console.log("Clicked:", type, item);
  };

  const baseCardStyle = {
    width: "100%",
    border: "1px solid #d0d0d0",
    borderRadius: "10px",
    marginBottom: "16px",
    backgroundColor: "#ffffff",
    cursor: "pointer",
    boxShadow: "0 2px 6px rgba(0,0,0,0.08)",
    overflow: "hidden", // so banner stays inside card
  };

  const labelStyle = {
    fontSize: "1rem",
    color: "#555",
    marginBottom: "6px",
  };

  const valueStyle = {
    fontSize: "2.5rem",
    fontWeight: "600",
    color: "#002b5b",
  };

  const nameStyle = {
    fontSize: "2.8rem",
    fontWeight: "700",
    color: "#111",
  };

  return (
    <div
      style={{
        padding: "20px",
        backgroundColor: "#f5f7fa",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div style={{ width: "100%", maxWidth: "1200px" }}>
        {/* Empty rectangle at the top */}
        <div
          style={{
            width: "33%",
            height: "70px",
            margin: "0 auto 25px auto",
            border: "2px dashed #999",
            borderRadius: "8px",
            backgroundColor: "#fafafa",
          }}
        ></div>

        {/* Caretakers Section */}
        <h2 style={{ color: "#002b5b", marginBottom: "16px" }}>Caretakers</h2>
        {caretakers.map((c, i) => {
  const hasAlerts = c.alerts >= 1; // show warning for ANY alerts
  return (
    <div
      key={i}
      onClick={() => handleCardClick(c, "caretaker")}
      style={{
        ...baseCardStyle,
        minHeight: hasAlerts ? "200px" : "160px", // taller if warning is shown
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Warning banner if there are alerts */}
      {hasAlerts && (
        <div
          style={{
            backgroundColor: "#fff4cc",
            color: "#b38600",
            padding: "8px 12px",
            fontSize: "1.2rem",
            fontWeight: "600",
            display: "flex",
            alignItems: "center",
            gap: "8px",
            borderBottom: "1px solid #e6c200",
          }}
        >
          ⚠️ Warning: {c.alerts} alert{c.alerts > 1 ? "s" : ""} for this caretaker
        </div>
      )}

      {/* Main content row */}
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
          <div style={labelStyle}>Tone</div>
          <div style={valueStyle}>{c.tone}</div>
        </div>
        <div style={{ textAlign: "center", flex: "1" }}>
          <div style={labelStyle}>Alerts</div>
          <div style={valueStyle}>{c.alerts}</div>
        </div>
      </div>
    </div>
  );
})}

    

        {/* Conversations Section */}
        <h2 style={{ color: "#002b5b", margin: "28px 0 16px" }}>Conversations</h2>
        {conversations.map((conv, i) => (
          <div
            key={i}
            onClick={() => handleCardClick(conv, "conversation")}
            style={{
              ...baseCardStyle,
              minHeight: "180px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              padding: "20px 32px",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div style={{ textAlign: "center", flex: "1" }}>
                <div style={labelStyle}>Time</div>
                <div style={valueStyle}>{conv.time}</div>
              </div>
              <div style={{ textAlign: "center", flex: "1" }}>
                <div style={labelStyle}>Flags</div>
                <div style={valueStyle}>{conv.flags.join(", ") || "None"}</div>
              </div>
              <div style={{ textAlign: "center", flex: "1" }}>
                <div style={labelStyle}>Sentiment</div>
                <div style={valueStyle}>{conv.sentiment}</div>
              </div>
            </div>

            {/* Summary at the bottom */}
            <div style={{ marginTop: "16px" }}>
              <div style={labelStyle}>Summary</div>
              <div style={{ fontSize: "1.6rem", color: "#333" }}>{conv.summary}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
