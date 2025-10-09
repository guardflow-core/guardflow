/**
 * GuardFlow Theme System
 * Sistema de temas avançado com modo dark e cores elegantes
 */

import { createTheme, ThemeOptions } from '@mui/material/styles';

// Paleta de cores elegantes da marca GuardFlow
export const brandColors = {
  // Cores principais da marca
  primary: {
    50: '#e3f2fd',
    100: '#bbdefb',
    200: '#90caf9',
    300: '#64b5f6',
    400: '#42a5f5',
    500: '#2196f3', // Azul principal
    600: '#1e88e5',
    700: '#1976d2',
    800: '#1565c0',
    900: '#0d47a1',
  },
  secondary: {
    50: '#f3e5f5',
    100: '#e1bee7',
    200: '#ce93d8',
    300: '#ba68c8',
    400: '#ab47bc',
    500: '#9c27b0', // Roxo principal
    600: '#8e24aa',
    700: '#7b1fa2',
    800: '#6a1b9a',
    900: '#4a148c',
  },
  // Cores ESG (Sustentabilidade)
  esg: {
    50: '#e8f5e8',
    100: '#c8e6c9',
    200: '#a5d6a7',
    300: '#81c784',
    400: '#66bb6a',
    500: '#4caf50', // Verde ESG
    600: '#43a047',
    700: '#388e3c',
    800: '#2e7d32',
    900: '#1b5e20',
  },
  // Cores de status
  success: {
    50: '#e8f5e8',
    100: '#c8e6c9',
    200: '#a5d6a7',
    300: '#81c784',
    400: '#66bb6a',
    500: '#4caf50',
    600: '#43a047',
    700: '#388e3c',
    800: '#2e7d32',
    900: '#1b5e20',
  },
  warning: {
    50: '#fff8e1',
    100: '#ffecb3',
    200: '#ffe082',
    300: '#ffd54f',
    400: '#ffca28',
    500: '#ffc107',
    600: '#ffb300',
    700: '#ffa000',
    800: '#ff8f00',
    900: '#ff6f00',
  },
  error: {
    50: '#ffebee',
    100: '#ffcdd2',
    200: '#ef9a9a',
    300: '#e57373',
    400: '#ef5350',
    500: '#f44336',
    600: '#e53935',
    700: '#d32f2f',
    800: '#c62828',
    900: '#b71c1c',
  },
  // Cores neutras elegantes
  neutral: {
    50: '#fafafa',
    100: '#f5f5f5',
    200: '#eeeeee',
    300: '#e0e0e0',
    400: '#bdbdbd',
    500: '#9e9e9e',
    600: '#757575',
    700: '#616161',
    800: '#424242',
    900: '#212121',
  }
};

// Gradientes da marca
export const brandGradients = {
  primary: 'linear-gradient(135deg, #2196f3 0%, #1976d2 100%)',
  secondary: 'linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%)',
  esg: 'linear-gradient(135deg, #4caf50 0%, #388e3c 100%)',
  success: 'linear-gradient(135deg, #4caf50 0%, #2e7d32 100%)',
  warning: 'linear-gradient(135deg, #ffc107 0%, #ff8f00 100%)',
  error: 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)',
  // Gradientes elegantes
  elegant: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  ocean: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  sunset: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
  forest: 'linear-gradient(135deg, #134e5e 0%, #71b280 100%)',
  // Gradientes dark
  darkElegant: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
  darkOcean: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
  darkForest: 'linear-gradient(135deg, #0f2027 0%, #203a43 100%)',
};

// Configuração do tema light
export const lightThemeOptions: ThemeOptions = {
  palette: {
    mode: 'light',
    primary: {
      main: brandColors.primary[500],
      light: brandColors.primary[300],
      dark: brandColors.primary[700],
      contrastText: '#ffffff',
    },
    secondary: {
      main: brandColors.secondary[500],
      light: brandColors.secondary[300],
      dark: brandColors.secondary[700],
      contrastText: '#ffffff',
    },
    background: {
      default: '#fafafa',
      paper: '#ffffff',
    },
    text: {
      primary: brandColors.neutral[900],
      secondary: brandColors.neutral[600],
    },
    success: {
      main: brandColors.esg[500],
      light: brandColors.esg[300],
      dark: brandColors.esg[700],
    },
    warning: {
      main: brandColors.warning[500],
      light: brandColors.warning[300],
      dark: brandColors.warning[700],
    },
    error: {
      main: brandColors.error[500],
      light: brandColors.error[300],
      dark: brandColors.error[700],
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
      lineHeight: 1.2,
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
      lineHeight: 1.3,
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.75rem',
      lineHeight: 1.4,
    },
    h4: {
      fontWeight: 600,
      fontSize: '1.5rem',
      lineHeight: 1.4,
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.25rem',
      lineHeight: 1.5,
    },
    h6: {
      fontWeight: 600,
      fontSize: '1.1rem',
      lineHeight: 1.5,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.6,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.07)',
          border: '1px solid rgba(0, 0, 0, 0.05)',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 8,
          padding: '8px 16px',
          transition: 'all 0.3s ease',
        },
        contained: {
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
          '&:hover': {
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.15)',
            transform: 'translateY(-1px)',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 20,
          fontWeight: 500,
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          height: 6,
        },
      },
    },
  },
};

// Configuração do tema dark
export const darkThemeOptions: ThemeOptions = {
  palette: {
    mode: 'dark',
    primary: {
      main: brandColors.primary[400],
      light: brandColors.primary[300],
      dark: brandColors.primary[600],
      contrastText: '#ffffff',
    },
    secondary: {
      main: brandColors.secondary[400],
      light: brandColors.secondary[300],
      dark: brandColors.secondary[600],
      contrastText: '#ffffff',
    },
    background: {
      default: '#0a0a0a',
      paper: '#1a1a1a',
    },
    text: {
      primary: '#ffffff',
      secondary: brandColors.neutral[400],
    },
    success: {
      main: brandColors.esg[400],
      light: brandColors.esg[300],
      dark: brandColors.esg[600],
    },
    warning: {
      main: brandColors.warning[400],
      light: brandColors.warning[300],
      dark: brandColors.warning[600],
    },
    error: {
      main: brandColors.error[400],
      light: brandColors.error[300],
      dark: brandColors.error[600],
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
      lineHeight: 1.2,
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
      lineHeight: 1.3,
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.75rem',
      lineHeight: 1.4,
    },
    h4: {
      fontWeight: 600,
      fontSize: '1.5rem',
      lineHeight: 1.4,
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.25rem',
      lineHeight: 1.5,
    },
    h6: {
      fontWeight: 600,
      fontSize: '1.1rem',
      lineHeight: 1.5,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.6,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 8px 25px rgba(0, 0, 0, 0.4)',
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 8,
          padding: '8px 16px',
          transition: 'all 0.3s ease',
        },
        contained: {
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.3)',
          '&:hover': {
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.4)',
            transform: 'translateY(-1px)',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 20,
          fontWeight: 500,
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          height: 6,
        },
      },
    },
  },
};

// Criar temas
export const lightTheme = createTheme(lightThemeOptions);
export const darkTheme = createTheme(darkThemeOptions);

// Configurações da marca
export const brandConfig = {
  name: 'GuardFlow',
  slogan: 'Agiliza aí suas compras!',
  tagline: 'Sistema de Checkout Inteligente',
  description: 'Revolucione sua experiência de compras com tecnologia ESG e sustentabilidade',
  colors: brandColors,
  gradients: brandGradients,
  logo: '🚀',
  version: '0.1.0',
  features: [
    'Checkout Inteligente',
    'Tokenização ESG',
    'Sustentabilidade',
    'Segurança Avançada',
    'Integração GuardPass'
  ]
};
