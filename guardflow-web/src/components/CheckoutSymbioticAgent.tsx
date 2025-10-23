import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Avatar,
  Chip,
  LinearProgress,
  Alert,
  IconButton,
  Tooltip,
  Card,
  CardContent,
  Grid,
  Divider,
  Stepper,
  Step,
  StepLabel,
  StepContent
} from '@mui/material';
import {
  Send as SendIcon,
  Psychology as PsychologyIcon,
  Insights as InsightsIcon,
  TrendingUp as TrendingUpIcon,
  EmojiEmotions as EmojiIcon,
  Lightbulb as LightbulbIcon,
  Speed as SpeedIcon,
  QrCodeScanner as ScannerIcon,
  Payment as PaymentIcon,
  CheckCircle as CheckIcon,
  ExitToApp as ExitIcon,
  Eco as EcoIcon,
  Security as SecurityIcon
} from '@mui/icons-material';

interface CheckoutMessage {
  id: string;
  text: string;
  sender: 'user' | 'agent';
  timestamp: Date;
  emotional_state?: string;
  confidence?: number;
  symbeon_component?: string;
  insights?: CheckoutInsight[];
}

interface CheckoutInsight {
  type: string;
  description: string;
  confidence: number;
  symbeon_component: string;
  actionable: boolean;
  priority: string;
  emotional_impact: string;
}

interface SEVECAREProps {
  userId: string;
  sessionId: string;
  onLearning?: (data: any) => void;
  onOptimization?: (data: any) => void;
  onStageChange?: (stage: string) => void;
}

const SEVECARE: React.FC<SEVECAREProps> = ({
  userId,
  sessionId,
  onLearning,
  onOptimization,
  onStageChange
}) => {
  const [messages, setMessages] = useState<CheckoutMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [emotionalState, setEmotionalState] = useState('confident');
  const [confidence, setConfidence] = useState(0);
  const [symbeonComponent, setSymbeonComponent] = useState('seve_core');
  const [checkoutInsights, setCheckoutInsights] = useState<CheckoutInsight[]>([]);
  const [currentStage, setCurrentStage] = useState('entry');
  const [checkoutMetrics, setCheckoutMetrics] = useState({
    scanCount: 0,
    totalItems: 0,
    esgScore: 0,
    checkoutSpeed: 0,
    errorCount: 0
  });
  const [learningProgress, setLearningProgress] = useState(0);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: CheckoutMessage = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/care/checkout-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          text: inputText,
          user_id: userId,
          session_id: sessionId,
          stage: currentStage,
          scan_count: checkoutMetrics.scanCount,
          total_items: checkoutMetrics.totalItems,
          esg_score: checkoutMetrics.esgScore,
          checkout_speed: checkoutMetrics.checkoutSpeed,
          error_count: checkoutMetrics.errorCount
        })
      });

      const data = await response.json();

      const agentMessage: CheckoutMessage = {
        id: (Date.now() + 1).toString(),
        text: data.response.response || data.response.guidance || 'Entendi sua solicitação',
        sender: 'agent',
        timestamp: new Date(),
        emotional_state: data.emotional_state,
        confidence: data.confidence,
        symbeon_component: data.symbeon_component,
        insights: data.checkout_insights
      };

      setMessages(prev => [...prev, agentMessage]);
      setEmotionalState(data.emotional_state);
      setConfidence(data.confidence);
      setSymbeonComponent(data.symbeon_component);
      setCheckoutInsights(data.checkout_insights || []);

      // Processar dados de aprendizado
      if (data.learning_data && onLearning) {
        onLearning(data.learning_data);
        setLearningProgress(data.learning_data.learning_progress || 0);
      }

      // Atualizar métricas se fornecidas
      if (data.symbeon_analysis?.analysis) {
        const analysis = data.symbeon_analysis.analysis;
        if (analysis.scan_count !== undefined) {
          setCheckoutMetrics(prev => ({ ...prev, scanCount: analysis.scan_count }));
        }
        if (analysis.esg_score !== undefined) {
          setCheckoutMetrics(prev => ({ ...prev, esgScore: analysis.esg_score }));
        }
      }

    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      const errorMessage: CheckoutMessage = {
        id: (Date.now() + 1).toString(),
        text: 'Desculpe, ocorreu um erro. Tente novamente.',
        sender: 'agent',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const getEmotionalIcon = (state: string) => {
    switch (state) {
      case 'frustrated': return '😤';
      case 'excited': return '🤩';
      case 'confused': return '😕';
      case 'satisfied': return '😊';
      case 'anxious': return '😰';
      case 'confident': return '😌';
      default: return '😐';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'error';
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

  const getSymbeonComponentColor = (component: string) => {
    switch (component) {
      case 'seve_core': return 'primary';
      case 'seve_empathy': return 'secondary';
      case 'seve_ethics': return 'success';
      case 'seve_vision': return 'warning';
      case 'seve_sense': return 'error';
      default: return 'default';
    }
  };

  const stages = [
    { label: 'Entrada', value: 'entry' },
    { label: 'Escaneamento', value: 'scanning' },
    { label: 'Pagamento', value: 'payment' },
    { label: 'Conclusão', value: 'completion' },
    { label: 'Saída', value: 'exit' }
  ];

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header do Agente Simbiótico de Checkout */}
      <Paper sx={{ p: 2, mb: 2, background: 'linear-gradient(135deg, #4caf50 0%, #2e7d32 100%)' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Avatar sx={{ bgcolor: 'white', color: '#4caf50' }}>
            <PsychologyIcon />
          </Avatar>
          <Box>
            <Typography variant="h6" sx={{ color: 'white', fontWeight: 'bold' }}>
              SEVE-CARE: Checkout Adaptive Responsive Engine
            </Typography>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
              C.A.R.E. cuida da sua experiência de checkout com inteligência, empatia e adaptação contínua
            </Typography>
          </Box>
          <Box sx={{ ml: 'auto', display: 'flex', gap: 1 }}>
            <Chip
              icon={<EmojiIcon />}
              label={`${getEmotionalIcon(emotionalState)} ${emotionalState}`}
              size="small"
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
            />
            <Chip
              icon={<SpeedIcon />}
              label={`${Math.round(confidence * 100)}% confiança`}
              size="small"
              color={getConfidenceColor(confidence)}
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
            />
            <Chip
              label={symbeonComponent}
              size="small"
              color={getSymbeonComponentColor(symbeonComponent)}
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
            />
          </Box>
        </Box>
        
        {/* Stepper do Checkout */}
        <Box sx={{ mt: 2 }}>
          <Stepper activeStep={stages.findIndex(s => s.value === currentStage)} alternativeLabel>
            {stages.map((stage) => (
              <Step key={stage.value}>
                <StepLabel
                  icon={getStageIcon(stage.value)}
                  sx={{ color: 'white' }}
                >
                  {stage.label}
                </StepLabel>
              </Step>
            ))}
          </Stepper>
        </Box>
        
        {/* Métricas do Checkout */}
        <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
          <Chip
            icon={<ScannerIcon />}
            label={`${checkoutMetrics.scanCount} itens`}
            size="small"
            sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
          />
          <Chip
            icon={<EcoIcon />}
            label={`ESG: ${Math.round(checkoutMetrics.esgScore * 100)}%`}
            size="small"
            sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
          />
          <Chip
            icon={<SpeedIcon />}
            label={`${checkoutMetrics.checkoutSpeed}s`}
            size="small"
            sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
          />
          {checkoutMetrics.errorCount > 0 && (
            <Chip
              icon={<SecurityIcon />}
              label={`${checkoutMetrics.errorCount} erros`}
              size="small"
              color="error"
              sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
            />
          )}
        </Box>
        
        {/* Progresso de Aprendizado */}
        <Box sx={{ mt: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <Typography variant="body2" sx={{ color: 'white' }}>
              Progresso de Aprendizado SYMBEON
            </Typography>
            <Typography variant="body2" sx={{ color: 'white', ml: 'auto' }}>
              {Math.round(learningProgress * 100)}%
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={learningProgress * 100}
            sx={{
              height: 6,
              borderRadius: 3,
              bgcolor: 'rgba(255,255,255,0.2)',
              '& .MuiLinearProgress-bar': {
                bgcolor: 'white'
              }
            }}
          />
        </Box>
      </Paper>

      {/* Insights de Checkout */}
      {checkoutInsights.length > 0 && (
        <Card sx={{ mb: 2, border: '1px solid #e0e0e0' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              <InsightsIcon color="primary" />
              <Typography variant="h6">Insights SYMBEON de Checkout</Typography>
            </Box>
            <Grid container spacing={2}>
              {checkoutInsights.map((insight, index) => (
                <Grid item xs={12} sm={6} key={index}>
                  <Alert
                    severity={insight.actionable ? 'info' : 'success'}
                    icon={<LightbulbIcon />}
                    sx={{ mb: 1 }}
                  >
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                      {insight.type.replace('_', ' ').toUpperCase()}
                    </Typography>
                    <Typography variant="body2">
                      {insight.description}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                      <Chip
                        label={insight.priority}
                        size="small"
                        color={insight.priority === 'high' ? 'error' : 'default'}
                      />
                      <Chip
                        label={`${Math.round(insight.confidence * 100)}%`}
                        size="small"
                        variant="outlined"
                      />
                      <Chip
                        label={insight.symbeon_component}
                        size="small"
                        color={getSymbeonComponentColor(insight.symbeon_component)}
                      />
                    </Box>
                  </Alert>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Área de Mensagens */}
      <Paper sx={{ flex: 1, p: 2, overflow: 'auto', mb: 2 }}>
        <Box sx={{ height: '400px', overflow: 'auto' }}>
          {messages.map((message) => (
            <Box
              key={message.id}
              sx={{
                display: 'flex',
                justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                mb: 2
              }}
            >
              <Box
                sx={{
                  maxWidth: '70%',
                  p: 2,
                  borderRadius: 2,
                  bgcolor: message.sender === 'user' ? '#e8f5e8' : '#f5f5f5',
                  border: message.sender === 'agent' ? '1px solid #e0e0e0' : 'none'
                }}
              >
                <Typography variant="body1">{message.text}</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                  <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                    {message.timestamp.toLocaleTimeString()}
                  </Typography>
                  {message.sender === 'agent' && message.confidence && (
                    <Chip
                      label={`${Math.round(message.confidence * 100)}%`}
                      size="small"
                      color={getConfidenceColor(message.confidence)}
                    />
                  )}
                  {message.emotional_state && (
                    <Chip
                      icon={<EmojiIcon />}
                      label={getEmotionalIcon(message.emotional_state)}
                      size="small"
                    />
                  )}
                  {message.symbeon_component && (
                    <Chip
                      label={message.symbeon_component}
                      size="small"
                      color={getSymbeonComponentColor(message.symbeon_component)}
                    />
                  )}
                </Box>
              </Box>
            </Box>
          ))}
          {isLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
              <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 2 }}>
                <Typography variant="body1">Agente SYMBEON está analisando...</Typography>
                <LinearProgress sx={{ mt: 1 }} />
              </Box>
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>
      </Paper>

      {/* Área de Input */}
      <Paper sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-end' }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Converse com o agente SYMBEON sobre seu checkout..."
            variant="outlined"
            disabled={isLoading}
          />
          <Button
            variant="contained"
            onClick={sendMessage}
            disabled={!inputText.trim() || isLoading}
            startIcon={<SendIcon />}
            sx={{
              bgcolor: '#4caf50',
              '&:hover': { bgcolor: '#388e3c' }
            }}
          >
            Enviar
          </Button>
        </Box>
        
        <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Chip
            label="Análise de Performance"
            size="small"
            onClick={() => setInputText('Analise a performance do meu checkout')}
            sx={{ cursor: 'pointer' }}
          />
          <Chip
            label="Score ESG"
            size="small"
            onClick={() => setInputText('Como está meu score ESG?')}
            sx={{ cursor: 'pointer' }}
          />
          <Chip
            label="Otimizações"
            size="small"
            onClick={() => setInputText('Sugira otimizações para meu checkout')}
            sx={{ cursor: 'pointer' }}
          />
          <Chip
            label="Suporte Emocional"
            size="small"
            onClick={() => setInputText('Preciso de ajuda emocional')}
            sx={{ cursor: 'pointer' }}
          />
          <Chip
            label="Detecção de Fraude"
            size="small"
            onClick={() => setInputText('Verifique se há anomalias')}
            sx={{ cursor: 'pointer' }}
          />
        </Box>
      </Paper>
    </Box>
  );
};

export default SEVECARE;