/**
 * GuardFlow Dashboard Component
 * Dashboard principal do sistema com design moderno
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  LinearProgress,
  Alert,
  CircularProgress,
  Chip,
  Avatar,
  Divider,
  useTheme,
} from '@mui/material';
import {
  ShoppingCart,
  Scanner,
  Nature as EcoIcon,
  TrendingUp,
  People,
  Store,
  Speed,
  CheckCircle,
  Error,
  Refresh,
  MonetizationOn,
  Security,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { mockApi } from '../services/mockApi';
import ConnectionTest from './ConnectionTest';
import GuardPassIntegration from './GuardPassIntegration';
import BrandConfig from './BrandConfig';

interface DashboardStats {
  totalScans: number;
  successfulScans: number;
  successRate: number;
  avgScanTime: number;
  esgScore: number;
  totalProducts: number;
  activeUsers: number;
}

interface ScanData {
  date: string;
  scans: number;
  success: number;
  efficiency: number;
}

const Dashboard: React.FC = () => {
  const theme = useTheme();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [scanData, setScanData] = useState<ScanData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    loadDashboardData();
    // Auto-refresh a cada 30 segundos
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Simular delay de API
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Usar mock API para demonstração
      const scanStatsResponse = await mockApi.getScanStats();
      const scanStats = scanStatsResponse.data.data;

      const esgResponse = await mockApi.getEsgDashboard();
      const esgData = esgResponse.data.data;

      const productsResponse = await mockApi.getProducts();
      const products = productsResponse.data.data.products || [];

      // Dados de gráfico mais realísticos
      const mockScanData: ScanData[] = [
        { date: '01/01', scans: 45, success: 42, efficiency: 93.3 },
        { date: '02/01', scans: 52, success: 48, efficiency: 92.3 },
        { date: '03/01', scans: 38, success: 35, efficiency: 92.1 },
        { date: '04/01', scans: 61, success: 58, efficiency: 95.1 },
        { date: '05/01', scans: 47, success: 44, efficiency: 93.6 },
        { date: '06/01', scans: 55, success: 52, efficiency: 94.5 },
        { date: '07/01', scans: 43, success: 40, efficiency: 93.0 },
      ];

      setStats({
        totalScans: scanStats?.total_scans || 0,
        successfulScans: scanStats?.successful_scans || 0,
        successRate: scanStats?.success_rate || 0,
        avgScanTime: scanStats?.avg_scan_time_ms || 0,
        esgScore: esgData?.total_score || 0,
        totalProducts: products.length,
        activeUsers: 150,
      });

      setScanData(mockScanData);
      setLastUpdate(new Date());
    } catch (err: any) {
      setError(err.message || 'Erro ao carregar dados do dashboard');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (rate: number) => {
    if (rate >= 95) return 'success';
    if (rate >= 90) return 'warning';
    return 'error';
  };

  const getEfficiencyColor = (score: number) => {
    if (score >= 90) return '#4caf50';
    if (score >= 80) return '#ff9800';
    return '#f44336';
  };

  if (loading && !stats) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px" flexDirection="column">
        <CircularProgress size={60} sx={{ mb: 2 }} />
        <Typography variant="h6" color="text.secondary">
          Carregando Dashboard...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        <Typography variant="h6">Erro ao carregar dados</Typography>
        <Typography>{error}</Typography>
        <Button onClick={loadDashboardData} startIcon={<Refresh />} sx={{ mt: 1 }}>
          Tentar Novamente
        </Button>
      </Alert>
    );
  }

  return (
    <Box sx={{ 
      p: 3, 
      backgroundColor: theme.palette.mode === 'dark' ? '#0a0a0a' : '#f5f5f5', 
      minHeight: '100vh',
      transition: 'background-color 0.3s ease',
    }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box>
            <Typography variant="h3" fontWeight="bold" color="primary">
              🚀 GuardFlow
            </Typography>
            <Typography variant="h6" color="text.secondary">
              Sistema de Checkout Inteligente
            </Typography>
          </Box>
          <Box display="flex" alignItems="center" gap={2}>
            <Chip
              icon={<CheckCircle />}
              label="Sistema Online"
              color="success"
              variant="outlined"
            />
            <Typography variant="caption" color="text.secondary">
              Última atualização: {lastUpdate.toLocaleTimeString()}
            </Typography>
          </Box>
        </Box>
        
        <Divider sx={{ mb: 3 }} />
        
        {/* Teste de conexão */}
        <ConnectionTest />
        
        {/* Integração GuardPass */}
        <GuardPassIntegration />
        
        {/* Configuração da Marca */}
        <BrandConfig />
      </Box>

      {/* Cards de estatísticas principais */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        {/* Total de Scans */}
        <Card sx={{ 
          flex: '1 1 300px', 
          minWidth: '300px', 
          background: theme.palette.mode === 'dark' 
            ? 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)' 
            : 'linear-gradient(135deg, #2196f3 0%, #1976d2 100%)', 
          color: 'white',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
          }
        }}>
          <CardContent>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box>
                <Typography variant="h6" sx={{ opacity: 0.9 }}>
                  Total de Scans
                </Typography>
                <Typography variant="h3" fontWeight="bold">
                  {stats?.totalScans?.toLocaleString() || 0}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  {stats?.successfulScans?.toLocaleString() || 0} bem-sucedidos
                </Typography>
              </Box>
              <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', width: 60, height: 60 }}>
                <Scanner sx={{ fontSize: 30 }} />
              </Avatar>
            </Box>
          </CardContent>
        </Card>

        {/* Taxa de Sucesso */}
        <Card sx={{ 
          flex: '1 1 300px', 
          minWidth: '300px', 
          background: theme.palette.mode === 'dark' 
            ? 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)' 
            : 'linear-gradient(135deg, #4caf50 0%, #388e3c 100%)', 
          color: 'white',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
          }
        }}>
          <CardContent>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box>
                <Typography variant="h6" sx={{ opacity: 0.9 }}>
                  Taxa de Sucesso
                </Typography>
                <Typography variant="h3" fontWeight="bold">
                  {stats?.successRate || 0}%
                </Typography>
                <Box display="flex" alignItems="center" gap={1} mt={1}>
                  <LinearProgress 
                    variant="determinate" 
                    value={stats?.successRate || 0} 
                    sx={{ flex: 1, height: 6, borderRadius: 3, bgcolor: 'rgba(255,255,255,0.2)' }}
                  />
                  <Typography variant="caption" sx={{ opacity: 0.8 }}>
                    {(stats?.successRate || 0) >= 95 ? 'Excelente' : (stats?.successRate || 0) >= 90 ? 'Bom' : 'Precisa melhorar'}
                  </Typography>
                </Box>
              </Box>
              <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', width: 60, height: 60 }}>
                <TrendingUp sx={{ fontSize: 30 }} />
              </Avatar>
            </Box>
          </CardContent>
        </Card>

        {/* Score ESG */}
        <Card sx={{ 
          flex: '1 1 300px', 
          minWidth: '300px', 
          background: theme.palette.mode === 'dark' 
            ? 'linear-gradient(135deg, #0f2027 0%, #203a43 100%)' 
            : 'linear-gradient(135deg, #4caf50 0%, #2e7d32 100%)', 
          color: 'white',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
          }
        }}>
          <CardContent>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box>
                <Typography variant="h6" sx={{ opacity: 0.9 }}>
                  Score ESG
                </Typography>
                <Typography variant="h3" fontWeight="bold">
                  {stats?.esgScore || 0}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Sustentabilidade
                </Typography>
              </Box>
              <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', width: 60, height: 60 }}>
                <EcoIcon sx={{ fontSize: 30 }} />
              </Avatar>
            </Box>
          </CardContent>
        </Card>

        {/* Produtos Cadastrados */}
        <Card sx={{ 
          flex: '1 1 300px', 
          minWidth: '300px', 
          background: theme.palette.mode === 'dark' 
            ? 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)' 
            : 'linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%)', 
          color: 'white',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
          }
        }}>
          <CardContent>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box>
                <Typography variant="h6" sx={{ opacity: 0.9 }}>
                  Produtos
                </Typography>
                <Typography variant="h3" fontWeight="bold">
                  {stats?.totalProducts || 0}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.8 }}>
                  Cadastrados
                </Typography>
              </Box>
              <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', width: 60, height: 60 }}>
                <Store sx={{ fontSize: 30 }} />
              </Avatar>
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Seção de Gráficos */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        {/* Gráfico de Performance */}
        <Card sx={{ flex: '2 1 600px', minWidth: '600px' }}>
          <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6" fontWeight="bold">
                📊 Performance de Scans
              </Typography>
              <Chip 
                icon={<Speed />}
                label={`${stats?.avgScanTime || 0}ms médio`}
                color="primary"
                variant="outlined"
              />
            </Box>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={scanData}>
                <defs>
                  <linearGradient id="colorScans" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#8884d8" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="colorSuccess" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#82ca9d" stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #ccc',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                  }}
                />
                <Area type="monotone" dataKey="scans" stroke="#8884d8" fillOpacity={1} fill="url(#colorScans)" strokeWidth={2} />
                <Area type="monotone" dataKey="success" stroke="#82ca9d" fillOpacity={1} fill="url(#colorSuccess)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Métricas de Performance */}
        <Card sx={{ flex: '1 1 300px', minWidth: '300px' }}>
          <CardContent>
            <Typography variant="h6" fontWeight="bold" gutterBottom>
              ⚡ Métricas de Performance
            </Typography>
            
            <Box sx={{ mb: 3 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                <Typography variant="body2" color="text.secondary">
                  Eficiência do Sistema
                </Typography>
                <Typography variant="h6" fontWeight="bold">
                  {stats?.successRate || 0}%
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={stats?.successRate || 0} 
                color={getStatusColor(stats?.successRate || 0)}
                sx={{ height: 8, borderRadius: 4 }}
              />
            </Box>

            <Box sx={{ mb: 3 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                <Typography variant="body2" color="text.secondary">
                  Score ESG
                </Typography>
                <Typography variant="h6" fontWeight="bold">
                  {stats?.esgScore || 0}/100
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={stats?.esgScore || 0} 
                color="success"
                sx={{ height: 8, borderRadius: 4 }}
              />
            </Box>

            <Box sx={{ mb: 3 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                <Typography variant="body2" color="text.secondary">
                  Tempo Médio de Scan
                </Typography>
                <Typography variant="h6" fontWeight="bold">
                  {stats?.avgScanTime || 0}ms
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={Math.min((stats?.avgScanTime || 0) / 10, 100)} 
                color="info"
                sx={{ height: 8, borderRadius: 4 }}
              />
            </Box>

            <Divider sx={{ my: 2 }} />
            
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="body2" color="text.secondary">
                Usuários Ativos
              </Typography>
              <Box display="flex" alignItems="center" gap={1}>
                <People color="primary" />
                <Typography variant="h6" fontWeight="bold">
                  {stats?.activeUsers || 0}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Ações Rápidas */}
      <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <CardContent>
          <Typography variant="h6" fontWeight="bold" gutterBottom>
            🚀 Ações Rápidas
          </Typography>
          <Box display="flex" gap={2} flexWrap="wrap">
            <Button
              variant="contained"
              startIcon={<Scanner />}
              onClick={() => window.open('/scanner', '_blank')}
              sx={{ 
                bgcolor: 'rgba(255,255,255,0.2)', 
                '&:hover': { bgcolor: 'rgba(255,255,255,0.3)' },
                color: 'white',
                border: '1px solid rgba(255,255,255,0.3)'
              }}
            >
              Abrir Scanner
            </Button>
            <Button
              variant="outlined"
              startIcon={<ShoppingCart />}
              onClick={() => window.open('/cart', '_blank')}
              sx={{ 
                borderColor: 'rgba(255,255,255,0.5)', 
                color: 'white',
                '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
              }}
            >
              Ver Carrinho
            </Button>
            <Button
              variant="contained"
              startIcon={<Security />}
              onClick={() => window.open('/qr-checkout', '_blank')}
              sx={{ 
                bgcolor: 'rgba(255,255,255,0.2)', 
                '&:hover': { bgcolor: 'rgba(255,255,255,0.3)' },
                color: 'white',
                border: '1px solid rgba(255,255,255,0.3)'
              }}
            >
              QR Checkout Demo
            </Button>
            <Button
              variant="outlined"
              startIcon={<People />}
              onClick={() => window.open('/seve', '_blank')}
              sx={{ 
                borderColor: 'rgba(255,255,255,0.5)', 
                color: 'white',
                '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
              }}
            >
              SEVE Personalização
            </Button>
            <Button
              variant="outlined"
              startIcon={<EcoIcon />}
              onClick={() => window.open('/esg', '_blank')}
              sx={{ 
                borderColor: 'rgba(255,255,255,0.5)', 
                color: 'white',
                '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
              }}
            >
              Dashboard ESG
            </Button>
            <Button
              variant="outlined"
              startIcon={<People />}
              onClick={() => window.open('/users', '_blank')}
              sx={{ 
                borderColor: 'rgba(255,255,255,0.5)', 
                color: 'white',
                '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
              }}
            >
              Gerenciar Usuários
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;