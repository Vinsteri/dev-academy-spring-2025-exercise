import React from 'react';
import { Pagination } from '@mui/material';

interface PaginationControlsProps {
  currentPage: number;
  numberOfPages: number;
  onPageChange: (page: number) => void;
}

const PaginationControls: React.FC<PaginationControlsProps> = ({
  currentPage,
  onPageChange,
  numberOfPages
}) => {
  // MUI Pagination calls onChange with event + pageNumber
  const handleChange = (_: React.ChangeEvent<unknown>, page: number) => {
    onPageChange(page);
  };


  return (
    <Pagination
      count={numberOfPages}
      page={currentPage}
      onChange={handleChange}
      sx={{ marginTop: 2, display: 'flex', justifyContent: 'center' }}
      shape="rounded"        // optional styling
      color="primary"        // sets the color to your theme primary
    />
  );
};

export default PaginationControls;
