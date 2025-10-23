import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Chip,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
  IconButton,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  useTheme,
} from '@mui/material';
import {
  CheckCircle,
  Error,
  Warning,
  Info,
  Refresh,
  Download,
  FilterList,
  Timeline,
  Speed,
  Memory,
  Storage,
  NetworkCheck,
  Security,
  Api,
  Database,
  Cloud,
} from '@mui/icons-material';

// Tipos
interface ServiceStatus {
  id: string;
  name: string;
  status: 'online' | 'offline' | 'degraded' | 'maintenance';
  uptime: number;
  responseTime: number;
  lastCheck: string;
  description: string;
  icon: React.ReactNode;
}

interface LogEntry {
  id: string;
  timestamp: string;
  level: 'info' | 'warning' | 'error' | 'debug';
  service: string;
  message: string;
  details?: string;
}

interface SystemMetrics {
  cpu: number;
  memory: number;
  disk: number;
  network: number;
  database: number;
  api: number;
}

// Componente Monitoring
const Monitoring: React.FC = () => {
  // Hooks
  const theme = useTheme();
  
  // Local state
  const [services, setServices] = useState<ServiceStatus[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [metrics, setMetrics] = useState<SystemMetrics>({
    cpu: 0,
    memory: 0,
    disk: 0,
    network: 0,
    database: 0,
    api: 0,
  });
  const [selectedService, setSelectedService] = useState('all');
  const [selectedLevel, setSelectedLevel] = useState('all');
  const [autoRefresh, setAutoRefresh] = useState(true);
  
  // Effects
  useEffect(() => {
    // Simular dados de serviços
    setServices([
      {
        id: '1',
        name: 'API Gateway',
        status: 'online',
        uptime: 99.9,
        responseTime: 45,
        lastCheck: '2024-01-20T10:30:00Z',
        description: 'Gateway principal da API',
        icon: <Api />,
      },
      {
        id: '2',
        name: 'Database',
        status: 'online',
        uptime: 99.8,
        responseTime: 12,
        lastCheck: '2024-01-20T10:30:00Z',
        description: 'Banco de dados PostgreSQL',
        icon: <Database />,
      },
      {
        id: '3',
        name: 'Redis Cache',
        status: 'online',
        uptime: 99.9,
        responseTime: 2,
        lastCheck: '2024-01-20T10:30:00Z',
        description: 'Cache Redis para sessões',
        icon: <Memory />,
      },
      {
        id: '4',
        name: 'Scanner Service',
        status: 'degraded',
        uptime: 95.2,
        responseTime: 120,
        lastCheck: '2024-01-20T10:30:00Z',
        description: 'Serviço de reconhecimento de produtos',
        icon: <Speed />,
      },
      {
        id: '5',
        name: 'Payment Gateway',
        status: 'online',
        uptime: 99.7,
        responseTime: 89,
        lastCheck: '2024-01-20T10:30:00Z',
        description: 'Gateway de pagamentos',
        icon: <Security />,
      },
      {
        id: '6',
        name: 'ESG Engine',
        status: 'online',
        uptime: 99.5,
        responseTime: 34,
        lastCheck: '2024-01-20T10:30:00Z',
        description: 'Motor de cálculo ESG',
        icon: <Cloud />,
      },
    ]);
    
    // Simular logs
    setLogs([
      {
        id: '1',
        timestamp: '2024-01-20T10:30:00Z',
        level: 'info',
        service: 'API Gateway',
        message: 'Request processada com sucesso',
        details: 'GET /api/v1/products - 200ms',
      },
      {
        id: '2',
        timestamp: '2024-01-20T10:29:45Z',
        level: 'warning',
        service: 'Scanner Service',
        message: 'Tempo de resposta elevado',
        details: 'Response time: 120ms (threshold: 100ms)',
      },
      {
        id: '3',
        timestamp: '2024-01-20T10:29:30Z',
        level: 'error',
        service: 'Payment Gateway',
        message: 'Falha na comunicação com Mercado Pago',
        details: 'Connection timeout after 30s',
      },
      {
        id: '4',
        timestamp: '2024-01-20T10:29:15Z',
        level: 'info',
        service: 'Database',
        message: 'Conexão estabelecida',
        details: 'Pool size: 10/20 connections',
      },
      {
        id: '5',
        timestamp: '2024-01-20T10:29:00Z',
        level: 'debug',
        service: 'ESG Engine',
        message: 'Cálculo ESG executado',
        details: 'Product ID: 12345, Score: 8.5',
      },
    ]);
    
    // Simular métricas do sistema
    setMetrics({
      cpu: 45,
      memory: 67,
      disk: 23,
      network: 89,
      database: 12,
      api: 34,
    });
  }, []);
  
  // Auto refresh
  useEffect(() => {
    if (!autoRefresh) return;
    
    const interval = setInterval(() => {
      // Simular atualização de métricas
      setMetrics(prev => ({
        cpu: Math.max(0, Math.min(100, prev.cpu + (Math.random() - 0.5) * 10)),
        memory: Math.max(0, Math.min(100, prev.memory + (Math.random() - 0.5) * 5)),
        disk: Math.max(0, Math.min(100, prev.disk + (Math.random() - 0.5) * 2)),
        network: Math.max(0, Math.min(100, prev.network + (Math.random() - 0.5) * 15)),
        database: Math.max(0, Math.min(100, prev.database + (Math.random() - 0.5) * 8)),
        api: Math.max(0, Math.min(100, prev.api + (Math.random() - 0.5) * 12)),
      }));
    }, 5000);
    
    return () => clearInterval(interval);
  }, [autoRefresh]);
  
  // Handlers
  const handleRefresh = () => {
    // Simular refresh
    setServices(prev => prev.map(service => ({
      ...service,
      lastCheck: new Date().toISOString(),
    })));
  };
  
  const handleDownloadLogs = () => {
    // Simular download de logs
    const logData = logs.map(log => ({
      timestamp: log.timestamp,
      level: log.level,
      service: log.service,
      message: log.message,
      details: log.details,
    }));
    
    const blob = new Blob([JSON.stringify(logData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `logs_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };
  
  // Renderizar status do serviço
  const renderServiceStatus = (status: string) => {
    const statusConfig = {
      online: { color: 'success', icon: <CheckCircle />, label: 'Online' },
      offline: { color: 'error', icon: <Error />, label: 'Offline' },
      degraded: { color: 'warning', icon: <Warning />, label: 'Degradado' },
      maintenance: { color: 'info', icon: <Info />, label: 'Manutenção' },
    };
    
    const config = statusConfig[status as keyof typeof statusConfig];
    
    return (
      <Chip
        icon={config.icon}
        label={config.label}
        color={config.color as any}
        size="small"
      />
    );
  };
  
  // Renderizar nível do log
  const renderLogLevel = (level: string) => {
    const levelConfig = {
      info: { color: 'info', icon: <Info /> },
      warning: { color: 'warning', icon: <Warning /> },
      error: { color: 'error', icon: <Error /> },
      debug: { color: 'default', icon: <Info /> },
    };
    
    const config = levelConfig[level as keyof typeof levelConfig];
    
    return (
      <Chip
        icon={config.icon}
        label={level.toUpperCase()}
        color={config.color as any}
        size="small"
      />
    );
  };
  
  // Renderizar métrica
  const renderMetric = (title: string, value: number, color: string) => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Typography variant="h4" component="div" sx={{ mr: 2 }}>
            {value.toFixed(1)}%
          </Typography>
          <Box sx={{ flexGrow: 1 }}>
            <LinearProgress
              variant="determinate"
              value={value}
              color={color as any}
              sx={{ height: 8, borderRadius: 4 }}
            />
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
  
  // Renderizar serviço
  const renderService = (service: ServiceStatus) => (
    <Card key={service.id} sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box sx={{ color: theme.palette.primary.main, mr: 2 }}>
            {service.icon}
          </Box>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" component="div">
              {service.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {service.description}
            </Typography>
          </Box>
          {renderServiceStatus(service.status)}
        </Box>
        
        <Grid container spacing={2}>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              Uptime
            </Typography>
            <Typography variant="h6">
              {service.uptime}%
            </Typography>
          </Grid>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              Response Time
            </Typography>
            <Typography variant="h6">
              {service.responseTime}ms
            </Typography>
          </Grid>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              Last Check
            </Typography>
            <Typography variant="body2">
              {new Date(service.lastCheck).toLocaleString()}
            </Typography>
          </Grid>
          <Grid item xs={6} md={3}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <LinearProgress
                variant="determinate"
                value={service.uptime}
                color={service.status === 'online' ? 'success' : 'warning'}
                sx={{ flexGrow: 1, mr: 1 }}
              />
              <Typography variant="body2">
                {service.uptime}%
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
  
  // Renderizar log
  const renderLog = (log: LogEntry) => (
    <TableRow key={log.id}>
      <TableCell>
        {renderLogLevel(log.level)}
      </TableCell>
      <TableCell>
        {log.service}
      </TableCell>
      <TableCell>
        {log.message}
      </TableCell>
      <TableCell>
        {new Date(log.timestamp).toLocaleString()}
      </TableCell>
    </TableRow>
  );
  
  // Filtrar logs
  const filteredLogs = logs.filter(log => {
    if (selectedService !== 'all' && log.service !== selectedService) return false;
    if (selectedLevel !== 'all' && log.level !== selectedLevel) return false;
    return true;
  });
  
  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Monitoramento
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Status dos serviços e logs do sistema
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={handleRefresh}
          >
            Atualizar
          </Button>
          <Button
            variant="outlined"
            startIcon={<Download />}
            onClick={handleDownloadLogs}
          >
            Exportar Logs
          </Button>
        </Box>
      </Box>
      
      {/* Métricas do sistema */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={2}>
          {renderMetric('CPU', metrics.cpu, 'primary')}
        </Grid>
        <Grid item xs={12} md={2}>
          {renderMetric('Memória', metrics.memory, 'secondary')}
        </Grid>
        <Grid item xs={12} md={2}>
          {renderMetric('Disco', metrics.disk, 'success')}
        </Grid>
        <Grid item xs={12} md={2}>
          {renderMetric('Rede', metrics.network, 'warning')}
        </Grid>
        <Grid item xs={12} md={2}>
          {renderMetric('Database', metrics.database, 'error')}
        </Grid>
        <Grid item xs={12} md={2}>
          {renderMetric('API', metrics.api, 'info')}
        </Grid>
      </Grid>
      
      {/* Status dos serviços */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Status dos Serviços
              </Typography>
              {services.map(renderService)}
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resumo
              </Typography>
              <List>
                <ListItem sx={{ px: 0 }}>
                  <ListItemText
                    primary="Serviços Online"
                    secondary={`${services.filter(s => s.status === 'online').length}/${services.length}`}
                  />
                </ListItem>
                <ListItem sx={{ px: 0 }}>
                  <ListItemText
                    primary="Uptime Médio"
                    secondary={`${(services.reduce((sum, s) => sum + s.uptime, 0) / services.length).toFixed(1)}%`}
                  />
                </ListItem>
                <ListItem sx={{ px: 0 }}>
                  <ListItemText
                    primary="Response Time Médio"
                    secondary={`${(services.reduce((sum, s) => sum + s.responseTime, 0) / services.length).toFixed(0)}ms`}
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      {/* Logs */}
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              Logs do Sistema
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Serviço</InputLabel>
                <Select
                  value={selectedService}
                  onChange={(e) => setSelectedService(e.target.value)}
                  label="Serviço"
                >
                  <MenuItem value="all">Todos</MenuItem>
                  {Array.from(new Set(logs.map(log => log.service))).map(service => (
                    <MenuItem key={service} value={service}>{service}</MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Nível</InputLabel>
                <Select
                  value={selectedLevel}
                  onChange={(e) => setSelectedLevel(e.target.value)}
                  label="Nível"
                >
                  <MenuItem value="all">Todos</MenuItem>
                  <MenuItem value="info">Info</MenuItem>
                  <MenuItem value="warning">Warning</MenuItem>
                  <MenuItem value="error">Error</MenuItem>
                  <MenuItem value="debug">Debug</MenuItem>
                </Select>
              </FormControl>
            </Box>
          </Box>
          
          <TableContainer component={Paper} sx={{ maxHeight: 400 }}>
            <Table stickyHeader>
              <TableHead>
                <TableRow>
                  <TableCell>Nível</TableCell>
                  <TableCell>Serviço</TableCell>
                  <TableCell>Mensagem</TableCell>
                  <TableCell>Timestamp</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredLogs.map(renderLog)}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Monitoring;