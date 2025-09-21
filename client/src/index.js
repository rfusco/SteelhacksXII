import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import PersonPage from "./PersonPage";
import ConversationPage from "./ConversationPage"; // ✅ new
import { BrowserRouter, Routes, Route } from "react-router-dom";
import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/person/:personName" element={<PersonPage />} />
        <Route path="/conversation/:convId" element={<ConversationPage />} /> {/* ✅ new */}
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

reportWebVitals();
