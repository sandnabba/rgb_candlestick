import './App.css';
import { handleButtonClick, handleSliderChange, handleColorChange } from './http_handler';

function App() {
  return (
    <div style={{ textAlign: "center", marginTop: "25px" }}>
      <h1>Sandnabba Candlestick Controller - v2024</h1>
      <div>
        <button
          onClick={() =>
            handleButtonClick({
              program: "rb",
            })
          }
          style={buttonStyle}
        >
          Rainbow
        </button>
        <button
          onClick={() =>
            handleButtonClick({
              program: "bounce",
            })
          }
          style={buttonStyle}
        >
          Bounce
        </button>
        <button
          onClick={() =>
            handleButtonClick({
              program: "fall",
            })
          }
          style={buttonStyle}
        >
          Falling
        </button>
        <button
          onClick={() =>
            handleButtonClick({
              program: "cop",
            })
          }
          style={buttonStyle}
        >
          Police
        </button>
        <button
          onClick={() =>
            handleButtonClick({
              program: "wave",
            })
          }
          style={buttonStyle}
        >
          Wave
        </button>
        {/* Slider */}
        <div style={{ marginTop: "30px" }}>
          <input
            type="range"
            min="3"
            max="40"
            defaultValue="20"
            onChange={handleSliderChange}
            style={{ width: "300px" }}
          />
          <p>
            Speed: <span id="sliderValue">15</span>
          </p>
        </div>
        {/* Color Picker */}
        <div style={{ marginTop: "30px" }}>
          <input
            type="color"
            id="colorPicker"
            name="color"
            defaultValue="#ff0000"
            onChange={handleColorChange}
          />
          <p>
            Selected Color: <span id="colorValue">#ff0000</span>
          </p>
        </div>
        <button
          onClick={() =>
            handleButtonClick({
              direction: "up",
            })
          }
          style={buttonStyle}
        >
          Up
        </button>
        <button
          onClick={() =>
            handleButtonClick({
              direction: "left",
            })
          }
          style={buttonStyle}
        >
          Left
        </button>
        <button
          onClick={() =>
            handleButtonClick({
              direction: "right",
            })
          }
          style={buttonStyle}
        >
          Right
        </button>
        <button
          onClick={() =>
            handleButtonClick({
              direction: "down",
            })
          }
          style={buttonStyle}
        >
          Down
        </button>
        {/* Reset Button */}
        <div style={{ marginTop: "20px" }}>
          <button
            onClick={() =>
              handleButtonClick({
                program: "random",
                speed: "10"
              })
            }
            style={resetButtonStyle}
          >
            Reset
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
  );
}

const buttonStyle = {
  padding: "10px 20px",
  margin: "10px",
  fontSize: "16px",
  cursor: "pointer",
};

const resetButtonStyle = {
  padding: "15px 30px",
  margin: "20px",
  fontSize: "18px",
  cursor: "pointer",
};

export default App;
