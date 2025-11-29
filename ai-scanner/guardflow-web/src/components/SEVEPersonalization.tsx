import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  Chip,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Avatar,
  LinearProgress,
  Divider
} from '@mui/material';
import {
  PersonAdd,
  Eco,
  ShoppingCart,
  Psychology,
  TrendingUp,
  Star,
  LocalOffer,
  Security,
  Analytics,
  Verified
} from '@mui/icons-material';

interface SEVEProfile {
  anonymous_id: string;
  esg_affinity: number;
  sustainability_score: number;
  interaction_count: number;
  recommendations: ProductRecommendation[];
  guardpass_suggestion?: GuardPassSuggestion;
}

interface ProductRecommendation {
  sku: string;
  name: string;
  brand: string;
  esg_score: number;
  price: number;
  discount_percentage: number;
  reason: string;
  confidence: number;
  category: string;
}

interface GuardPassSuggestion {
  should_suggest: boolean;
  confidence: number;
  personalized_benefits: string[];
  suggested_tier: string;
  incentive: string;
}

const SEVEPersonalization: React.FC = () => {
  const [seveProfile, setSEVEProfile] = useState<SEVEProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [showGuardPassDialog, setShowGuardPassDialog] = useState(false);
  const [storeSection, setStoreSection] = useState('entrance');

  const steps = [
    'Entrada na Loja',
    'Personalização Inicial', 
    'Recomendações ESG',
    'Ativação do Carrinho',
    'Upgrade GuardPass'
  ];

  const storeSections = [
    { id: 'entrance', name: '🚪 Entrada', icon: '🚪' },
    { id: 'alimentacao', name: '🥗 Alimentação', icon: '🥗' },
    { id: 'limpeza', name: '🧽 Limpeza', icon: '🧽' },
    { id: 'higiene', name: '🧴 Higiene', icon: '🧴' },
    { id: 'bebidas', name: '🥤 Bebidas', icon: '🥤' }
  ];

  const initializeSEVE = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/seve/initialize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          store_id: 'store_demo_001',
          device_type: 'mobile',
          store_section: storeSection,
          interaction_speed: 'medium'
        })
      });

      if (response.ok) {
        const profile = await response.json();
        setSEVEProfile(profile);
        setCurrentStep(1);
      }
    } catch (error) {
      console.error('Erro ao inicializar SEVE:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateSEVEInteraction = async (interactionData: any) => {
    if (!seveProfile) return;

    try {
      const response = await fetch(`/api/v1/seve/update/${seveProfile.anonymous_id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...interactionData,
          current_section: storeSection
        })
      });

      if (response.ok) {
        const updatedProfile = await response.json();
        setSEVEProfile(updatedProfile);
      }
    } catch (error) {
      console.error('Erro ao atualizar SEVE:', error);
    }
  };

  const simulateStoreNavigation = (section: string) => {
    setStoreSection(section);
    if (seveProfile) {
      updateSEVEInteraction({
        viewed_categories: [section],
        current_section: section
      });
      setCurrentStep(2);
    }
  };

  const simulateProductInteraction = (esgProducts: boolean = false) => {
    if (seveProfile) {
      updateSEVEInteraction({
        viewed_esg_products: esgProducts,
        premium_product_views: esgProducts,
        viewed_brands: esgProducts ? ['Organic', 'Native', 'Taeq'] : ['Nestlé', 'Unilever']
      });
      setCurrentStep(3);
    }
  };

  const activateCart = () => {
    setCurrentStep(4);
    if (seveProfile?.guardpass_suggestion?.should_suggest) {
      setTimeout(() => setShowGuardPassDialog(true), 2000);
    }
  };

  const getESGColor = (score: number) => {
    if (score >= 8) return 'success';
    if (score >= 6) return 'warning';
    return 'error';
  };

  const getAffinityLevel = (affinity: number) => {
    if (affinity >= 0.8) return { level: 'Alto', color: 'success' };
    if (affinity >= 0.5) return { level: 'Médio', color: 'warning' };
    return { level: 'Baixo', color: 'error' };
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        🧠 SEVE Personalization Engine
      </Typography>
      
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Jornada do Usuário com Personalização Ética desde a Entrada
      </Typography>

      {/* Stepper da Jornada */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stepper activeStep={currentStep} orientation="horizontal">
            {steps.map((label, index) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {/* Controles de Simulação */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🎮 Simulação da Jornada
              </Typography>

              {currentStep === 0 && (
                <Box>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    Cliente aproxima o celular do portal de entrada
                  </Typography>
                  <Button
                    variant="contained"
                    onClick={initializeSEVE}
                    disabled={loading}
                    startIcon={loading ? <CircularProgress size={20} /> : <PersonAdd />}
                    fullWidth
                  >
                    {loading ? 'Inicializando SEVE...' : 'Inicializar Personalização'}
                  </Button>
                </Box>
              )}

              {currentStep === 1 && (
                <Box>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    Navegação pelas seções da loja
                  </Typography>
                  <Grid container spacing={1}>
                    {storeSections.map((section) => (
                      <Grid item xs={6} key={section.id}>
                        <Button
                          variant={storeSection === section.id ? 'contained' : 'outlined'}
                          onClick={() => simulateStoreNavigation(section.id)}
                          size="small"
                          fullWidth
                        >
                          {section.icon} {section.name.split(' ')[1]}
                        </Button>
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              )}

              {currentStep === 2 && (
                <Box>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    Interação com produtos
                  </Typography>
                  <Button
                    variant="outlined"
                    onClick={() => simulateProductInteraction(false)}
                    sx={{ mb: 1 }}
                    fullWidth
                  >
                    🛒 Produtos Convencionais
                  </Button>
                  <Button
                    variant="contained"
                    color="success"
                    onClick={() => simulateProductInteraction(true)}
                    fullWidth
                  >
                    🌱 Produtos ESG Premium
                  </Button>
                </Box>
              )}

              {currentStep === 3 && (
                <Box>
                  <Typography variant="body2" sx={{ mb: 2 }}>
                    Ativar carrinho inteligente
                  </Typography>
                  <Button
                    variant="contained"
                    onClick={activateCart}
                    startIcon={<ShoppingCart />}
                    fullWidth
                  >
                    🚀 Ativar Carrinho "Agiliza Aí"
                  </Button>
                </Box>
              )}

              {currentStep === 4 && (
                <Box textAlign="center">
                  <Typography variant="h6" color="success.main" sx={{ mb: 1 }}>
                    ✅ Carrinho Ativado!
                  </Typography>
                  <Typography variant="body2">
                    Aguardando sugestão de GuardPass...
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Perfil SEVE */}
        {seveProfile && (
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🧠 Perfil SEVE Anônimo
                </Typography>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    ID: {seveProfile.anonymous_id.substring(0, 8)}...
                  </Typography>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    Afinidade ESG: {(seveProfile.esg_affinity * 100).toFixed(0)}%
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={seveProfile.esg_affinity * 100}
                    color={getAffinityLevel(seveProfile.esg_affinity).color as any}
                  />
                  <Chip 
                    label={getAffinityLevel(seveProfile.esg_affinity).level}
                    color={getAffinityLevel(seveProfile.esg_affinity).color as any}
                    size="small"
                    sx={{ mt: 1 }}
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    Score Sustentabilidade: {(seveProfile.sustainability_score * 100).toFixed(0)}%
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={seveProfile.sustainability_score * 100}
                    color="success"
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Chip 
                    icon={<Analytics />}
                    label={`${seveProfile.interaction_count} interações`}
                    variant="outlined"
                    size="small"
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Recomendações */}
        {seveProfile?.recommendations && seveProfile.recommendations.length > 0 && (
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🎯 Recomendações Personalizadas
                </Typography>

                <List dense>
                  {seveProfile.recommendations.map((rec, index) => (
                    <ListItem key={index} divider>
                      <ListItemIcon>
                        <Eco color={getESGColor(rec.esg_score) as any} />
                      </ListItemIcon>
                      <ListItemText
                        primary={rec.name}
                        secondary={
                          <Box>
                            <Typography variant="body2">
                              {rec.brand} • R$ {rec.price.toFixed(2)}
                            </Typography>
                            <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                              <Chip 
                                label={`ESG ${rec.esg_score.toFixed(1)}`}
                                color={getESGColor(rec.esg_score) as any}
                                size="small"
                              />
                              {rec.discount_percentage > 0 && (
                                <Chip 
                                  label={`-${rec.discount_percentage}%`}
                                  color="error"
                                  size="small"
                                />
                              )}
                            </Box>
                            <Typography variant="caption" color="text.secondary">
                              {rec.reason}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

      {/* Dialog GuardPass */}
      <Dialog 
        open={showGuardPassDialog} 
        onClose={() => setShowGuardPassDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <Security color="primary" />
            <Typography variant="h6">
              🚀 Upgrade para GuardPass
            </Typography>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          {seveProfile?.guardpass_suggestion && (
            <Box>
              <Alert severity="success" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  Baseado no seu perfil ESG, você é elegível para benefícios exclusivos!
                </Typography>
              </Alert>

              <Typography variant="h6" gutterBottom>
                🎁 Benefícios Personalizados:
              </Typography>
              
              <List dense>
                {seveProfile.guardpass_suggestion.personalized_benefits.map((benefit, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Star color="primary" />
                    </ListItemIcon>
                    <ListItemText primary={benefit} />
                  </ListItem>
                ))}
              </List>

              <Divider sx={{ my: 2 }} />

              <Box textAlign="center">
                <Chip 
                  icon={<LocalOffer />}
                  label={seveProfile.guardpass_suggestion.incentive}
                  color="primary"
                  size="medium"
                />
                
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Tier sugerido: <strong>{seveProfile.guardpass_suggestion.suggested_tier}</strong>
                </Typography>
                
                <Typography variant="caption" color="text.secondary">
                  Confiança: {(seveProfile.guardpass_suggestion.confidence * 100).toFixed(0)}%
                </Typography>
              </Box>
            </Box>
          )}
        </DialogContent>
        
        <DialogActions>
          <Button onClick={() => setShowGuardPassDialog(false)}>
            Agora Não
          </Button>
          <Button 
            variant="contained" 
            startIcon={<Verified />}
            onClick={() => {
              setShowGuardPassDialog(false);
              // Aqui integraria com o sistema real de GuardPass
              alert('🎉 GuardPass ativado com sucesso!');
            }}
          >
            Ativar GuardPass
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SEVEPersonalization;
