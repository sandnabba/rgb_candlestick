import './App.css';
import { useState } from 'react';
import { handleButtonClick, handleSliderChange, handleColorChange } from './http_handler';
import { ConnectionStatus } from './ConnectionStatus';
import { useCandlestick } from './CandlestickContext';

function App() {
  const { selectedCandlestick: candlestickState } = useCandlestick();
  const [showDebug, setShowDebug] = useState(false);

  // Helper function to check if a program is active
  const isActiveProgram = (program: string) => {
    // Don't show active state if disconnected
    if (!candlestickState?.connected) return false;
    return candlestickState?.program === program;
  };

  // Helper function to check if a direction is active
  const isActiveDirection = (direction: string) => {
    // Don't show active state if disconnected
    if (!candlestickState?.connected) return false;
    return candlestickState?.direction === direction;
  };

  // Check if controls should be disabled
  const isDisconnected = !candlestickState?.connected;

  // Toggle debug modal
  const toggleDebug = () => {
    setShowDebug(!showDebug);
  };

  return (
    <div>
      {/* Connection Status Header */}
      <ConnectionStatus onStatusClick={toggleDebug} />
      
      {/* Debug Modal */}
      {showDebug && candlestickState && (
        <div style={debugOverlayStyle} onClick={toggleDebug}>
          <div style={debugModalStyle} onClick={(e) => e.stopPropagation()}>
            <h3 style={{ marginTop: 0, color: "#333" }}>Debug Information</h3>
            <div style={{ textAlign: "left" }}>
              <div style={debugItemStyle}>
                <strong>Candlestick ID:</strong> {candlestickState.id}
              </div>
              <div style={debugItemStyle}>
                <strong>Connected:</strong> {candlestickState.connected ? "✅ Yes" : "❌ No"}
              </div>
              <div style={debugItemStyle}>
                <strong>Program:</strong> {candlestickState.program || "None"}
                {candlestickState.random && <span style={{ marginLeft: "8px", color: "#ff9800", fontWeight: "bold" }}>🎲 Random Mode</span>}
              </div>
              <div style={debugItemStyle}>
                <strong>Speed:</strong> {candlestickState.speed !== null ? candlestickState.speed : "Not set"}
              </div>
              <div style={debugItemStyle}>
                <strong>Direction:</strong> {candlestickState.direction || "None"}
              </div>
              <div style={debugItemStyle}>
                <strong>Color:</strong> 
                {candlestickState.color ? (
                  <>
                    <span style={{ 
                      display: "inline-block", 
                      width: "20px", 
                      height: "20px", 
                      backgroundColor: candlestickState.color,
                      border: "1px solid #ccc",
                      marginLeft: "8px",
                      verticalAlign: "middle",
                      borderRadius: "3px"
                    }}></span>
                    <span style={{ marginLeft: "5px" }}>{candlestickState.color}</span>
                  </>
                ) : "None"}
              </div>
              <div style={debugItemStyle}>
                <strong>Last Seen:</strong> {new Date(candlestickState.last_seen).toLocaleString()}
              </div>
            </div>
            <button onClick={toggleDebug} style={debugCloseButtonStyle}>
              Close
            </button>
          </div>
        </div>
      )}
      
      <div style={{ textAlign: "center", marginTop: "25px" }}>
        <h1>Sandnabba Candlestick Controller - v2025</h1>
        
        {/* Disconnected Overlay */}
        {candlestickState && !candlestickState.connected && (
          <div style={disconnectedBannerStyle}>
            ⚠️ Candlestick Disconnected - Waiting for connection...
          </div>
        )}
        
        <div>
        {/* Program Buttons */}
        <div style={{ marginBottom: "20px" }}>
          <h3 style={{ color: "#555" }}>
            Programs
            {isActiveProgram("static_color") && (
              <span style={{ marginLeft: "10px", fontSize: "14px", color: "#9c27b0", fontWeight: "normal" }}>
                🎨 Static Color Mode
              </span>
            )}
          </h3>
          <button
            onClick={() =>
              handleButtonClick({
                program: "rb",
              })
            }
            style={isActiveProgram("rb") ? activeButtonStyle : buttonStyle}
            className={isActiveProgram("rb") ? "active-btn" : ""}
            disabled={isDisconnected}
          >
            🌈 Rainbow
          </button>
          <button
            onClick={() =>
              handleButtonClick({
                program: "bounce",
              })
            }
            style={isActiveProgram("bounce") ? activeButtonStyle : buttonStyle}
            className={isActiveProgram("bounce") ? "active-btn" : ""}
          >
            ⚡ Bounce
          </button>
          <button
            onClick={() =>
              handleButtonClick({
                program: "fall",
              })
            }
            style={isActiveProgram("fall") ? activeButtonStyle : buttonStyle}
            className={isActiveProgram("fall") ? "active-btn" : ""}
          >
            ⬇️ Falling
          </button>
          <button
            onClick={() =>
              handleButtonClick({
                program: "cop",
              })
            }
            style={isActiveProgram("cop") ? activeButtonStyle : buttonStyle}
            className={isActiveProgram("cop") ? "active-btn" : ""}
          >
            🚔 Police
          </button>
          <button
            onClick={() =>
              handleButtonClick({
                program: "wave",
              })
            }
            style={isActiveProgram("wave") ? activeButtonStyle : buttonStyle}
            className={isActiveProgram("wave") ? "active-btn" : ""}
          >
            🌊 Wave
          </button>
        </div>
        {/* Slider */}
        <div style={{ marginTop: "30px" }}>
          <h3 style={{ color: "#555" }}>Speed</h3>
          <input
            type="range"
            min="3"
            max="40"
            value={candlestickState?.speed || 20}
            onChange={handleSliderChange}
            style={{ width: "300px" }}
          />
          <p>
            Speed: <span id="sliderValue">{candlestickState?.speed || 15}</span>
          </p>
        </div>

        {/* Color Picker */}
        <div style={{ marginTop: "30px" }}>
          <h3 style={{ color: "#555" }}>Static Color</h3>
          <input
            type="color"
            id="colorPicker"
            name="color"
            value={candlestickState?.color || "#ff0000"}
            onChange={handleColorChange}
          />
          <p>
            Selected Color: <span id="colorValue">{candlestickState?.color || "#ff0000"}</span>
          </p>
        </div>

        {/* Direction Buttons */}
        <div style={{ marginTop: "30px" }}>
          <h3 style={{ color: "#555" }}>Direction</h3>
          <button
            onClick={() =>
              handleButtonClick({
                direction: "up",
              })
            }
            style={isActiveDirection("up") ? activeButtonStyle : buttonStyle}
          >
            ⬆️ Up
          </button>
          <button
            onClick={() =>
              handleButtonClick({
                direction: "left",
              })
            }
            style={isActiveDirection("left") ? activeButtonStyle : buttonStyle}
          >
            ⬅️ Left
          </button>
          <button
            onClick={() =>
              handleButtonClick({
                direction: "right",
              })
            }
            style={isActiveDirection("right") ? activeButtonStyle : buttonStyle}
          >
            ➡️ Right
          </button>
          <button
            onClick={() =>
              handleButtonClick({
                direction: "down",
              })
            }
            style={isActiveDirection("down") ? activeButtonStyle : buttonStyle}
          >
            ⬇️ Down
          </button>
        </div>
        {/* Reset / Random Button */}
        <div style={{ marginTop: "20px" }}>
          <button
            onClick={() =>
              handleButtonClick({
                program: "random",
                speed: 10
              })
            }
            style={candlestickState?.random ? activeResetButtonStyle : resetButtonStyle}
            className={candlestickState?.random ? "active-btn" : ""}
          >
            🎲 Reset / Random
          </button>
        </div>
        {/* Info Paragraph */}
        <div style={{ marginTop: "50px" }}>
          <p style={{ fontSize: "18px", color: "#666" }}>
            For documentation, build instruction and more information, please see:<br />
            <a href='https://github.com/sandnabba/rgb_candlestick'>https://github.com/sandnabba/rgb_candlestick</a>
          </p>
        </div>
        </div>
      </div>
    </div>
  );
}

const buttonStyle: React.CSSProperties = {
  padding: "10px 20px",
  margin: "10px",
  fontSize: "16px",
  cursor: "pointer",
  backgroundColor: "#f0f0f0",
  border: "2px solid #ccc",
  borderRadius: "8px",
  transition: "all 0.3s ease",
  fontWeight: "500",
};

const activeButtonStyle: React.CSSProperties = {
  ...buttonStyle,
  backgroundColor: "#4CAF50",
  color: "white",
  border: "2px solid #45a049",
  boxShadow: "0 0 15px rgba(76, 175, 80, 0.5), 0 0 30px rgba(76, 175, 80, 0.3)",
  transform: "scale(1.05)",
  fontWeight: "bold",
};

const resetButtonStyle: React.CSSProperties = {
  padding: "15px 30px",
  margin: "20px",
  fontSize: "18px",
  cursor: "pointer",
  backgroundColor: "#ff9800",
  color: "white",
  border: "2px solid #f57c00",
  borderRadius: "8px",
  fontWeight: "bold",
};

const activeResetButtonStyle: React.CSSProperties = {
  ...resetButtonStyle,
  backgroundColor: "#4CAF50",
  border: "2px solid #45a049",
  boxShadow: "0 0 15px rgba(76, 175, 80, 0.5), 0 0 30px rgba(76, 175, 80, 0.3)",
  transform: "scale(1.05)",
};

const debugOverlayStyle: React.CSSProperties = {
  position: "fixed",
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: "rgba(0, 0, 0, 0.5)",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  zIndex: 2000,
};

const debugModalStyle: React.CSSProperties = {
  backgroundColor: "white",
  padding: "30px",
  borderRadius: "12px",
  maxWidth: "500px",
  width: "90%",
  boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
};

const debugItemStyle: React.CSSProperties = {
  padding: "10px",
  marginBottom: "8px",
  backgroundColor: "#f5f5f5",
  borderRadius: "5px",
  fontSize: "14px",
};

const debugCloseButtonStyle: React.CSSProperties = {
  marginTop: "20px",
  padding: "10px 20px",
  backgroundColor: "#2196F3",
  color: "white",
  border: "none",
  borderRadius: "5px",
  cursor: "pointer",
  fontSize: "14px",
  fontWeight: "bold",
};

const disconnectedBannerStyle: React.CSSProperties = {
  backgroundColor: "#ffebee",
  border: "2px solid #f44336",
  borderRadius: "8px",
  padding: "15px",
  margin: "20px auto",
  maxWidth: "600px",
  color: "#c62828",
  fontSize: "16px",
  fontWeight: "bold",
  boxShadow: "0 2px 8px rgba(244, 67, 54, 0.2)",
};

export default App;
