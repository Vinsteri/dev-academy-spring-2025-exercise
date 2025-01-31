import React, { useState } from 'react';

interface SearchAndFilterProps {
  onSearch: (query: string) => void;
}

const SearchAndFilter: React.FC<SearchAndFilterProps> = ({ onSearch }) => {
  const [searchInput, setSearchInput] = useState('');

  const handleSearchInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchInput(e.target.value);
  };

  const handleSearchClick = () => {
    onSearch(searchInput);
  };

  return (
    <div className="search-and-filter">
      <input
        type="text"
        placeholder="Search by date, e.g. 2025-01-01"
        value={searchInput}
        onChange={handleSearchInput}
      />
      <button onClick={handleSearchClick}>Search</button>
      
      {/* Example additional filters: 
        <select>
          <option value="all">All Days</option>
          <option value="negative">Negative Price Days Only</option>
        </select>
      */}
    </div>
  );
};

export default SearchAndFilter;
