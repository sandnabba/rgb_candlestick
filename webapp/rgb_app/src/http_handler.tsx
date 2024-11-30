// This file handles the HTTP calls made to the candlestick API.
// These calls could probably be merged in some way, but whatever...

import { ChangeEvent } from "react";

export const handleButtonClick = async (data) => {
  try {
    const response = await fetch("/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    
    if (response.ok) {
      console.log("Success!");
    } else {
      console.error("Error:", response.statusText);
      alert("POST request failed!");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred!");
  }
};

export const handleSliderChange = async (event: ChangeEvent<HTMLInputElement>): Promise<void> => {
  const inputElement = event.target as HTMLInputElement;
  const sliderValue = inputElement.value;
  console.log("Slider value:", sliderValue);

  // Update the text content of the span element with the slider value
  const sliderValueElement = document.getElementById("sliderValue");
  if (sliderValueElement) {
    sliderValueElement.textContent = sliderValue;
  }

  try {
    const response = await fetch("/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ speed: sliderValue }),
    });

    if (response.ok) {
      console.log("Slider value sent successfully!");
    } else {
      console.error("Error:", response.statusText);
      alert("POST request failed!");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred!");
  }
};

export const handleColorChange = async (event: ChangeEvent<HTMLInputElement>): Promise<void> => {
  const inputElement = event.target as HTMLInputElement;
  const colorValue = inputElement.value;
  console.log("Selected color:", colorValue);

  const colorValueElement = document.getElementById("colorValue");
  if (colorValueElement) {
    colorValueElement.textContent = colorValue;
  }

  try {
    const response = await fetch("/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ color: colorValue }),
    });

    if (response.ok) {
      console.log("Color sent successfully!");
    } else {
      console.error("Error:", response.statusText);
      alert("POST request failed!");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred!");
  }
};
