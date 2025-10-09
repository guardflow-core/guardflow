/**
 * Theme Toggle Component
 * Componente elegante para alternar entre modo light e dark
 */

import React from 'react';
import {
  IconButton,
  Tooltip,
  Box,
  Typography,
  Switch,
  FormControlLabel,
  Chip,
} from '@mui/material';
import {
  DarkMode,
  LightMode,
  Palette,
  AutoMode,
} from '@mui/icons-material';
import { useTheme } from '../contexts/ThemeContext';

interface ThemeToggleProps {
  variant?: 'icon' | 'switch' | 'chip' | 'full';
  showLabel?: boolean;
  size?: 'small' | 'medium' | 'large';
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({ 
  variant = 'icon', 
  showLabel = false,
  size = 'medium' 
}) => {
  const { isDarkMode, toggleTheme, brand } = useTheme();

  const getIcon = () => {
    if (isDarkMode) {
      return <LightMode fontSize={size} />;
    }
    return <DarkMode fontSize={size} />;
  };

  const getTooltipText = () => {
    return isDarkMode ? 'Alternar para modo claro' : 'Alternar para modo escuro';
  };

  const getChipColor = () => {
    return isDarkMode ? 'primary' : 'default';
  };

  const getChipIcon = () => {
    return isDarkMode ? <LightMode /> : <DarkMode />;
  };

  if (variant === 'icon') {
    return (
      <Tooltip title={getTooltipText()}>
        <IconButton
          onClick={toggleTheme}
          color="inherit"
          sx={{
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'scale(1.1)',
            },
          }}
        >
          {getIcon()}
        </IconButton>
      </Tooltip>
    );
  }

  if (variant === 'switch') {
    return (
      <FormControlLabel
        control={
          <Switch
            checked={isDarkMode}
            onChange={toggleTheme}
            color="primary"
            sx={{
              '& .MuiSwitch-thumb': {
                transition: 'all 0.3s ease',
              },
            }}
          />
        }
        label={showLabel ? (isDarkMode ? 'Modo Escuro' : 'Modo Claro') : ''}
        sx={{
          '& .MuiFormControlLabel-label': {
            fontSize: '0.875rem',
            fontWeight: 500,
          },
        }}
      />
    );
  }

  if (variant === 'chip') {
    return (
      <Chip
        icon={getChipIcon()}
        label={isDarkMode ? 'Modo Escuro' : 'Modo Claro'}
        onClick={toggleTheme}
        color={getChipColor()}
        variant={isDarkMode ? 'filled' : 'outlined'}
        sx={{
          transition: 'all 0.3s ease',
          cursor: 'pointer',
          '&:hover': {
            transform: 'scale(1.05)',
          },
        }}
      />
    );
  }

  if (variant === 'full') {
    return (
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          p: 2,
          borderRadius: 2,
          bgcolor: 'background.paper',
          border: '1px solid',
          borderColor: 'divider',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: 2,
          },
        }}
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 1,
          }}
        >
          <Palette color="primary" />
          <Typography variant="body2" fontWeight={500}>
            Tema
          </Typography>
        </Box>
        
        <Switch
          checked={isDarkMode}
          onChange={toggleTheme}
          color="primary"
          sx={{
            '& .MuiSwitch-thumb': {
              transition: 'all 0.3s ease',
            },
          }}
        />
        
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 1,
            ml: 1,
          }}
        >
          {getIcon()}
          <Typography variant="body2" color="text.secondary">
            {isDarkMode ? 'Escuro' : 'Claro'}
          </Typography>
        </Box>
      </Box>
    );
  }

  return null;
};

export default ThemeToggle;
