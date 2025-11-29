import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Box, Chip, IconButton, Tooltip } from '@mui/material';
import { Palette, Info } from '@mui/icons-material';
import { CustomThemeProvider, useTheme } from './contexts/ThemeContext';
import ThemeToggle from './components/ThemeToggle';
import Dashboard from './components/Dashboard';
import QRCheckoutDemo from './pages/QRCheckoutDemo';
import SEVEPersonalization from './components/SEVEPersonalization';
import ScannerPage from './pages/ScannerPage';
import CartPage from './pages/CartPage';
import ESGDashboard from './pages/ESGDashboard';
import UsersPage from './pages/UsersPage';
import PerformancePage from './pages/PerformancePage';
import SymbioticAgentPage from './pages/SymbioticAgentPage';
import CheckoutSymbioticAgentPage from './pages/CheckoutSymbioticAgentPage';
import './App.css';

// Componente principal da aplicação
const AppContent: React.FC = () => {
  const { brand } = useTheme();

  return (
    <Router>
      <Box sx={{ flexGrow: 1, minHeight: '100vh' }}>
        <AppBar 
          position="static" 
          sx={{ 
            background: 'linear-gradient(135deg, #2196f3 0%, #1976d2 100%)',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
            transition: 'all 0.3s ease',
          }}
        >
          <Toolbar>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexGrow: 1 }}>
              <Typography variant="h5" component="div" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                {brand.logo} {brand.name}
              </Typography>
              <Chip 
                label={brand.slogan}
                size="small" 
                sx={{ 
                  bgcolor: 'rgba(255,255,255,0.2)', 
                  color: 'white',
                  fontWeight: 500,
                  fontSize: '0.75rem',
                  height: 24,
                }} 
              />
            </Box>
            
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <ThemeToggle variant="icon" size="medium" />
              <Tooltip title={`${brand.name} v${brand.version}`}>
                <IconButton color="inherit" size="small">
                  <Info />
                </IconButton>
              </Tooltip>
            </Box>
          </Toolbar>
        </AppBar>
          
        <Container maxWidth="xl" sx={{ mt: 0, mb: 0, p: 0 }}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/scanner" element={<ScannerPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/esg" element={<ESGDashboard />} />
          <Route path="/users" element={<UsersPage />} />
          <Route path="/performance" element={<PerformancePage />} />
          <Route path="/symbiotic-agent" element={<SymbioticAgentPage />} />
          <Route path="/checkout-symbiotic-agent" element={<CheckoutSymbioticAgentPage />} />
          <Route path="/qr-checkout" element={<QRCheckoutDemo />} />
          <Route path="/seve" element={<SEVEPersonalization />} />
          </Routes>
        </Container>
      </Box>
    </Router>
  );
};

// Componente principal com provider de tema
function App() {
  return (
    <CustomThemeProvider>
      <AppContent />
    </CustomThemeProvider>
  );
}

export default App;