import React from 'react';

interface PaginationControlsProps {
  currentPage: number;
  numberOfPages: number;
  onPageChange: (page: number) => void;
}

const PaginationControls: React.FC<PaginationControlsProps> = ({ currentPage, numberOfPages, onPageChange }) => {
  const handleFirst = () => {
    onPageChange(1);
  };
  
  const handlePrev = () => {
    if (currentPage > 1) onPageChange(currentPage - 1);
  };

  const handleNext = () => {
    if (currentPage < numberOfPages) onPageChange(currentPage + 1);
  };

  const handleLast = () => {
    onPageChange(numberOfPages);
  }


  return (
    <div className="pagination-controls">
      <button onClick={handleFirst} disabled={currentPage === 1}>
        First
      </button>
      <button onClick={handlePrev} disabled={currentPage === 1}>
        Prev
      </button>
      <span>Page {currentPage}</span>
      <button onClick={handleNext} disabled={currentPage === numberOfPages}>
        Next
        </button>
      <button onClick={handleLast} disabled={currentPage === numberOfPages}>
        Last
      </button>
    </div>
  );
};

export default PaginationControls;
