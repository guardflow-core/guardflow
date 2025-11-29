import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Avatar,
  Chip,
  LinearProgress,
  Alert,
  Button,
  IconButton,
  Tooltip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction
} from '@mui/material';
import {
  Psychology as PsychologyIcon,
  Insights as InsightsIcon,
  TrendingUp as TrendingUpIcon,
  Speed as SpeedIcon,
  Eco as EcoIcon,
  Security as SecurityIcon,
  QrCodeScanner as ScannerIcon,
  Payment as PaymentIcon,
  CheckCircle as CheckIcon,
  ExitToApp as ExitIcon,
  Lightbulb as LightbulbIcon,
  Analytics as AnalyticsIcon,
  Timeline as TimelineIcon,
  Assessment as AssessmentIcon,
  Refresh as RefreshIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';
import SEVECARE from '../components/CheckoutSymbioticAgent';

const CheckoutSymbioticAgentPage: React.FC = () => {
  const [userId] = useState('user_' + Math.random().toString(36).substr(2, 9));
  const [sessionId] = useState('session_' + Math.random().toString(36).substr(2, 9));
  const [learningData, setLearningData] = useState<any>(null);
  const [optimizationData, setOptimizationData] = useState<any>(null);
  const [currentStage, setCurrentStage] = useState('entry');
  const [symbeonStats, setSymbeonStats] = useState({
    totalInteractions: 0,
    successRate: 0,
    learningProgress: 0,
    emotionalIntelligence: 0,
    performanceScore: 0
  });

  useEffect(() => {
    // Simular dados iniciais
    setSymbeonStats({
      totalInteractions: 42,
      successRate: 0.87,
      learningProgress: 0.68,
      emotionalIntelligence: 0.92,
      performanceScore: 0.85
    });
  }, []);

  const handleLearning = (data: any) => {
    setLearningData(data);
    setSymbeonStats(prev => ({
      ...prev,
      totalInteractions: data.learning_entries || prev.totalInteractions,
      successRate: data.success_rate || prev.successRate,
      learningProgress: data.learning_progress || prev.learningProgress
    }));
  };

  const handleOptimization = (data: any) => {
    setOptimizationData(data);
  };

  const handleStageChange = (stage: string) => {
    setCurrentStage(stage);
  };

  const getStageIcon = (stage: string) => {
    switch (stage) {
      case 'entry': return <ScannerIcon />;
      case 'scanning': return <ScannerIcon />;
      case 'payment': return <PaymentIcon />;
      case 'completion': return <CheckIcon />;
      case 'exit': return <ExitIcon />;
      default: return <ScannerIcon />;
    }
  };

  const getStageColor = (stage: string) => {
    switch (stage) {
      case 'entry': return 'primary';
      case 'scanning': return 'info';
      case 'payment': return 'warning';
      case 'completion': return 'success';
      case 'exit': return 'secondary';
      default: return 'default';
    }
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Avatar sx={{ bgcolor: 'primary.main' }}>
            <PsychologyIcon />
          </Avatar>
          SEVE-CARE: Checkout Adaptive Responsive Engine
        </Typography>
        <Typography variant="body1" color="text.secondary">
          C.A.R.E. cuida da sua experiência de checkout com inteligência, empatia e adaptação contínua
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Estatísticas SYMBEON */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader
              title="Estatísticas SYMBEON"
              avatar={
                <Avatar sx={{ bgcolor: 'primary.main' }}>
                  <AnalyticsIcon />
                </Avatar>
              }
              action={
                <IconButton>
                  <RefreshIcon />
                </IconButton>
              }
            />
            <CardContent>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Interações Totais</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {symbeonStats.totalInteractions}
                  </Typography>
                </Box>
                <LinearProgress variant="determinate" value={100} />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Taxa de Sucesso</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {Math.round(symbeonStats.successRate * 100)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={symbeonStats.successRate * 100}
                  color="success"
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Progresso de Aprendizado</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {Math.round(symbeonStats.learningProgress * 100)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={symbeonStats.learningProgress * 100}
                  color="info"
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Inteligência Emocional</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {Math.round(symbeonStats.emotionalIntelligence * 100)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={symbeonStats.emotionalIntelligence * 100}
                  color="secondary"
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Score de Performance</Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {Math.round(symbeonStats.performanceScore * 100)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={symbeonStats.performanceScore * 100}
                  color="warning"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Status do Checkout */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader
              title="Status do Checkout"
              avatar={
                <Avatar sx={{ bgcolor: 'success.main' }}>
                  {getStageIcon(currentStage)}
                </Avatar>
              }
            />
            <CardContent>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Estágio Atual
                </Typography>
                <Chip
                  icon={getStageIcon(currentStage)}
                  label={currentStage.toUpperCase()}
                  color={getStageColor(currentStage)}
                  size="large"
                  sx={{ mb: 2 }}
                />
                <Typography variant="body2" color="text.secondary">
                  {currentStage === 'entry' && 'Iniciando processo de checkout'}
                  {currentStage === 'scanning' && 'Escaneando produtos'}
                  {currentStage === 'payment' && 'Processando pagamento'}
                  {currentStage === 'completion' && 'Finalizando compra'}
                  {currentStage === 'exit' && 'Concluindo experiência'}
                </Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Box>
                <Typography variant="h6" gutterBottom>
                  Métricas em Tempo Real
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <ScannerIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary="Itens Escaneados" secondary="0" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <EcoIcon color="success" />
                    </ListItemIcon>
                    <ListItemText primary="Score ESG" secondary="0%" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <SpeedIcon color="info" />
                    </ListItemIcon>
                    <ListItemText primary="Velocidade" secondary="0s" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <SecurityIcon color="error" />
                    </ListItemIcon>
                    <ListItemText primary="Erros" secondary="0" />
                  </ListItem>
                </List>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Insights SYMBEON */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader
              title="Insights SYMBEON"
              avatar={
                <Avatar sx={{ bgcolor: 'info.main' }}>
                  <InsightsIcon />
                </Avatar>
              }
            />
            <CardContent>
              <Alert severity="info" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  <strong>SEVE Core:</strong> Análise geral do checkout
                </Typography>
              </Alert>
              
              <Alert severity="success" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  <strong>SEVE Empathy:</strong> Suporte emocional ativo
                </Typography>
              </Alert>
              
              <Alert severity="warning" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  <strong>SEVE Ethics:</strong> Monitoramento ESG
                </Typography>
              </Alert>
              
              <Alert severity="error" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  <strong>SEVE Sense:</strong> Detecção de anomalias
                </Typography>
              </Alert>

              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Componentes SYMBEON ativos: 4/5
                </Typography>
                <LinearProgress 
                  variant="determinate" 
                  value={80} 
                  color="info"
                  sx={{ mt: 1 }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Agente Simbiótico de Checkout */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <PsychologyIcon color="primary" />
              Interface do Agente Simbiótico
            </Typography>
            <SEVECARE
              userId={userId}
              sessionId={sessionId}
              onLearning={handleLearning}
              onOptimization={handleOptimization}
              onStageChange={handleStageChange}
            />
          </Paper>
        </Grid>

        {/* Dados de Aprendizado */}
        {learningData && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader
                title="Dados de Aprendizado"
                avatar={
                  <Avatar sx={{ bgcolor: 'success.main' }}>
                    <TimelineIcon />
                  </Avatar>
                }
              />
              <CardContent>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Última atualização: {new Date().toLocaleString()}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2">
                    <strong>Interações:</strong> {learningData.learning_entries || 0}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Taxa de Sucesso:</strong> {Math.round((learningData.success_rate || 0) * 100)}%
                  </Typography>
                  <Typography variant="body2">
                    <strong>Estágio Preferido:</strong> {learningData.preferred_stage || 'entry'}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Progresso:</strong> {Math.round((learningData.learning_progress || 0) * 100)}%
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Dados de Otimização */}
        {optimizationData && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader
                title="Otimizações Sugeridas"
                avatar={
                  <Avatar sx={{ bgcolor: 'warning.main' }}>
                    <AssessmentIcon />
                  </Avatar>
                }
              />
              <CardContent>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Baseado na análise SYMBEON
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2">
                    <strong>Tipo:</strong> {optimizationData.optimization_type || 'N/A'}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Prioridade:</strong> {optimizationData.priority || 'N/A'}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Melhoria Esperada:</strong> {optimizationData.expected_improvement || 'N/A'}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Tempo de Implementação:</strong> {optimizationData.implementation_time || 'N/A'}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Container>
  );
};

export default CheckoutSymbioticAgentPage;
