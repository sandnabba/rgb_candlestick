// ConnectionStatus component - displays candlestick connection status as a header/toolbar

import { useState, useEffect } from "react";
import { Candlestick, listCandlesticks, setCurrentCandlestickId, getCurrentCandlestickId } from "./http_handler";

export const ConnectionStatus = () => {
  const [candlesticks, setCandlesticks] = useState<Candlestick[]>([]);
  const [selectedId, setSelectedId] = useState<string>(getCurrentCandlestickId());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch candlesticks on mount and periodically
  useEffect(() => {
    const fetchCandlesticks = async () => {
      try {
        const sticks = await listCandlesticks();
        setCandlesticks(sticks);
        setError(null);
        
        // If no selection yet and we have candlesticks, select the first connected one
        if (!selectedId && sticks.length > 0) {
          const firstConnected = sticks.find(c => c.connected);
          const newId = firstConnected?.id || sticks[0].id;
          setSelectedId(newId);
          setCurrentCandlestickId(newId);
        }
      } catch (err) {
        setError("Failed to connect to backend");
        console.error("Error fetching candlesticks:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCandlesticks();
    const interval = setInterval(fetchCandlesticks, 3000); // Refresh every 3 seconds

    return () => clearInterval(interval);
  }, []);

  const selectedCandlestick = candlesticks.find(c => c.id === selectedId);

  // Format last update time
  const formatLastUpdate = (lastSeen?: string) => {
    if (!lastSeen) return "Never";
    const date = new Date(lastSeen);
    return date.toLocaleTimeString();
  };

  if (loading) {
    return (
      <div style={headerContainerStyle}>
        <span style={loadingStyle}>🔄 Connecting...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ ...headerContainerStyle, ...errorHeaderStyle }}>
        <span style={errorStyle}>● Disconnected</span>
      </div>
    );
  }

  if (candlesticks.length === 0 || !selectedCandlestick?.connected) {
    return (
      <div style={{ ...headerContainerStyle, ...warningHeaderStyle }}>
        <span style={errorStyle}>● Disconnected</span>
      </div>
    );
  }

  // Connected state - show name and last update
  return (
    <div style={connectedHeaderStyle}>
      <div style={contentStyle}>
        <span style={connectedDotStyle}>●</span>
        <span style={nameStyle}>{selectedCandlestick.id}</span>
        <span style={separatorStyle}>•</span>
        <span style={lastUpdateStyle}>
          {formatLastUpdate(selectedCandlestick.last_seen)}
        </span>
      </div>
    </div>
  );
};

// Styles - Small badge in top right corner
const headerContainerStyle: React.CSSProperties = {
  position: "fixed",
  top: "10px",
  right: "10px",
  backgroundColor: "#f5f5f5",
  border: "1px solid #ddd",
  borderRadius: "6px",
  padding: "6px 12px",
  display: "flex",
  alignItems: "center",
  gap: "6px",
  fontSize: "12px",
  boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  zIndex: 1000,
};

const connectedHeaderStyle: React.CSSProperties = {
  position: "fixed",
  top: "10px",
  right: "10px",
  backgroundColor: "#e8f5e9",
  border: "1px solid #4CAF50",
  borderRadius: "6px",
  padding: "6px 12px",
  display: "flex",
  alignItems: "center",
  fontSize: "12px",
  boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  zIndex: 1000,
};

const errorHeaderStyle: React.CSSProperties = {
  backgroundColor: "#ffebee",
  border: "1px solid #f44336",
};

const warningHeaderStyle: React.CSSProperties = {
  backgroundColor: "#ffebee",
  border: "1px solid #f44336",
};

const contentStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: "6px",
};

const connectedDotStyle: React.CSSProperties = {
  color: "#4CAF50",
  fontSize: "10px",
};

const nameStyle: React.CSSProperties = {
  fontSize: "12px",
  fontWeight: "600",
  color: "#333",
};

const separatorStyle: React.CSSProperties = {
  color: "#999",
  fontSize: "10px",
};

const lastUpdateStyle: React.CSSProperties = {
  fontSize: "11px",
  color: "#666",
};

const loadingStyle: React.CSSProperties = {
  fontSize: "12px",
  color: "#666",
};

const errorStyle: React.CSSProperties = {
  fontSize: "12px",
  color: "#d32f2f",
  fontWeight: "600",
};
