import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Avatar,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  Paper,
  useTheme,
} from '@mui/material';
import {
  TrendingUp,
  ShoppingCart,
  Store,
  Scanner,
  Eco,
  Speed,
  Security,
  Analytics,
} from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { fetchProductsStart } from '../store/slices/productSlice';
import { fetchESGStart } from '../store/slices/esgSlice';

// Tipos
interface MetricCard {
  title: string;
  value: string | number;
  change: number;
  icon: React.ReactNode;
  color: string;
}

interface RecentActivity {
  id: string;
  type: 'scan' | 'purchase' | 'esg' | 'payment';
  description: string;
  timestamp: string;
  icon: React.ReactNode;
}

// Componente Dashboard
const Dashboard: React.FC = () => {
  // Hooks
  const theme = useTheme();
  const dispatch = useDispatch();
  
  // Redux state
  const { products, loading: productsLoading } = useSelector((state: RootState) => state.product);
  const { currentScore, loading: esgLoading } = useSelector((state: RootState) => state.esg);
  const { totalItems, totalAmount, averageESGScore } = useSelector((state: RootState) => state.cart);
  const { totalScanned, successRate } = useSelector((state: RootState) => state.scanner);
  
  // Local state
  const [recentActivities, setRecentActivities] = useState<RecentActivity[]>([]);
  
  // Effects
  useEffect(() => {
    // Carregar dados iniciais
    dispatch(fetchProductsStart());
    dispatch(fetchESGStart());
    
    // Simular atividades recentes
    setRecentActivities([
      {
        id: '1',
        type: 'scan',
        description: 'Produto escaneado: Leite Orgânico',
        timestamp: '2 min atrás',
        icon: <Scanner />,
      },
      {
        id: '2',
        type: 'purchase',
        description: 'Compra finalizada: R$ 45,90',
        timestamp: '15 min atrás',
        icon: <ShoppingCart />,
      },
      {
        id: '3',
        type: 'esg',
        description: 'Score ESG atualizado: 8.5',
        timestamp: '1 hora atrás',
        icon: <Eco />,
      },
    ]);
  }, [dispatch]);
  
  // Métricas principais
  const metrics: MetricCard[] = [
    {
      title: 'Produtos Escaneados',
      value: totalScanned,
      change: 12.5,
      icon: <Scanner />,
      color: theme.palette.primary.main,
    },
    {
      title: 'Taxa de Sucesso',
      value: `${(successRate * 100).toFixed(1)}%`,
      change: 8.2,
      icon: <Speed />,
      color: theme.palette.success.main,
    },
    {
      title: 'Score ESG',
      value: currentScore?.overall?.toFixed(1) || '0.0',
      change: 5.7,
      icon: <Eco />,
      color: theme.palette.success.main,
    },
    {
      title: 'Valor Total',
      value: `R$ ${totalAmount.toFixed(2)}`,
      change: -2.1,
      icon: <ShoppingCart />,
      color: theme.palette.warning.main,
    },
  ];
  
  // Renderizar métricas
  const renderMetricCard = (metric: MetricCard) => (
    <Card key={metric.title} sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Avatar sx={{ bgcolor: metric.color, mr: 2 }}>
            {metric.icon}
          </Avatar>
          <Box>
            <Typography variant="h6" component="div">
              {metric.value}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {metric.title}
            </Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Chip
            label={`${metric.change > 0 ? '+' : ''}${metric.change}%`}
            color={metric.change > 0 ? 'success' : 'error'}
            size="small"
            sx={{ mr: 1 }}
          />
          <Typography variant="body2" color="text.secondary">
            vs. mês anterior
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
  
  // Renderizar atividades recentes
  const renderRecentActivity = (activity: RecentActivity) => (
    <ListItem key={activity.id} sx={{ px: 0 }}>
      <ListItemAvatar>
        <Avatar sx={{ bgcolor: theme.palette.primary.main }}>
          {activity.icon}
        </Avatar>
      </ListItemAvatar>
      <ListItemText
        primary={activity.description}
        secondary={activity.timestamp}
      />
    </ListItem>
  );
  
  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Visão geral do sistema Agilizia AI
        </Typography>
      </Box>
      
      {/* Métricas principais */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {metrics.map(renderMetricCard)}
      </Grid>
      
      {/* Conteúdo principal */}
      <Grid container spacing={3}>
        {/* Gráfico de performance */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Performance do Sistema
              </Typography>
              <Box sx={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography variant="body1" color="text.secondary">
                  Gráfico de performance será implementado aqui
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Atividades recentes */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Atividades Recentes
              </Typography>
              <List>
                {recentActivities.map(renderRecentActivity)}
              </List>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Status do sistema */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Status do Sistema
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Scanner</Typography>
                  <Typography variant="body2">Online</Typography>
                </Box>
                <LinearProgress variant="determinate" value={100} color="success" />
              </Box>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">ESG Engine</Typography>
                  <Typography variant="body2">Online</Typography>
                </Box>
                <LinearProgress variant="determinate" value={100} color="success" />
              </Box>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Payment Gateway</Typography>
                  <Typography variant="body2">Online</Typography>
                </Box>
                <LinearProgress variant="determinate" value={100} color="success" />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Resumo ESG */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resumo ESG
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Score Geral</Typography>
                  <Typography variant="body2">{currentScore?.overall?.toFixed(1) || '0.0'}</Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={currentScore?.overall ? currentScore.overall * 10 : 0} 
                  color="success" 
                />
              </Box>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Ambiental</Typography>
                  <Typography variant="body2">{currentScore?.environmental?.toFixed(1) || '0.0'}</Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={currentScore?.environmental ? currentScore.environmental * 10 : 0} 
                  color="success" 
                />
              </Box>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Social</Typography>
                  <Typography variant="body2">{currentScore?.social?.toFixed(1) || '0.0'}</Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={currentScore?.social ? currentScore.social * 10 : 0} 
                  color="success" 
                />
              </Box>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Governança</Typography>
                  <Typography variant="body2">{currentScore?.governance?.toFixed(1) || '0.0'}</Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={currentScore?.governance ? currentScore.governance * 10 : 0} 
                  color="success" 
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;