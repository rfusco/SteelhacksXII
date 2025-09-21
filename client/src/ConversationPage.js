// ConversationPage.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
function sentimentLabel(score) {
  if (score <= -0.6) return "Terrible";
  if (score <= -0.2) return "Bad";
  if (score < 0.2) return "Fair";
  if (score < 0.6) return "Good";
  return "Excellent";
}
function ConversationPage() {
  const { convId } = useParams();
  const [conversation, setConversation] = useState(null);

  useEffect(() => {
    async function fetchConversation() {
      try {
        const res = await fetch(`http://127.0.0.1:5000/conversation/${convId}`);
        const data = await res.json();
        setConversation(data);
      } catch {
        setConversation({ error: "Failed to fetch conversation" });
      }
    }
    if (convId) fetchConversation();
  }, [convId]);

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
    fontSize: "1.8rem",
    margin: "20px 0 16px",
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
    display: "flex",
    flexDirection: "column",
  };

  const labelStyle = { fontSize: "0.9rem", color: "#7c6f64", marginBottom: "6px", fontWeight: "500" };
  const valueStyle = { fontSize: "2.4rem", fontWeight: "800", color: "#3f2e1f" };
  const nameStyle = { fontSize: "2rem", fontWeight: "700", color: "#a16207" };

  if (!conversation) return <div style={{ padding: "20px" }}>Loading...</div>;
  if (conversation.error) return <div style={{ padding: "20px", color: "red" }}>{conversation.error}</div>;

  const hasFlags = conversation.flags && conversation.flags.length > 0;

  // Extract flagged sentences
  let flaggedSentences = [];
  if (hasFlags && conversation.sentences) {
    flaggedSentences = conversation.flags
      .map((f) => conversation.sentences[parseInt(f, 10)])
      .filter(Boolean);
  }

  return (
    <div style={pageStyle}>
      <div style={containerStyle}>
        <h2 style={sectionTitle}>Conversation Detail</h2>

        {/* Conversation Card */}
        <div style={baseCardStyle}>
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
              ⚠️ {conversation.flags.length} flag{conversation.flags.length > 1 ? "s" : ""} in this conversation
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
            <div style={{ flex: "1", ...nameStyle }}>
              {new Date(conversation.start_time).toLocaleString()}
            </div>
            <div style={{ textAlign: "center", flex: "1" }}>
              <div style={labelStyle}>Flags</div>
              <div style={valueStyle}>{conversation.flags ? conversation.flags.length : 0}</div>
            </div>
              <div style={{ textAlign: "center", flex: "1" }}>
                <div style={labelStyle}>Sentiment</div>
                <div style={valueStyle}>
                  {conversation.sentiment != null
                    ? `${conversation.sentiment.toFixed(2)} (${sentimentLabel(conversation.sentiment)})`
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

        {/* Flagged Dialogue */}
        {flaggedSentences.length > 0 && (
          <div
            style={{
              marginTop: "32px",
              padding: "20px",
              backgroundColor: "#ffffff",
              borderRadius: "12px",
              boxShadow: "0 4px 10px rgba(0,0,0,0.08)",
              textAlign: "center",
            }}
          >
            <h3 style={{ color: "#a16207", marginBottom: "16px" }}>🚩 Flagged Dialogue</h3>
            {flaggedSentences.map((s, i) => (
              <div
                key={i}
                style={{
                  fontSize: "1.4rem",
                  fontWeight: "500",
                  marginBottom: "12px",
                  color: "#3f2e1f",
                }}
              >
                {s.text || "(no text available)"}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ConversationPage;
