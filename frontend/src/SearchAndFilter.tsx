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
          gap: 2, 
          justifyContent: 'space-between',
        }}
      >
        <TextField
          label="Search by date (e.g., 2020-12-31)"
          variant='standard'
          value={searchInput}
          onChange={handleSearchInput}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              handleSearchClick();
            }
          }}
          sx={{ width: '80%' }}
        />
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleSearchClick}

        >
          Search
        </Button>
      </Box>
    </Box>
  );
};


export default SearchAndFilter;
