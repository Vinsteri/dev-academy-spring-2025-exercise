import React from 'react';
import { DailyStat } from './DailyStatsPage';

interface StatsListProps {
  stats: DailyStat[];
  onSort: (column: string) => void;
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
}

const StatsList: React.FC<StatsListProps> = ({ stats, onSort, sortColumn, sortDirection }) => {
  
  // (A) MOBILE-FRIENDLY CARD VIEW or (B) TABLE 
  // If you'd like to conditionally switch based on screen size, you could do so with CSS or a media query.

  // For a table approach:
  return (
    <table>
      <thead>
        <tr>
          <th onClick={() => onSort('date')}>
            Date 
            {sortColumn === 'date' ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : null}
          </th>
          <th onClick={() => onSort('total_consumption')}>
            Consumption 
            {sortColumn === 'total_consumption' ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : null}
          </th>
          <th onClick={() => onSort('total_production')}>
            Production
            {sortColumn === 'total_production' ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : null}
          </th>
          <th onClick={() => onSort('average_price')}>
            Avg Price
            {sortColumn === 'average_price' ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : null}
          </th>
          <th onClick={() => onSort('longest_negative_price_streak')}>
            Neg. Streak (hrs)
            {sortColumn === 'longest_negative_price_streak' ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : null}
          </th>
        </tr>
      </thead>
      <tbody>
        {stats.map((row) => (
          <tr key={row.date}>
            <td>{row.date}</td>
            <td>{row.total_consumption}</td>
            <td>{row.total_production}</td>
            <td>{row.average_price}</td>
            <td>{row.longest_negative_price_streak}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default StatsList;
