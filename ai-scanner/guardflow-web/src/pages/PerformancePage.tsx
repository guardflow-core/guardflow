import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  LinearProgress,
  Chip,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Switch,
  FormControlLabel,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress
} from '@mui/material';
import {
  Speed,
  Memory,
  Storage,
  NetworkCheck,
  TrendingUp,
  PlayArrow,
  Stop,
  Refresh,
  Settings,
  Warning,
  CheckCircle,
  Error as ErrorIcon
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

interface PerformanceMetrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  cache_hit_rate: number;
  active_connections: number;
  database_connections: number;
  health_score: number;
  status: string;
  timestamp: string;
}

interface OptimizationAction {
  action_type: string;
  description: string;
  impact_level: string;
  estimated_improvement: number;
  executed: boolean;
  execution_time?: string;
  result?: string;
}

const PerformancePage: React.FC = () => {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  const [metricsHistory, setMetricsHistory] = useState<any[]>([]);
  const [actions, setActions] = useState<OptimizationAction[]>([]);
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [loading, setLoading] = useState(true);
  const [optimizing, setOptimizing] = useState(false);
  const [configDialog, setConfigDialog] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Configurações de monitoramento
  const [monitoringConfig, setMonitoringConfig] = useState({
    interval_seconds: 30,
    cpu_threshold: 80,
    memory_threshold: 85,
    response_time_threshold: 2.0,
    auto_optimize: true
  });

  useEffect(() => {
    loadPerformanceData();
    checkMonitoringStatus();

    // Auto refresh a cada 30 segundos se ativado
    const interval = setInterval(() => {
      if (autoRefresh) {
        loadPerformanceData();
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [autoRefresh]);

  const loadPerformanceData = async () => {
    try {
      // Carregar métricas atuais
      const metricsResponse = await fetch('/api/v1/performance/status');
      if (metricsResponse.ok) {
        const metricsData = await metricsResponse.json();
        setMetrics(metricsData);
      }

      // Carregar histórico
      const historyResponse = await fetch('/api/v1/performance/metrics/history?limit=20');
      if (historyResponse.ok) {
        const historyData = await historyResponse.json();
        setMetricsHistory(historyData.metrics || []);
      }

      // Carregar ações
      const actionsResponse = await fetch('/api/v1/performance/actions/history?limit=10');
      if (actionsResponse.ok) {
        const actionsData = await actionsResponse.json();
        setActions(actionsData.actions || []);
      }

      setLoading(false);
    } catch (error) {
      console.error('Erro ao carregar dados de performance:', error);
      setLoading(false);
    }
  };

  const checkMonitoringStatus = async () => {
    try {
      const response = await fetch('/api/v1/performance/monitoring/status');
      if (response.ok) {
        const data = await response.json();
        setIsMonitoring(data.is_active);
      }
    } catch (error) {
      console.error('Erro ao verificar status do monitoramento:', error);
    }
  };

  const handleStartMonitoring = async () => {
    try {
      const response = await fetch('/api/v1/performance/monitoring/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(monitoringConfig)
      });

      if (response.ok) {
        setIsMonitoring(true);
        loadPerformanceData();
      }
    } catch (error) {
      console.error('Erro ao iniciar monitoramento:', error);
    }
  };

  const handleStopMonitoring = async () => {
    try {
      const response = await fetch('/api/v1/performance/monitoring/stop', {
        method: 'POST'
      });

      if (response.ok) {
        setIsMonitoring(false);
      }
    } catch (error) {
      console.error('Erro ao parar monitoramento:', error);
    }
  };

  const handleOptimize = async () => {
    setOptimizing(true);
    try {
      const response = await fetch('/api/v1/performance/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          level: 'medium',
          target_areas: ['cpu', 'memory', 'cache'],
          force: false
        })
      });

      if (response.ok) {
        await loadPerformanceData();
      }
    } catch (error) {
      console.error('Erro ao otimizar:', error);
    } finally {
      setOptimizing(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return 'success';
      case 'good': return 'info';
      case 'warning': return 'warning';
      case 'critical': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'excellent': return <CheckCircle color="success" />;
      case 'good': return <CheckCircle color="info" />;
      case 'warning': return <Warning color="warning" />;
      case 'critical': return <ErrorIcon color="error" />;
      default: return <Speed />;
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ ml: 2 }}>Carregando dados de performance...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
        <Box display="flex" alignItems="center">
          <Speed sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
          <Typography variant="h4">Performance do Sistema</Typography>
        </Box>
        <Box>
          <FormControlLabel
            control={<Switch checked={autoRefresh} onChange={(e) => setAutoRefresh(e.target.checked)} />}
            label="Auto Refresh"
            sx={{ mr: 2 }}
          />
          <Button
            variant="outlined"
            startIcon={<Settings />}
            onClick={() => setConfigDialog(true)}
            sx={{ mr: 1 }}
          >
            Configurar
          </Button>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={loadPerformanceData}
            sx={{ mr: 1 }}
          >
            Atualizar
          </Button>
          {isMonitoring ? (
            <Button
              variant="contained"
              color="error"
              startIcon={<Stop />}
              onClick={handleStopMonitoring}
              sx={{ mr: 1 }}
            >
              Parar Monitoramento
            </Button>
          ) : (
            <Button
              variant="contained"
              color="success"
              startIcon={<PlayArrow />}
              onClick={handleStartMonitoring}
              sx={{ mr: 1 }}
            >
              Iniciar Monitoramento
            </Button>
          )}
          <Button
            variant="contained"
            color="primary"
            startIcon={<TrendingUp />}
            onClick={handleOptimize}
            disabled={optimizing}
          >
            {optimizing ? 'Otimizando...' : 'Otimizar'}
          </Button>
        </Box>
      </Box>

      {/* Status Geral */}
      {metrics && (
        <Alert
          severity={getStatusColor(metrics.status) as any}
          icon={getStatusIcon(metrics.status)}
          sx={{ mb: 3 }}
        >
          <Typography variant="h6">
            Sistema {metrics.status === 'excellent' ? 'Excelente' : 
                     metrics.status === 'good' ? 'Bom' :
                     metrics.status === 'warning' ? 'Atenção' : 'Crítico'} 
            - Health Score: {metrics.health_score}%
          </Typography>
          <Typography variant="body2">
            Monitoramento: {isMonitoring ? 'Ativo' : 'Inativo'} | 
            Última atualização: {new Date(metrics.timestamp).toLocaleString()}
          </Typography>
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Métricas Principais */}
        {metrics && (
          <>
            <Grid item xs={12} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Speed color="primary" sx={{ mr: 1 }} />
                    <Typography variant="h6">CPU</Typography>
                  </Box>
                  <Typography variant="h4" color={metrics.cpu_usage > 80 ? 'error' : 'primary'}>
                    {metrics.cpu_usage.toFixed(1)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={metrics.cpu_usage}
                    color={metrics.cpu_usage > 80 ? 'error' : 'primary'}
                    sx={{ mt: 1, height: 8, borderRadius: 4 }}
                  />
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Memory color="secondary" sx={{ mr: 1 }} />
                    <Typography variant="h6">Memória</Typography>
                  </Box>
                  <Typography variant="h4" color={metrics.memory_usage > 85 ? 'error' : 'secondary'}>
                    {metrics.memory_usage.toFixed(1)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={metrics.memory_usage}
                    color={metrics.memory_usage > 85 ? 'error' : 'secondary'}
                    sx={{ mt: 1, height: 8, borderRadius: 4 }}
                  />
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Storage color="info" sx={{ mr: 1 }} />
                    <Typography variant="h6">Disco</Typography>
                  </Box>
                  <Typography variant="h4" color="info">
                    {metrics.disk_usage.toFixed(1)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={metrics.disk_usage}
                    color="info"
                    sx={{ mt: 1, height: 8, borderRadius: 4 }}
                  />
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <NetworkCheck color="success" sx={{ mr: 1 }} />
                    <Typography variant="h6">Cache Hit</Typography>
                  </Box>
                  <Typography variant="h4" color="success">
                    {(metrics.cache_hit_rate * 100).toFixed(1)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={metrics.cache_hit_rate * 100}
                    color="success"
                    sx={{ mt: 1, height: 8, borderRadius: 4 }}
                  />
                </CardContent>
              </Card>
            </Grid>
          </>
        )}

        {/* Gráfico de Histórico */}
        <Grid item xs={12} md={8}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Histórico de Performance</Typography>
              {metricsHistory.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={metricsHistory}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="timestamp" 
                      tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                    />
                    <YAxis />
                    <Tooltip 
                      labelFormatter={(value) => new Date(value).toLocaleString()}
                      formatter={(value: number, name: string) => [`${value.toFixed(1)}%`, name]}
                    />
                    <Area type="monotone" dataKey="cpu_usage" stackId="1" stroke="#1976d2" fill="#1976d2" fillOpacity={0.3} name="CPU" />
                    <Area type="monotone" dataKey="memory_usage" stackId="2" stroke="#9c27b0" fill="#9c27b0" fillOpacity={0.3} name="Memória" />
                  </AreaChart>
                </ResponsiveContainer>
              ) : (
                <Typography color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
                  Nenhum dado histórico disponível
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Conexões */}
        <Grid item xs={12} md={4}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Conexões</Typography>
              {metrics && (
                <Box>
                  <Box display="flex" justifyContent="space-between" mb={2}>
                    <Typography>Conexões Ativas:</Typography>
                    <Chip label={metrics.active_connections} color="primary" size="small" />
                  </Box>
                  <Box display="flex" justifyContent="space-between" mb={2}>
                    <Typography>Conexões BD:</Typography>
                    <Chip label={metrics.database_connections} color="secondary" size="small" />
                  </Box>
                  <Box display="flex" justifyContent="space-between">
                    <Typography>Health Score:</Typography>
                    <Chip 
                      label={`${metrics.health_score}%`} 
                      color={metrics.health_score > 80 ? 'success' : metrics.health_score > 60 ? 'warning' : 'error'} 
                      size="small" 
                    />
                  </Box>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Ações de Otimização */}
        <Grid item xs={12}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Histórico de Otimizações</Typography>
              {actions.length > 0 ? (
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Ação</TableCell>
                        <TableCell>Descrição</TableCell>
                        <TableCell>Impacto</TableCell>
                        <TableCell>Melhoria</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Executado em</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {actions.map((action, index) => (
                        <TableRow key={index}>
                          <TableCell>{action.action_type}</TableCell>
                          <TableCell>{action.description}</TableCell>
                          <TableCell>
                            <Chip 
                              label={action.impact_level} 
                              size="small"
                              color={action.impact_level === 'high' ? 'error' : action.impact_level === 'medium' ? 'warning' : 'default'}
                            />
                          </TableCell>
                          <TableCell>{action.estimated_improvement.toFixed(1)}%</TableCell>
                          <TableCell>
                            <Chip 
                              label={action.executed ? 'Executado' : 'Pendente'} 
                              size="small"
                              color={action.executed ? 'success' : 'default'}
                            />
                          </TableCell>
                          <TableCell>
                            {action.execution_time ? new Date(action.execution_time).toLocaleString() : '-'}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
                  Nenhuma otimização executada ainda
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Dialog de Configuração */}
      <Dialog open={configDialog} onClose={() => setConfigDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Configurações de Monitoramento</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <Typography gutterBottom>Intervalo de Monitoramento (segundos):</Typography>
            <input
              type="number"
              value={monitoringConfig.interval_seconds}
              onChange={(e) => setMonitoringConfig({
                ...monitoringConfig,
                interval_seconds: parseInt(e.target.value) || 30
              })}
              style={{ width: '100%', padding: '8px', marginBottom: '16px' }}
            />

            <Typography gutterBottom>Threshold CPU (%):</Typography>
            <input
              type="number"
              value={monitoringConfig.cpu_threshold}
              onChange={(e) => setMonitoringConfig({
                ...monitoringConfig,
                cpu_threshold: parseFloat(e.target.value) || 80
              })}
              style={{ width: '100%', padding: '8px', marginBottom: '16px' }}
            />

            <Typography gutterBottom>Threshold Memória (%):</Typography>
            <input
              type="number"
              value={monitoringConfig.memory_threshold}
              onChange={(e) => setMonitoringConfig({
                ...monitoringConfig,
                memory_threshold: parseFloat(e.target.value) || 85
              })}
              style={{ width: '100%', padding: '8px', marginBottom: '16px' }}
            />

            <FormControlLabel
              control={
                <Switch
                  checked={monitoringConfig.auto_optimize}
                  onChange={(e) => setMonitoringConfig({
                    ...monitoringConfig,
                    auto_optimize: e.target.checked
                  })}
                />
              }
              label="Otimização Automática"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfigDialog(false)}>Cancelar</Button>
          <Button onClick={() => setConfigDialog(false)} variant="contained">Salvar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PerformancePage;
