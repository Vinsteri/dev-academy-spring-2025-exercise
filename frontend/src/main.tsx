import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import DailyStatsPage from './DailyStatsPage.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <DailyStatsPage />
  </StrictMode>,
)
