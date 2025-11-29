import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  Alert,
  Button,
  Divider,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Psychology as PsychologyIcon,
  Insights as InsightsIcon,
  TrendingUp as TrendingUpIcon,
  EmojiEmotions as EmojiIcon,
  Lightbulb as LightbulbIcon,
  Speed as SpeedIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  Share as ShareIcon
} from '@mui/icons-material';
import SymbioticAgent from '../components/SymbioticAgent';

interface SymbioticSummary {
  user_profile: {
    learning_level: string;
    emotional_state: string;
    interaction_count: number;
    goals: string[];
    pain_points: string[];
    success_patterns: string[];
    preferences: Record<string, any>;
  };
  system_context: {
    performance: Record<string, any>;
    esg_score: number;
    health: Record<string, any>;
  };
  symbiotic_insights: Array<{
    type: string;
    description: string;
    confidence: number;
    actionable: boolean;
  }>;
  learning_recommendations: Array<{
    recommendation_type: string;
    description: string;
    priority: string;
    actionable: boolean;
    confidence: number;
  }>;
}

const SymbioticAgentPage: React.FC = () => {
  const [summary, setSummary] = useState<SymbioticSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userId] = useState('user_' + Date.now()); // Simulação de ID do usuário

  useEffect(() => {
    loadSymbioticSummary();
  }, []);

  const loadSymbioticSummary = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/v1/symbiotic-agent/summary/${userId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Erro ao carregar resumo simbiótico');
      }

      const data = await response.json();
      setSummary(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  const handleLearning = (data: any) => {
    console.log('Dados de aprendizado:', data);
    // Atualizar progresso de aprendizado
    loadSymbioticSummary();
  };

  const handleOptimization = (data: any) => {
    console.log('Dados de otimização:', data);
    // Processar sugestões de otimização
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'default';
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

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
          <LinearProgress sx={{ width: '100%' }} />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={loadSymbioticSummary}>
          Tentar Novamente
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <PsychologyIcon sx={{ fontSize: 40, color: '#667eea' }} />
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#333' }}>
              Agente Simbiótico Agilizia_AI
            </Typography>
            <Typography variant="subtitle1" sx={{ color: '#666' }}>
              Aprendizado mútuo e evolução contínua entre usuário e sistema
            </Typography>
          </Box>
          <Box sx={{ ml: 'auto', display: 'flex', gap: 1 }}>
            <Tooltip title="Atualizar dados">
              <IconButton onClick={loadSymbioticSummary}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Exportar relatório">
              <IconButton>
                <DownloadIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Compartilhar">
              <IconButton>
                <ShareIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* Resumo do Perfil do Usuário */}
        {summary && (
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <EmojiIcon color="primary" />
                  Perfil do Usuário
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Estado Emocional
                  </Typography>
                  <Chip
                    icon={<EmojiIcon />}
                    label={`${getEmotionalIcon(summary.user_profile.emotional_state)} ${summary.user_profile.emotional_state}`}
                    color="primary"
                    variant="outlined"
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Nível de Aprendizado
                  </Typography>
                  <Chip
                    label={summary.user_profile.learning_level}
                    color="secondary"
                    variant="outlined"
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Interações
                  </Typography>
                  <Typography variant="h6" sx={{ color: 'primary.main' }}>
                    {summary.user_profile.interaction_count}
                  </Typography>
                </Box>

                <Divider sx={{ my: 2 }} />

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Metas
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {summary.user_profile.goals.map((goal, index) => (
                      <Chip key={index} label={goal} size="small" />
                    ))}
                  </Box>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Pontos de Dor
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {summary.user_profile.pain_points.map((pain, index) => (
                      <Chip key={index} label={pain} size="small" color="error" />
                    ))}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Contexto do Sistema */}
        {summary && (
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <SpeedIcon color="primary" />
                  Contexto do Sistema
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Performance do Checkout
                  </Typography>
                  <Typography variant="h6" sx={{ color: 'primary.main' }}>
                    {summary.system_context.performance.checkout_speed}s
                  </Typography>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Score ESG
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LinearProgress
                      variant="determinate"
                      value={summary.system_context.esg_score * 100}
                      sx={{ flex: 1, height: 8, borderRadius: 4 }}
                    />
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                      {Math.round(summary.system_context.esg_score * 100)}%
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Taxa de Erro
                  </Typography>
                  <Typography variant="h6" sx={{ color: 'error.main' }}>
                    {summary.system_context.performance.error_rate}%
                  </Typography>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Satisfação do Usuário
                  </Typography>
                  <Typography variant="h6" sx={{ color: 'success.main' }}>
                    {summary.system_context.performance.user_satisfaction}/5
                  </Typography>
                </Box>

                <Divider sx={{ my: 2 }} />

                <Box>
                  <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
                    Status do Sistema
                  </Typography>
                  <Chip
                    label={summary.system_context.health.status}
                    color={summary.system_context.health.status === 'healthy' ? 'success' : 'error'}
                    variant="outlined"
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Insights Simbióticos */}
        {summary && (
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <InsightsIcon color="primary" />
                  Insights Simbióticos
                </Typography>
                
                {summary.symbiotic_insights.map((insight, index) => (
                  <Alert
                    key={index}
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
                ))}

                {summary.symbiotic_insights.length === 0 && (
                  <Typography variant="body2" sx={{ color: 'text.secondary', textAlign: 'center', py: 2 }}>
                    Nenhum insight disponível no momento
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Recomendações de Aprendizado */}
        {summary && summary.learning_recommendations.length > 0 && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <TrendingUpIcon color="primary" />
                  Recomendações de Aprendizado
                </Typography>
                
                <Grid container spacing={2}>
                  {summary.learning_recommendations.map((recommendation, index) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                      <Alert
                        severity={getPriorityColor(recommendation.priority) as any}
                        sx={{ height: '100%' }}
                      >
                        <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                          {recommendation.recommendation_type.replace('_', ' ').toUpperCase()}
                        </Typography>
                        <Typography variant="body2">
                          {recommendation.description}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                          <Chip
                            label={recommendation.priority}
                            size="small"
                            color={getPriorityColor(recommendation.priority)}
                          />
                          <Chip
                            label={`${Math.round(recommendation.confidence * 100)}%`}
                            size="small"
                            variant="outlined"
                          />
                        </Box>
                      </Alert>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Interface do Agente Simbiótico */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <PsychologyIcon color="primary" />
                Chat com o Agente Simbiótico
              </Typography>
              
              <SymbioticAgent
                userId={userId}
                onLearning={handleLearning}
                onOptimization={handleOptimization}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default SymbioticAgentPage;
