import './App.css';
import { handleButtonClick, handleSliderChange, handleColorChange } from './http_handler';

function App() {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Candlestick Controller v2</h1>
      <div>
        <button
          onClick={() =>
            handleButtonClick({
              program: "rb",
            })
          }
          style={buttonStyle}
        >
          Rainbow 1
        </button>
        <button
          onClick={() =>
            handleButtonClick({
              program: "rb2",
            })
          }
          style={buttonStyle}
        >
          Rainbow 2
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
          Waterfall
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
        {/* Reset Button */}
        <div style={{ marginTop: "20px" }}>
          <button
            onClick={() =>
              handleButtonClick({
                program: "random",
                speed: "15"
              })
            }
            style={resetButtonStyle}
          >
            Reset
          </button>
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
