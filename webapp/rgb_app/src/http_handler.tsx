// This file handles the HTTP calls made to the candlestick backend API.
// Updated to use the new WebSocket backend architecture.

import { ChangeEvent } from "react";

// Backend configuration
// In production, this should be set via environment variables
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";
const DEFAULT_CANDLESTICK_ID = import.meta.env.VITE_CANDLESTICK_ID || "candlestick_001";

// TypeScript interfaces
export interface Candlestick {
  id: string;
  connected: boolean;
  program: string | null;
  speed: number | null;
  direction: string | null;
  color: string | null;
  last_seen: string;
}

export interface CandlestickCommand {
  program?: string;
  speed?: number;
  direction?: string;
  color?: string;
}

// Storage for current candlestick ID
let currentCandlestickId = DEFAULT_CANDLESTICK_ID;

export const setCurrentCandlestickId = (id: string) => {
  currentCandlestickId = id;
};

export const getCurrentCandlestickId = (): string => {
  return currentCandlestickId;
};

// Get list of all candlesticks
export const listCandlesticks = async (): Promise<Candlestick[]> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/candlesticks`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch candlesticks: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data.candlesticks;
  } catch (error) {
    console.error("Error fetching candlesticks:", error);
    throw error;
  }
};

// Get specific candlestick status
export const getCandlestick = async (id: string): Promise<Candlestick> => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/candlesticks/${id}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("Candlestick not found");
      }
      throw new Error(`Failed to fetch candlestick: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Error fetching candlestick ${id}:`, error);
    throw error;
  }
};

// Send command to candlestick
export const sendCommand = async (
  candlestickId: string,
  command: CandlestickCommand
): Promise<void> => {
  try {
    const response = await fetch(
      `${BACKEND_URL}/api/candlesticks/${candlestickId}/command`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(command),
      }
    );
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("Candlestick not connected");
      }
      throw new Error(`Failed to send command: ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log("Command sent successfully:", data.message);
  } catch (error) {
    console.error("Error sending command:", error);
    throw error;
  }
};

// Legacy handler for button clicks - updated to use new backend
export const handleButtonClick = async (data: CandlestickCommand) => {
  try {
    await sendCommand(currentCandlestickId, data);
    console.log("Success!");
  } catch (error) {
    console.error("Error:", error);
    alert(`Failed to send command: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
};

// Handler for slider changes
export const handleSliderChange = async (event: ChangeEvent<HTMLInputElement>): Promise<void> => {
  const inputElement = event.target as HTMLInputElement;
  const sliderValue = parseInt(inputElement.value);
  console.log("Slider value:", sliderValue);

  // Update the text content of the span element with the slider value
  const sliderValueElement = document.getElementById("sliderValue");
  if (sliderValueElement) {
    sliderValueElement.textContent = sliderValue.toString();
  }

  try {
    await sendCommand(currentCandlestickId, { speed: sliderValue });
    console.log("Slider value sent successfully!");
  } catch (error) {
    console.error("Error:", error);
    alert(`Failed to update speed: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
};

// Handler for color changes
export const handleColorChange = async (event: ChangeEvent<HTMLInputElement>): Promise<void> => {
  const inputElement = event.target as HTMLInputElement;
  const colorValue = inputElement.value;
  console.log("Selected color:", colorValue);

  const colorValueElement = document.getElementById("colorValue");
  if (colorValueElement) {
    colorValueElement.textContent = colorValue;
  }

  try {
    await sendCommand(currentCandlestickId, { color: colorValue });
    console.log("Color sent successfully!");
  } catch (error) {
    console.error("Error:", error);
    alert(`Failed to set color: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
};
