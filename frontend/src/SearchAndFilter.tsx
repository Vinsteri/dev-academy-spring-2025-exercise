import React, { useState } from 'react';
import {Box, Button, TextField} from '@mui/material';

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
    <Box 
      sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        gap: 2,
        marginBottom: 2,
        marginTop: 2,
        marginLeft: 2,
      }}
    >
      <Box 
        sx={{ 
          display: 'flex', 
          flexDirection: 'row', 
          gap: 2 
        }}
      >
        <TextField
          label="Search by date (e.g., 2025-01-01)"
          variant='filled'
          value={searchInput}
          onChange={handleSearchInput}
        />
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleSearchClick}
        >
          Search
        </Button>
      </Box>

      {/* Example of a filter select could go here 
         <FormControl>
           <InputLabel>Filter</InputLabel>
           <Select
             value={filterValue}
             onChange={handleFilterChange}
           >
             <MenuItem value="all">All</MenuItem>
             <MenuItem value="negative">Negative Price Only</MenuItem>
           </Select>
         </FormControl>
      */}
    </Box>
  );
};


export default SearchAndFilter;
