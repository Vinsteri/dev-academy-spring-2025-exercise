import React from 'react';
import { DailyStat } from './DailyStatsPage';
import { formatValue, formatWhtoMWh, formatkWhtoMWh, formatHours } from './utils';
import { Table, TableHead, TableRow, TableCell, TableBody, Card, CardContent, Typography, useMediaQuery } from '@mui/material';


interface StatsListProps {
  stats: DailyStat[];
  onSort: (column: string) => void;
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
}

const StatsList: React.FC<StatsListProps> = ({ stats, onSort, sortColumn, sortDirection }) => {
  const isMobile = useMediaQuery('(max-width:600px)');

  return (
    <>
      {!isMobile ? (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell onClick={() => onSort('date')}>
                Date 
                {sortColumn === 'date' ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : null}
              </TableCell>
              <TableCell onClick={() => onSort('total_consumption')}>
                Consumption 
                {sortColumn === 'total_consumption' ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : null}
              </TableCell>
              <TableCell onClick={() => onSort('total_production')}>
                Production
                {sortColumn === 'total_production' ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : null}
              </TableCell>
              <TableCell onClick={() => onSort('average_price')}>
                Avg Price
                {sortColumn === 'average_price' ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : null}
              </TableCell>
              <TableCell onClick={() => onSort('longest_negative_price_streak')}>
                Neg. Streak (hrs)
                {sortColumn === 'longest_negative_price_streak' ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : null}
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {stats.map((row) => (
              <TableRow key={row.date}>
                <TableCell>{row.date}</TableCell>
                <TableCell>{formatWhtoMWh(row.total_consumption)} MWh</TableCell>
                <TableCell>{formatkWhtoMWh(row.total_production)} MWh</TableCell>
                <TableCell>{formatValue(row.average_price)} €/MWh</TableCell>
                <TableCell>{formatHours(row.longest_negative_price_streak)} hrs</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      ) : (
        <div className="card-view">
          {stats.map((row) => (
            <Card key={row.date} sx={{ marginBottom: 2 }}>
              <CardContent>
                <Typography variant="h6">Date: {row.date}</Typography>
                <Typography>Consumption: {formatWhtoMWh(row.total_consumption)} MWh</Typography>
                <Typography>Production: {formatkWhtoMWh(row.total_production)} MWh</Typography>
                <Typography>Avg Price: {formatValue(row.average_price)} €/MWh</Typography>
                <Typography>Neg. Streak (hrs): {formatHours(row.longest_negative_price_streak)} hrs</Typography>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </>
  );
};

export default StatsList;
