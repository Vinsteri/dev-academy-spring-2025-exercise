export const formatValue = (value: number): string => {
    if (value >= 1000) {
        return value.toFixed(0); // Show as integer
    }
    return value.toFixed(2); // Round to 2 decimal places
};

export const formatkWhtoMWh = (value: number): string => {
    return (value / 1000).toFixed(2);
}

export const formatWhtoMWh = (value: number): string => {
    return (value / 10000).toFixed(2);
}

export const formatHours = (value: number): string => {
    return value.toFixed(0);
}