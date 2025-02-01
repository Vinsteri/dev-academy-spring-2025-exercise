export const formatValue = (value: number): string => {
    if (value >= 1000) {
      return value.toFixed(0); // Show as integer
    }
    return value.toFixed(2); // Round to 2 decimal places
  };