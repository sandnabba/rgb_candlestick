import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { CandlestickProvider } from './CandlestickContext.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <CandlestickProvider>
      <App />
    </CandlestickProvider>
  </StrictMode>,
)
