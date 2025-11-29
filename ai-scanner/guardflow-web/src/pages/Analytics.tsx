import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tabs,
  Tab,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  LinearProgress,
  useTheme,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Eco,
  Speed,
  Security,
  Analytics,
  Assessment,
  Timeline,
} from '@mui/icons-material';
import { useSelector } from 'react-redux';
import { RootState } from '../store';

// Tipos
interface AnalyticsData {
  period: string;
  metrics: {
    totalScans: number;
    successRate: number;
    avgScanTime: number;
    esgScore: number;
    totalTransactions: number;
    totalRevenue: number;
  };
  trends: {
    scans: number[];
    esg: number[];
    revenue: number[];
  };
  topProducts: Array<{
    name: string;
    scans: number;
    esgScore: number;
  }>;
  esgBreakdown: {
    environmental: number;
    social: number;
    governance: number;
  };
}

// Componente Analytics
const Analytics: React.FC = () => {
  // Hooks
  const theme = useTheme();
  
  // Redux state
  const { totalScanned, successRate } = useSelector((state: RootState) => state.scanner);
  const { totalAmount, totalItems, averageESGScore } = useSelector((state: RootState) => state.cart);
  const { currentScore } = useSelector((state: RootState) => state.esg);
  
  // Local state
  const [selectedPeriod, setSelectedPeriod] = useState('7d');
  const [selectedTab, setSelectedTab] = useState(0);
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  
  // Effects
  useEffect(() => {
    // Simular dados de analytics
    setAnalyticsData({
      period: selectedPeriod,
      metrics: {
        totalScans: totalScanned,
        successRate: successRate * 100,
        avgScanTime: 2.3,
        esgScore: currentScore?.overall || 0,
        totalTransactions: 45,
        totalRevenue: totalAmount,
      },
      trends: {
        scans: [10, 15, 12, 18, 22, 25, 28],
        esg: [7.2, 7.5, 7.8, 8.1, 8.3, 8.5, 8.7],
        revenue: [120, 150, 180, 220, 250, 280, 320],
      },
      topProducts: [
        { name: 'Leite Orgânico', scans: 45, esgScore: 9.2 },
        { name: 'Pão Integral', scans: 38, esgScore: 8.8 },
        { name: 'Frutas Locais', scans: 32, esgScore: 9.5 },
        { name: 'Verduras Orgânicas', scans: 28, esgScore: 9.1 },
      ],
      esgBreakdown: {
        environmental: currentScore?.environmental || 0,
        social: currentScore?.social || 0,
        governance: currentScore?.governance || 0,
      },
    });
  }, [selectedPeriod, totalScanned, successRate, totalAmount, currentScore]);
  
  // Handlers
  const handlePeriodChange = (event: any) => {
    setSelectedPeriod(event.target.value);
  };
  
  const handleTabChange = (event: any, newValue: number) => {
    setSelectedTab(newValue);
  };
  
  // Renderizar métrica
  const renderMetric = (title: string, value: string | number, change: number, icon: React.ReactNode) => (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box sx={{ 
            bgcolor: change > 0 ? theme.palette.success.main : theme.palette.error.main,
            color: 'white',
            borderRadius: '50%',
            p: 1,
            mr: 2
          }}>
            {icon}
          </Box>
          <Box>
            <Typography variant="h6" component="div">
              {value}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {title}
            </Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Chip
            label={`${change > 0 ? '+' : ''}${change}%`}
            color={change > 0 ? 'success' : 'error'}
            size="small"
            sx={{ mr: 1 }}
          />
          <Typography variant="body2" color="text.secondary">
            vs. período anterior
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
  
  // Renderizar gráfico placeholder
  const renderChart = (title: string, data: number[]) => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <Box sx={{ height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Typography variant="body1" color="text.secondary">
            Gráfico de {title.toLowerCase()} será implementado aqui
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
  
  // Renderizar breakdown ESG
  const renderESGBreakdown = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Breakdown ESG
        </Typography>
        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body2">Ambiental</Typography>
            <Typography variant="body2">{analyticsData?.esgBreakdown.environmental.toFixed(1)}</Typography>
          </Box>
          <LinearProgress 
            variant="determinate" 
            value={analyticsData?.esgBreakdown.environmental ? analyticsData.esgBreakdown.environmental * 10 : 0} 
            color="success" 
          />
        </Box>
        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body2">Social</Typography>
            <Typography variant="body2">{analyticsData?.esgBreakdown.social.toFixed(1)}</Typography>
          </Box>
          <LinearProgress 
            variant="determinate" 
            value={analyticsData?.esgBreakdown.social ? analyticsData.esgBreakdown.social * 10 : 0} 
            color="success" 
          />
        </Box>
        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body2">Governança</Typography>
            <Typography variant="body2">{analyticsData?.esgBreakdown.governance.toFixed(1)}</Typography>
          </Box>
          <LinearProgress 
            variant="determinate" 
            value={analyticsData?.esgBreakdown.governance ? analyticsData.esgBreakdown.governance * 10 : 0} 
            color="success" 
          />
        </Box>
      </CardContent>
    </Card>
  );
  
  // Renderizar top produtos
  const renderTopProducts = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Top Produtos
        </Typography>
        <List>
          {analyticsData?.topProducts.map((product, index) => (
            <ListItem key={index} sx={{ px: 0 }}>
              <ListItemIcon>
                <Chip label={index + 1} size="small" color="primary" />
              </ListItemIcon>
              <ListItemText
                primary={product.name}
                secondary={`${product.scans} scans • ESG: ${product.esgScore}`}
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
  
  if (!analyticsData) return null;
  
  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Analytics
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Análise de performance e métricas ESG
          </Typography>
        </Box>
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Período</InputLabel>
          <Select
            value={selectedPeriod}
            onChange={handlePeriodChange}
            label="Período"
          >
            <MenuItem value="7d">7 dias</MenuItem>
            <MenuItem value="30d">30 dias</MenuItem>
            <MenuItem value="90d">90 dias</MenuItem>
            <MenuItem value="1y">1 ano</MenuItem>
          </Select>
        </FormControl>
      </Box>
      
      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={selectedTab} onChange={handleTabChange}>
          <Tab label="Visão Geral" />
          <Tab label="Performance" />
          <Tab label="ESG" />
          <Tab label="Produtos" />
        </Tabs>
      </Box>
      
      {/* Conteúdo baseado na tab selecionada */}
      {selectedTab === 0 && (
        <Grid container spacing={3}>
          {/* Métricas principais */}
          <Grid item xs={12} md={3}>
            {renderMetric('Total de Scans', analyticsData.metrics.totalScans, 12.5, <Analytics />)}
          </Grid>
          <Grid item xs={12} md={3}>
            {renderMetric('Taxa de Sucesso', `${analyticsData.metrics.successRate.toFixed(1)}%`, 8.2, <Speed />)}
          </Grid>
          <Grid item xs={12} md={3}>
            {renderMetric('Score ESG', analyticsData.metrics.esgScore.toFixed(1), 5.7, <Eco />)}
          </Grid>
          <Grid item xs={12} md={3}>
            {renderMetric('Receita Total', `R$ ${analyticsData.metrics.totalRevenue.toFixed(2)}`, -2.1, <TrendingUp />)}
          </Grid>
          
          {/* Gráficos */}
          <Grid item xs={12} md={8}>
            {renderChart('Evolução de Scans', analyticsData.trends.scans)}
          </Grid>
          <Grid item xs={12} md={4}>
            {renderESGBreakdown()}
          </Grid>
        </Grid>
      )}
      
      {selectedTab === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            {renderChart('Performance de Scans', analyticsData.trends.scans)}
          </Grid>
          <Grid item xs={12} md={6}>
            {renderChart('Tempo Médio de Scan', [2.5, 2.3, 2.1, 2.0, 1.9, 1.8, 1.7])}
          </Grid>
        </Grid>
      )}
      
      {selectedTab === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            {renderChart('Evolução ESG', analyticsData.trends.esg)}
          </Grid>
          <Grid item xs={12} md={6}>
            {renderESGBreakdown()}
          </Grid>
        </Grid>
      )}
      
      {selectedTab === 3 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            {renderTopProducts()}
          </Grid>
          <Grid item xs={12} md={6}>
            {renderChart('Receita por Produto', analyticsData.trends.revenue)}
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default Analytics;