/**
 * GuardFlow ESG Dashboard
 * Dashboard detalhado com métricas ESG avançadas e análises
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  LinearProgress,
  Divider,
  Paper,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Tooltip,
} from '@mui/material';
import {
  EcoIcon,
  TrendingUp,
  TrendingDown,
  Assessment,
  Timeline,
  PieChart,
  BarChart,
  Refresh,
  Download,
  FilterList,
  ExpandMore,
  Info,
  CheckCircle,
  Warning,
  Error,
  Public,
  Group,
  Business,
  Lightbulb,
  Recycling,
  WaterDrop,
  Co2,
  Energy,
  Forest,
  Factory,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  PieChart as RechartsPieChart,
  Cell,
  BarChart as RechartsBarChart,
  Bar,
  RadialBarChart,
  RadialBar,
  Legend,
} from 'recharts';

interface ESGMetrics {
  environmental: {
    score: number;
    carbonFootprint: number;
    waterUsage: number;
    wasteReduction: number;
    renewableEnergy: number;
  };
  social: {
    score: number;
    laborPractices: number;
    communityImpact: number;
    productSafety: number;
    diversity: number;
  };
  governance: {
    score: number;
    transparency: number;
    ethics: number;
    riskManagement: number;
    boardDiversity: number;
  };
  overall: number;
  trend: 'up' | 'down' | 'stable';
  lastUpdated: string;
}

interface ESGTransaction {
  id: string;
  date: string;
  store: string;
  products: number;
  esgScore: number;
  carbonSaved: number;
  category: string;
  value: number;
}

interface ESGChallenge {
  id: string;
  title: string;
  description: string;
  target: number;
  current: number;
  reward: string;
  deadline: string;
  category: 'environmental' | 'social' | 'governance';
}

const ESGDashboard: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  const [timeRange, setTimeRange] = useState('30d');
  const [esgMetrics, setEsgMetrics] = useState<ESGMetrics | null>(null);
  const [transactions, setTransactions] = useState<ESGTransaction[]>([]);
  const [challenges, setChallenges] = useState<ESGChallenge[]>([]);
  const [historicalData, setHistoricalData] = useState<any[]>([]);
  const [categoryData, setCategoryData] = useState<any[]>([]);

  const colors = {
    environmental: '#4CAF50',
    social: '#2196F3',
    governance: '#FF9800',
    primary: '#1976d2',
    success: '#4CAF50',
    warning: '#FF9800',
    error: '#f44336',
  };

  const pieColors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336'];

  useEffect(() => {
    loadESGData();
  }, [timeRange]);

  const loadESGData = useCallback(async () => {
    setLoading(true);
    try {
      // Simular carregamento de dados ESG
      // Em produção, faria chamadas para APIs reais
      
      const mockMetrics: ESGMetrics = {
        environmental: {
          score: 8.2,
          carbonFootprint: 2.4, // tons CO2 saved
          waterUsage: 15.6, // % reduction
          wasteReduction: 23.1, // % reduction
          renewableEnergy: 67.8, // % usage
        },
        social: {
          score: 7.8,
          laborPractices: 8.5,
          communityImpact: 7.2,
          productSafety: 9.1,
          diversity: 6.4,
        },
        governance: {
          score: 8.5,
          transparency: 9.2,
          ethics: 8.8,
          riskManagement: 7.9,
          boardDiversity: 8.1,
        },
        overall: 8.2,
        trend: 'up',
        lastUpdated: new Date().toISOString(),
      };

      const mockTransactions: ESGTransaction[] = Array.from({ length: 20 }, (_, i) => ({
        id: `tx_${i + 1}`,
        date: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        store: ['Loja Centro', 'Loja Shopping', 'Loja Bairro'][Math.floor(Math.random() * 3)],
        products: Math.floor(Math.random() * 15) + 1,
        esgScore: Math.round((Math.random() * 3 + 7) * 10) / 10,
        carbonSaved: Math.round((Math.random() * 2 + 0.5) * 100) / 100,
        category: ['Alimentação', 'Bebidas', 'Limpeza', 'Higiene'][Math.floor(Math.random() * 4)],
        value: Math.round((Math.random() * 200 + 50) * 100) / 100,
      }));

      const mockChallenges: ESGChallenge[] = [
        {
          id: 'ch1',
          title: 'Reduza sua Pegada de Carbono',
          description: 'Economize 10kg de CO₂ este mês',
          target: 10,
          current: 6.8,
          reward: '50 pontos ESG',
          deadline: '2025-11-30',
          category: 'environmental',
        },
        {
          id: 'ch2',
          title: 'Produtos Sustentáveis',
          description: 'Compre 20 produtos com score ESG > 8',
          target: 20,
          current: 14,
          reward: '100 pontos ESG',
          deadline: '2025-11-30',
          category: 'environmental',
        },
        {
          id: 'ch3',
          title: 'Apoie Marcas Éticas',
          description: 'Compre de 5 marcas com certificação social',
          target: 5,
          current: 3,
          reward: '75 pontos ESG',
          deadline: '2025-11-30',
          category: 'social',
        },
      ];

      const mockHistorical = Array.from({ length: 30 }, (_, i) => ({
        date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }),
        environmental: Math.round((7.5 + Math.random() * 1.5) * 10) / 10,
        social: Math.round((7.0 + Math.random() * 1.8) * 10) / 10,
        governance: Math.round((8.0 + Math.random() * 1.0) * 10) / 10,
        overall: Math.round((7.5 + Math.random() * 1.3) * 10) / 10,
      }));

      const mockCategoryData = [
        { name: 'Alimentação Sustentável', value: 35, score: 8.4, transactions: 45 },
        { name: 'Produtos de Limpeza Eco', value: 25, score: 7.8, transactions: 32 },
        { name: 'Cosméticos Naturais', value: 20, score: 8.9, transactions: 28 },
        { name: 'Bebidas Orgânicas', value: 15, score: 8.1, transactions: 19 },
        { name: 'Outros Sustentáveis', value: 5, score: 7.5, transactions: 8 },
      ];

      setEsgMetrics(mockMetrics);
      setTransactions(mockTransactions);
      setChallenges(mockChallenges);
      setHistoricalData(mockHistorical);
      setCategoryData(mockCategoryData);
      
    } catch (err) {
      setError('Erro ao carregar dados ESG');
      console.error('ESG data error:', err);
    } finally {
      setLoading(false);
    }
  }, [timeRange]);

  const getScoreColor = (score: number) => {
    if (score >= 8) return colors.success;
    if (score >= 6) return colors.warning;
    return colors.error;
  };

  const getScoreIcon = (score: number) => {
    if (score >= 8) return <CheckCircle sx={{ color: colors.success }} />;
    if (score >= 6) return <Warning sx={{ color: colors.warning }} />;
    return <Error sx={{ color: colors.error }} />;
  };

  const exportData = () => {
    // Simular exportação de dados
    const data = {
      metrics: esgMetrics,
      transactions: transactions,
      exportDate: new Date().toISOString(),
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `esg-report-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (loading && !esgMetrics) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3, maxWidth: 1400, mx: 'auto' }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box>
            <Typography variant="h4" fontWeight="bold" gutterBottom>
              🌱 Dashboard ESG
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Análise detalhada do impacto ambiental, social e de governança
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Período</InputLabel>
              <Select
                value={timeRange}
                label="Período"
                onChange={(e) => setTimeRange(e.target.value)}
              >
                <MenuItem value="7d">7 dias</MenuItem>
                <MenuItem value="30d">30 dias</MenuItem>
                <MenuItem value="90d">90 dias</MenuItem>
                <MenuItem value="1y">1 ano</MenuItem>
              </Select>
            </FormControl>
            <Button
              variant="outlined"
              startIcon={<Refresh />}
              onClick={loadESGData}
              disabled={loading}
            >
              Atualizar
            </Button>
            <Button
              variant="outlined"
              startIcon={<Download />}
              onClick={exportData}
            >
              Exportar
            </Button>
          </Box>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}
      </Box>

      {esgMetrics && (
        <>
          {/* Cards de métricas principais */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: colors.success, mr: 2 }}>
                      <EcoIcon />
                    </Avatar>
                    <Box>
                      <Typography variant="h4" fontWeight="bold" color={getScoreColor(esgMetrics.overall)}>
                        {esgMetrics.overall.toFixed(1)}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Score ESG Geral
                      </Typography>
                    </Box>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {esgMetrics.trend === 'up' ? (
                      <TrendingUp sx={{ color: colors.success }} />
                    ) : esgMetrics.trend === 'down' ? (
                      <TrendingDown sx={{ color: colors.error }} />
                    ) : (
                      <Timeline sx={{ color: colors.warning }} />
                    )}
                    <Typography variant="caption" color="text.secondary">
                      Tendência {esgMetrics.trend === 'up' ? 'positiva' : esgMetrics.trend === 'down' ? 'negativa' : 'estável'}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: colors.environmental, mr: 2 }}>
                      <Forest />
                    </Avatar>
                    <Box>
                      <Typography variant="h4" fontWeight="bold" color={getScoreColor(esgMetrics.environmental.score)}>
                        {esgMetrics.environmental.score.toFixed(1)}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Ambiental
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    {esgMetrics.environmental.carbonFootprint}t CO₂ economizadas
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: colors.social, mr: 2 }}>
                      <Group />
                    </Avatar>
                    <Box>
                      <Typography variant="h4" fontWeight="bold" color={getScoreColor(esgMetrics.social.score)}>
                        {esgMetrics.social.score.toFixed(1)}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Social
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    Impacto social positivo
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar sx={{ bgcolor: colors.governance, mr: 2 }}>
                      <Business />
                    </Avatar>
                    <Box>
                      <Typography variant="h4" fontWeight="bold" color={getScoreColor(esgMetrics.governance.score)}>
                        {esgMetrics.governance.score.toFixed(1)}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Governança
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    Práticas éticas
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Tabs de conteúdo */}
          <Card>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
                <Tab label="Visão Geral" />
                <Tab label="Análise Detalhada" />
                <Tab label="Transações" />
                <Tab label="Desafios ESG" />
              </Tabs>
            </Box>

            {/* Tab 0: Visão Geral */}
            {activeTab === 0 && (
              <CardContent>
                <Grid container spacing={3}>
                  {/* Gráfico de tendência */}
                  <Grid item xs={12} lg={8}>
                    <Typography variant="h6" gutterBottom>
                      Evolução dos Scores ESG
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={historicalData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="date" />
                          <YAxis domain={[0, 10]} />
                          <RechartsTooltip />
                          <Legend />
                          <Line type="monotone" dataKey="environmental" stroke={colors.environmental} strokeWidth={2} name="Ambiental" />
                          <Line type="monotone" dataKey="social" stroke={colors.social} strokeWidth={2} name="Social" />
                          <Line type="monotone" dataKey="governance" stroke={colors.governance} strokeWidth={2} name="Governança" />
                          <Line type="monotone" dataKey="overall" stroke={colors.primary} strokeWidth={3} name="Geral" />
                        </LineChart>
                      </ResponsiveContainer>
                    </Box>
                  </Grid>

                  {/* Distribuição por categoria */}
                  <Grid item xs={12} lg={4}>
                    <Typography variant="h6" gutterBottom>
                      Compras por Categoria
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <RechartsPieChart>
                          <Pie
                            data={categoryData}
                            cx="50%"
                            cy="50%"
                            outerRadius={80}
                            fill="#8884d8"
                            dataKey="value"
                            label={({ name, value }) => `${name}: ${value}%`}
                          >
                            {categoryData.map((_, index) => (
                              <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
                            ))}
                          </Pie>
                          <RechartsTooltip />
                        </RechartsPieChart>
                      </ResponsiveContainer>
                    </Box>
                  </Grid>

                  {/* Métricas ambientais detalhadas */}
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      Impacto Ambiental
                    </Typography>
                    <List>
                      <ListItem>
                        <ListItemAvatar>
                          <Avatar sx={{ bgcolor: colors.success }}>
                            <Co2 />
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary="Pegada de Carbono"
                          secondary={`${esgMetrics.environmental.carbonFootprint}t CO₂ economizadas`}
                        />
                      </ListItem>
                      <ListItem>
                        <ListItemAvatar>
                          <Avatar sx={{ bgcolor: colors.primary }}>
                            <WaterDrop />
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary="Uso de Água"
                          secondary={`${esgMetrics.environmental.waterUsage}% redução`}
                        />
                      </ListItem>
                      <ListItem>
                        <ListItemAvatar>
                          <Avatar sx={{ bgcolor: colors.warning }}>
                            <Recycling />
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary="Redução de Resíduos"
                          secondary={`${esgMetrics.environmental.wasteReduction}% menos resíduos`}
                        />
                      </ListItem>
                      <ListItem>
                        <ListItemAvatar>
                          <Avatar sx={{ bgcolor: colors.environmental }}>
                            <Energy />
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary="Energia Renovável"
                          secondary={`${esgMetrics.environmental.renewableEnergy}% do consumo`}
                        />
                      </ListItem>
                    </List>
                  </Grid>

                  {/* Ranking de categorias */}
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      Ranking de Categorias ESG
                    </Typography>
                    <List>
                      {categoryData.map((category, index) => (
                        <ListItem key={category.name}>
                          <ListItemAvatar>
                            <Avatar sx={{ bgcolor: pieColors[index] }}>
                              {index + 1}
                            </Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={category.name}
                            secondary={
                              <Box>
                                <Typography variant="body2" component="span">
                                  Score: {category.score} • {category.transactions} transações
                                </Typography>
                                <LinearProgress
                                  variant="determinate"
                                  value={(category.score / 10) * 100}
                                  sx={{ mt: 1 }}
                                  color={category.score >= 8 ? "success" : category.score >= 6 ? "warning" : "error"}
                                />
                              </Box>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Grid>
                </Grid>
              </CardContent>
            )}

            {/* Tab 1: Análise Detalhada */}
            {activeTab === 1 && (
              <CardContent>
                <Grid container spacing={3}>
                  {/* Análise Ambiental */}
                  <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 2, bgcolor: `${colors.environmental}15` }}>
                      <Typography variant="h6" gutterBottom color={colors.environmental}>
                        <Forest sx={{ mr: 1, verticalAlign: 'middle' }} />
                        Ambiental ({esgMetrics.environmental.score.toFixed(1)})
                      </Typography>
                      
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          Práticas Laborais: {esgMetrics.environmental.carbonFootprint}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={85}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="success"
                        />
                      </Box>

                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          Uso de Água: {esgMetrics.environmental.waterUsage}%
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.environmental.waterUsage * 5}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="primary"
                        />
                      </Box>

                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          Redução de Resíduos: {esgMetrics.environmental.wasteReduction}%
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.environmental.wasteReduction * 4}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="warning"
                        />
                      </Box>

                      <Box>
                        <Typography variant="body2" gutterBottom>
                          Energia Renovável: {esgMetrics.environmental.renewableEnergy}%
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.environmental.renewableEnergy}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="success"
                        />
                      </Box>
                    </Paper>
                  </Grid>

                  {/* Análise Social */}
                  <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 2, bgcolor: `${colors.social}15` }}>
                      <Typography variant="h6" gutterBottom color={colors.social}>
                        <Group sx={{ mr: 1, verticalAlign: 'middle' }} />
                        Social ({esgMetrics.social.score.toFixed(1)})
                      </Typography>
                      
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          Práticas Laborais: {esgMetrics.social.laborPractices}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.social.laborPractices * 10}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="success"
                        />
                      </Box>

                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          Impacto Comunitário: {esgMetrics.social.communityImpact}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.social.communityImpact * 10}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="primary"
                        />
                      </Box>

                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          Segurança do Produto: {esgMetrics.social.productSafety}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.social.productSafety * 10}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="success"
                        />
                      </Box>

                      <Box>
                        <Typography variant="body2" gutterBottom>
                          Diversidade: {esgMetrics.social.diversity}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.social.diversity * 10}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="warning"
                        />
                      </Box>
                    </Paper>
                  </Grid>

                  {/* Análise de Governança */}
                  <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 2, bgcolor: `${colors.governance}15` }}>
                      <Typography variant="h6" gutterBottom color={colors.governance}>
                        <Business sx={{ mr: 1, verticalAlign: 'middle' }} />
                        Governança ({esgMetrics.governance.score.toFixed(1)})
                      </Typography>
                      
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          Transparência: {esgMetrics.governance.transparency}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.governance.transparency * 10}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="success"
                        />
                      </Box>

                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          Ética: {esgMetrics.governance.ethics}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.governance.ethics * 10}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="success"
                        />
                      </Box>

                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          Gestão de Riscos: {esgMetrics.governance.riskManagement}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.governance.riskManagement * 10}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="primary"
                        />
                      </Box>

                      <Box>
                        <Typography variant="body2" gutterBottom>
                          Diversidade no Conselho: {esgMetrics.governance.boardDiversity}
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={esgMetrics.governance.boardDiversity * 10}
                          sx={{ height: 6, borderRadius: 3 }}
                          color="success"
                        />
                      </Box>
                    </Paper>
                  </Grid>

                  {/* Gráfico de barras comparativo */}
                  <Grid item xs={12}>
                    <Typography variant="h6" gutterBottom>
                      Comparativo de Dimensões ESG
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <RechartsBarChart
                          data={[
                            { name: 'Ambiental', score: esgMetrics.environmental.score },
                            { name: 'Social', score: esgMetrics.social.score },
                            { name: 'Governança', score: esgMetrics.governance.score },
                          ]}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" />
                          <YAxis domain={[0, 10]} />
                          <RechartsTooltip />
                          <Bar dataKey="score" fill={colors.primary} />
                        </RechartsBarChart>
                      </ResponsiveContainer>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            )}

            {/* Tab 2: Transações */}
            {activeTab === 2 && (
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Histórico de Transações ESG
                </Typography>
                
                <TableContainer component={Paper} sx={{ mt: 2 }}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Data</TableCell>
                        <TableCell>Loja</TableCell>
                        <TableCell align="center">Produtos</TableCell>
                        <TableCell align="center">Score ESG</TableCell>
                        <TableCell align="center">CO₂ Economizado</TableCell>
                        <TableCell>Categoria</TableCell>
                        <TableCell align="right">Valor</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {transactions.slice(0, 10).map((transaction) => (
                        <TableRow key={transaction.id}>
                          <TableCell>{new Date(transaction.date).toLocaleDateString('pt-BR')}</TableCell>
                          <TableCell>{transaction.store}</TableCell>
                          <TableCell align="center">{transaction.products}</TableCell>
                          <TableCell align="center">
                            <Chip
                              label={transaction.esgScore.toFixed(1)}
                              color={transaction.esgScore >= 8 ? "success" : transaction.esgScore >= 6 ? "warning" : "error"}
                              size="small"
                            />
                          </TableCell>
                          <TableCell align="center">{transaction.carbonSaved}kg</TableCell>
                          <TableCell>{transaction.category}</TableCell>
                          <TableCell align="right">R$ {transaction.value.toFixed(2)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            )}

            {/* Tab 3: Desafios ESG */}
            {activeTab === 3 && (
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Desafios ESG Ativos
                </Typography>
                
                <Grid container spacing={2} sx={{ mt: 1 }}>
                  {challenges.map((challenge) => (
                    <Grid item xs={12} md={6} key={challenge.id}>
                      <Card variant="outlined">
                        <CardContent>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                            <Avatar sx={{ 
                              bgcolor: colors[challenge.category], 
                              mr: 2 
                            }}>
                              {challenge.category === 'environmental' ? <EcoIcon /> :
                               challenge.category === 'social' ? <Group /> : <Business />}
                            </Avatar>
                            <Box sx={{ flexGrow: 1 }}>
                              <Typography variant="subtitle1" fontWeight="bold">
                                {challenge.title}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                {challenge.description}
                              </Typography>
                            </Box>
                          </Box>

                          <Box sx={{ mb: 2 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                              <Typography variant="body2">
                                Progresso: {challenge.current}/{challenge.target}
                              </Typography>
                              <Typography variant="body2">
                                {Math.round((challenge.current / challenge.target) * 100)}%
                              </Typography>
                            </Box>
                            <LinearProgress
                              variant="determinate"
                              value={(challenge.current / challenge.target) * 100}
                              sx={{ height: 8, borderRadius: 4 }}
                              color={challenge.current >= challenge.target ? "success" : "primary"}
                            />
                          </Box>

                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <Chip
                              label={challenge.reward}
                              color="primary"
                              size="small"
                              icon={<Lightbulb />}
                            />
                            <Typography variant="caption" color="text.secondary">
                              Até {new Date(challenge.deadline).toLocaleDateString('pt-BR')}
                            </Typography>
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            )}
          </Card>
        </>
      )}
    </Box>
  );
};

export default ESGDashboard;
