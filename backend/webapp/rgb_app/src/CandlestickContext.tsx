// CandlestickContext - Shared state for candlestick data
// This eliminates duplicate API polling by providing a single source of truth

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Candlestick, listCandlesticks, setCurrentCandlestickId } from './http_handler';

interface CandlestickContextType {
  candlesticks: Candlestick[];
  selectedCandlestick: Candlestick | null;
  selectedId: string;
  setSelectedId: (id: string) => void;
  loading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
}

const CandlestickContext = createContext<CandlestickContextType | undefined>(undefined);

interface CandlestickProviderProps {
  children: ReactNode;
  pollInterval?: number; // in milliseconds, default 3000
}

export const CandlestickProvider = ({ children, pollInterval = 3000 }: CandlestickProviderProps) => {
  const [candlesticks, setCandlesticks] = useState<Candlestick[]>([]);
  // Start with empty string to allow auto-selection of first connected candlestick
  const [selectedId, setSelectedIdState] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCandlesticks = async () => {
    try {
      const sticks = await listCandlesticks();
      setCandlesticks(sticks);
      setError(null);
      
      // Auto-select logic: if current selection is not in the list (or empty), select first connected
      const currentSelectionExists = sticks.some(c => c.id === selectedId);
      if ((!selectedId || !currentSelectionExists) && sticks.length > 0) {
        const firstConnected = sticks.find(c => c.connected);
        const newId = firstConnected?.id || sticks[0].id;
        setSelectedIdState(newId);
        setCurrentCandlestickId(newId);
      }
    } catch (err) {
      setError("Failed to connect to backend");
      console.error("Error fetching candlesticks:", err);
    } finally {
      setLoading(false);
    }
  };

  // Update both local state and http_handler's currentCandlestickId
  const setSelectedId = (id: string) => {
    setSelectedIdState(id);
    setCurrentCandlestickId(id);
  };

  // Poll for candlestick updates
  useEffect(() => {
    fetchCandlesticks();
    const interval = setInterval(fetchCandlesticks, pollInterval);
    return () => clearInterval(interval);
  }, [pollInterval]);

  // Find the selected candlestick from the list
  const selectedCandlestick = candlesticks.find(c => c.id === selectedId) || null;

  const value: CandlestickContextType = {
    candlesticks,
    selectedCandlestick,
    selectedId,
    setSelectedId,
    loading,
    error,
    refresh: fetchCandlesticks,
  };

  return (
    <CandlestickContext.Provider value={value}>
      {children}
    </CandlestickContext.Provider>
  );
};

// Custom hook to use the candlestick context
export const useCandlestick = (): CandlestickContextType => {
  const context = useContext(CandlestickContext);
  if (context === undefined) {
    throw new Error('useCandlestick must be used within a CandlestickProvider');
  }
  return context;
};
