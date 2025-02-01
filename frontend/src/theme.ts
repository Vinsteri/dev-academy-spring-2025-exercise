// src/theme.ts
import { createTheme } from '@mui/material/styles';

export const lightTheme = createTheme({
  palette: {
    mode: 'light',
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          color: '#213547',
          backgroundColor: '#ffffff',
        },
        a: {
          '&:hover': {
            color: '#747bff',
          },
        },
        button: {
          backgroundColor: '#f9f9f9',
          fontFamily: 'inherit',
          cursor: 'pointer',
          transition: 'border-color 0.25s',
          '&:hover': {
            borderColor: '#646cff',
          },
          '&:focus, &:focus-visible': {
            outline: '4px auto -webkit-focus-ring-color',
          },
        },
      },
    },
  },
});

export const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#1a1a1a',
        },
      },
    },
  },
});