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
  Divider
} from '@mui/material';
import {
  Send as SendIcon,
  Psychology as PsychologyIcon,
  Insights as InsightsIcon,
  TrendingUp as TrendingUpIcon,
  EmojiEmotions as EmojiIcon,
  Lightbulb as LightbulbIcon,
  Speed as SpeedIcon
} from '@mui/icons-material';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'agent';
  timestamp: Date;
  emotional_state?: string;
  confidence?: number;
  insights?: SymbioticInsight[];
}

interface SymbioticInsight {
  type: string;
  description: string;
  confidence: number;
  source: string;
  actionable: boolean;
}

interface SymbioticAgentProps {
  userId: string;
  onLearning?: (data: any) => void;
  onOptimization?: (data: any) => void;
}

const SymbioticAgent: React.FC<SymbioticAgentProps> = ({
  userId,
  onLearning,
  onOptimization
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [emotionalState, setEmotionalState] = useState('neutral');
  const [confidence, setConfidence] = useState(0);
  const [symbioticInsights, setSymbioticInsights] = useState<SymbioticInsight[]>([]);
  const [learningProgress, setLearningProgress] = useState(0);
  const [agentStatus, setAgentStatus] = useState('active');
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/symbiotic-agent/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          text: inputText,
          user_id: userId,
          context: {
            emotional_state: emotionalState,
            learning_progress: learningProgress
          }
        })
      });

      const data = await response.json();

      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response.result || data.response.tool_used,
        sender: 'agent',
        timestamp: new Date(),
        emotional_state: data.emotional_state,
        confidence: data.confidence,
        insights: data.symbiotic_insights
      };

      setMessages(prev => [...prev, agentMessage]);
      setEmotionalState(data.emotional_state);
      setConfidence(data.confidence);
      setSymbioticInsights(data.symbiotic_insights || []);

      // Processar dados de aprendizado
      if (data.learning_data && onLearning) {
        onLearning(data.learning_data);
        setLearningProgress(data.learning_data.learning_progress || 0);
      }

    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      const errorMessage: Message = {
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
      default: return '😐';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'error';
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header do Agente Simbiótico */}
      <Paper sx={{ p: 2, mb: 2, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Avatar sx={{ bgcolor: 'white', color: '#667eea' }}>
            <PsychologyIcon />
          </Avatar>
          <Box>
            <Typography variant="h6" sx={{ color: 'white', fontWeight: 'bold' }}>
              Agente Simbiótico Agilizia_AI
            </Typography>
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
              Aprendizado mútuo e evolução contínua
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
          </Box>
        </Box>
        
        {/* Progresso de Aprendizado */}
        <Box sx={{ mt: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <Typography variant="body2" sx={{ color: 'white' }}>
              Progresso de Aprendizado
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

      {/* Insights Simbióticos */}
      {symbioticInsights.length > 0 && (
        <Card sx={{ mb: 2, border: '1px solid #e0e0e0' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              <InsightsIcon color="primary" />
              <Typography variant="h6">Insights Simbióticos</Typography>
            </Box>
            <Grid container spacing={2}>
              {symbioticInsights.map((insight, index) => (
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
                    <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                      Confiança: {Math.round(insight.confidence * 100)}%
                    </Typography>
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
                  bgcolor: message.sender === 'user' ? '#e3f2fd' : '#f5f5f5',
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
                </Box>
              </Box>
            </Box>
          ))}
          {isLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
              <Box sx={{ p: 2, bgcolor: '#f5f5f5', borderRadius: 2 }}>
                <Typography variant="body1">Agente está pensando...</Typography>
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
            placeholder="Digite sua mensagem para o agente simbiótico..."
            variant="outlined"
            disabled={isLoading}
          />
          <Button
            variant="contained"
            onClick={sendMessage}
            disabled={!inputText.trim() || isLoading}
            startIcon={<SendIcon />}
            sx={{
              bgcolor: '#667eea',
              '&:hover': { bgcolor: '#5a6fd8' }
            }}
          >
            Enviar
          </Button>
        </Box>
        
        <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Chip
            label="Análise de Checkout"
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
            onClick={() => setInputText('Sugira otimizações para meu sistema')}
            sx={{ cursor: 'pointer' }}
          />
          <Chip
            label="Insights"
            size="small"
            onClick={() => setInputText('Gere insights preditivos')}
            sx={{ cursor: 'pointer' }}
          />
        </Box>
      </Paper>
    </Box>
  );
};

export default SymbioticAgent;
