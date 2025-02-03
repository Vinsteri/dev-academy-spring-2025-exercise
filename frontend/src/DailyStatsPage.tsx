import React, { useState, useEffect } from 'react';
import SearchAndFilter from './SearchAndFilter.tsx';
import StatsList from './StatsList.tsx';
import PaginationControls from './PaginationControls.tsx';
import { Container, Typography } from '@mui/material';

export interface DailyStat {
  date: string;
  total_consumption: number;
  total_production: number;
  average_price: number;
  longest_negative_price_streak: number;
}

const DailyStatsPage: React.FC = () => {
  const [stats, setStats] = useState<DailyStat[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // For searching, filtering, pagination
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [sortColumn, setSortColumn] = useState('date');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  const [pageSize] = useState(25);

  useEffect(() => {
    setLoading(true);
    setError('');

    const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
    const url = `${baseUrl}/api/daily-stats?page=${currentPage}&pageSize=${pageSize}&sort=${sortColumn}&direction=${sortDirection}&search=${searchQuery}`;

    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch');
        return res.json();
      })
      .then((data) => {
        setStats(data.results);
        setTotalCount(data.total_count);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError('Error fetching data');
        setLoading(false);
      });
  }, [searchQuery, currentPage, sortColumn, sortDirection]);

  // Handlers for search/filter
  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setCurrentPage(1); // Reset to first page
  };

  // Handlers for sorting
  const handleSort = (column: string) => {
    if (sortColumn === column) {
      // Toggle asc/desc
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('asc');
    }
    setCurrentPage(1);
  };

  return (
    <Container maxWidth="sm" sx={{ marginY: 4 }}>
      <SearchAndFilter onSearch={handleSearch} />

      {loading && <Typography>Loading...</Typography>}
      {error && <Typography color="error">{error}</Typography>}

      {!loading && !error && (
        <>
          <StatsList
            stats={stats}
            onSort={handleSort}
            sortColumn={sortColumn}
            sortDirection={sortDirection}
          />
          <PaginationControls
            currentPage={currentPage}
            onPageChange={setCurrentPage}
            numberOfPages={Math.ceil(totalCount / pageSize)}
          />
        </>
      )}
    </Container>
  );
};

export default DailyStatsPage;
