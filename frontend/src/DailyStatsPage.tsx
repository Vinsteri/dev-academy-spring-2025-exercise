import React, { useState, useEffect } from 'react';
import SearchAndFilter from './SearchAndFilter.tsx';
import StatsList from './StatsList.tsx';
import PaginationControls from './PaginationControls.tsx';

export interface DailyStat {
  date: string;
  total_consumption: number;
  total_production: number;
  average_price: number;
  longest_negative_price_streak: number;
}

const DailyStatsPage: React.FC = () => {
  const [stats, setStats] = useState<DailyStat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // For searching, filtering, pagination
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [sortColumn, setSortColumn] = useState('date');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');

  useEffect(() => {
    setLoading(true);
    setError('');

    // Construct your query params (search, pagination, sorting) if needed
    const baseUrl = 'http://localhost:8000/api/daily-stats';
    const url = `${baseUrl}?page=${currentPage}&sort=${sortColumn}&direction=${sortDirection}&search=${searchQuery}`;

    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch');
        return res.json();
      })
      .then((data: DailyStat[]) => {
        setStats(data);
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
    <div className="daily-stats-page">
      <SearchAndFilter onSearch={handleSearch} />
      
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {!loading && !error && (
        <>
          <StatsList stats={stats} onSort={handleSort} sortColumn={sortColumn} sortDirection={sortDirection} />
          <PaginationControls currentPage={currentPage} onPageChange={setCurrentPage} />
        </>
      )}
    </div>
  );
};

export default DailyStatsPage;
