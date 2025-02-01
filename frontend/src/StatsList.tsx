import React from 'react';
import { DailyStat } from './DailyStatsPage';
import { formatValue, formatWhtoMWh, formatkWhtoMWh, formatHours } from './utils';
import './StatsList.css';

interface StatsListProps {
  stats: DailyStat[];
  onSort: (column: string) => void;
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
}

const StatsList: React.FC<StatsListProps> = ({ stats, onSort, sortColumn, sortDirection }) => {
  return (
    <>
      <table className="table-view">
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
              <td>{formatWhtoMWh(row.total_consumption)} MWh</td>
              <td>{formatkWhtoMWh(row.total_production)} MWh</td>
              <td>{formatValue(row.average_price)} €/MWh</td>
              <td>{formatHours(row.longest_negative_price_streak)} hrs</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="card-view">
        {stats.map((row) => (
          <div className="card" key={row.date}>
            <div><span>Date:</span> {row.date}</div>
            <div><span>Consumption:</span> {formatWhtoMWh(row.total_consumption)} Mwh</div>
            <div><span>Production:</span> {formatkWhtoMWh(row.total_production)} Mwh</div>
            <div><span>Avg Price:</span> {formatValue(row.average_price)} €/MWh</div>
            <div><span>Neg. Streak (hrs):</span> {formatHours(row.longest_negative_price_streak)} hrs</div>
          </div>
        ))}
      </div>
    </>
  );
};

export default StatsList;
