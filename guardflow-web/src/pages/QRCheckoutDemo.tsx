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
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  QrCode,
  ShoppingCart,
  Scale,
  Security,
  Eco,
  Timer,
  CheckCircle,
  Warning,
  Block,
  Speed
} from '@mui/icons-material';

interface CartItem {
  sku: string;
  name: string;
  unit_price: number;
  quantity: number;
  expected_weight_kg: number;
  sensitive?: boolean;
  esg_score?: number;
  ncm_code?: string;
}

interface Cart {
  cart_id: string;
  store_id: string;
  items: CartItem[];
  subtotal: number;
  expected_total_weight_kg: number;
  sector_context?: string;
  store_type?: string;
}

interface SealResponse {
  cart_id: string;
  qr_token: string;
  agility_tax_applicable: boolean;
  estimated_time_saved_minutes: number;
  esg_impact_score?: number;
}

interface AnomalyScore {
  score: number;
  decision: 'allow' | 'sample' | 'block';
  delta_weight_ratio: number;
  sensitive_items_flag: boolean;
}

const DEMO_PRODUCTS = {
  supermercado: [
    { sku: "7891000100103", name: "Leite Integral 1L", price: 4.50, weight: 1.03, esg_score: 6.5, ncm: "04011010" },
    { sku: "7891000315507", name: "Açúcar Cristal 1kg", price: 3.20, weight: 1.0, esg_score: 4.0, ncm: "17019900" },
    { sku: "7891000053508", name: "Arroz Branco 5kg", price: 18.90, weight: 5.0, esg_score: 5.5, ncm: "10063021" },
    { sku: "7891991010016", name: "Cerveja Lata 350ml", price: 2.80, weight: 0.35, esg_score: 3.0, ncm: "22030000", sensitive: true }
  ],
  farmacia: [
    { sku: "7896658003912", name: "Dipirona 500mg", price: 8.50, weight: 0.05, esg_score: 8.0, ncm: "30049099", sensitive: true },
    { sku: "7896112108721", name: "Vitamina C 1g", price: 15.20, weight: 0.08, esg_score: 7.5, ncm: "21069090" }
  ],
  eletronicos: [
    { sku: "7899619404567", name: "Cabo USB-C 1m", price: 25.90, weight: 0.15, esg_score: 4.5, ncm: "85444290" },
    { sku: "7891234567890", name: "Fone Bluetooth", price: 89.90, weight: 0.25, esg_score: 5.2, ncm: "85183000", sensitive: true }
  ]
};

const QRCheckoutDemo: React.FC = () => {
  const [storeType, setStoreType] = useState<string>('supermercado');
  const [cart, setCart] = useState<Cart | null>(null);
  const [sealResponse, setSealResponse] = useState<SealResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [qrDialogOpen, setQrDialogOpen] = useState(false);
  const [testWeight, setTestWeight] = useState(0);
  const [anomalyScore, setAnomalyScore] = useState<AnomalyScore | null>(null);
  const [guardpassEnabled, setGuardpassEnabled] = useState(false);

  const createDemoCart = () => {
    const products = DEMO_PRODUCTS[storeType as keyof typeof DEMO_PRODUCTS];
    const selectedProducts = products.slice(0, Math.min(3, products.length));
    
    const items: CartItem[] = selectedProducts.map(product => ({
      sku: product.sku,
      name: product.name,
      unit_price: product.price,
      quantity: Math.floor(Math.random() * 3) + 1,
      expected_weight_kg: product.weight,
      sensitive: product.sensitive || false,
      esg_score: product.esg_score,
      ncm_code: product.ncm
    }));

    const subtotal = items.reduce((sum, item) => sum + (item.unit_price * item.quantity), 0);
    const totalWeight = items.reduce((sum, item) => sum + (item.expected_weight_kg * item.quantity), 0);

    const newCart: Cart = {
      cart_id: `demo_cart_${Date.now()}`,
      store_id: `store_${storeType}_001`,
      items,
      subtotal: Math.round(subtotal * 100) / 100,
      expected_total_weight_kg: Math.round(totalWeight * 1000) / 1000,
      sector_context: storeType === 'farmacia' ? 'security' : 'retail',
      store_type: storeType
    };

    setCart(newCart);
    setTestWeight(newCart.expected_total_weight_kg);
    setSealResponse(null);
    setAnomalyScore(null);
  };

  const sealCart = async () => {
    if (!cart) return;

    setLoading(true);
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json'
      };
      
      if (guardpassEnabled) {
        headers['guardpass_token'] = 'demo_premium_token';
      }

      const response = await fetch('/api/v1/qr-checkout/seal', {
        method: 'POST',
        headers,
        body: JSON.stringify({
          cart: {
            ...cart,
            timestamp_ms: Date.now()
          }
        })
      });

      if (response.ok) {
        const result = await response.json();
        setSealResponse(result);
        setQrDialogOpen(true);
      } else {
        console.error('Erro ao selar carrinho:', await response.text());
      }
    } catch (error) {
      console.error('Erro na requisição:', error);
    } finally {
      setLoading(false);
    }
  };

  const testAnomalyScore = async () => {
    if (!cart) return;

    setLoading(true);
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json'
      };
      
      if (guardpassEnabled) {
        headers['guardpass_token'] = 'demo_premium_token';
      }

      const response = await fetch('/api/v1/qr-checkout/anomaly-score', {
        method: 'POST',
        headers,
        body: JSON.stringify({
          expected_weight_kg: cart.expected_total_weight_kg,
          measured_weight_kg: testWeight,
          items: cart.items,
          scan_duration_sec: 45,
          sector_context: cart.sector_context,
          store_type: cart.store_type,
          time_of_day: new Date().getHours(),
          guardpass_tier: guardpassEnabled ? 'premium' : 'basic'
        })
      });

      if (response.ok) {
        const result = await response.json();
        setAnomalyScore(result);
      } else {
        console.error('Erro ao calcular score:', await response.text());
      }
    } catch (error) {
      console.error('Erro na requisição:', error);
    } finally {
      setLoading(false);
    }
  };

  const getDecisionColor = (decision: string) => {
    switch (decision) {
      case 'allow': return 'success';
      case 'sample': return 'warning';
      case 'block': return 'error';
      default: return 'default';
    }
  };

  const getDecisionIcon = (decision: string) => {
    switch (decision) {
      case 'allow': return <CheckCircle />;
      case 'sample': return <Warning />;
      case 'block': return <Block />;
      default: return null;
    }
  };

  useEffect(() => {
    createDemoCart();
  }, [storeType]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        🛒 QR Checkout Demo - GuardFlow
      </Typography>
      
      <Grid container spacing={3}>
        {/* Configuração */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                ⚙️ Configuração
              </Typography>
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Tipo de Loja</InputLabel>
                <Select
                  value={storeType}
                  onChange={(e) => setStoreType(e.target.value)}
                >
                  <MenuItem value="supermercado">🛒 Supermercado</MenuItem>
                  <MenuItem value="farmacia">💊 Farmácia</MenuItem>
                  <MenuItem value="eletronicos">📱 Eletrônicos</MenuItem>
                </Select>
              </FormControl>

              <Box sx={{ mb: 2 }}>
                <Button
                  variant="outlined"
                  onClick={() => setGuardpassEnabled(!guardpassEnabled)}
                  color={guardpassEnabled ? 'primary' : 'default'}
                  fullWidth
                >
                  {guardpassEnabled ? '🔓 GuardPass Premium' : '🔒 GuardPass Básico'}
                </Button>
              </Box>

              <Button
                variant="contained"
                onClick={createDemoCart}
                fullWidth
                startIcon={<ShoppingCart />}
              >
                Novo Carrinho Demo
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Carrinho */}
        <Grid item xs={12} md={8}>
          {cart && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🛒 Carrinho: {cart.cart_id}
                </Typography>
                
                <List dense>
                  {cart.items.map((item, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        {item.sensitive ? <Security color="error" /> : <ShoppingCart />}
                      </ListItemIcon>
                      <ListItemText
                        primary={`${item.quantity}x ${item.name}`}
                        secondary={
                          <Box>
                            <Typography variant="body2">
                              R$ {item.unit_price.toFixed(2)} | {item.expected_weight_kg}kg
                            </Typography>
                            {item.esg_score && (
                              <Chip
                                size="small"
                                icon={<Eco />}
                                label={`ESG: ${item.esg_score}`}
                                color={item.esg_score > 7 ? 'success' : item.esg_score > 5 ? 'warning' : 'default'}
                              />
                            )}
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>

                <Divider sx={{ my: 2 }} />
                
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="h6">
                      💰 Total: R$ {cart.subtotal.toFixed(2)}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="h6">
                      ⚖️ Peso: {cart.expected_total_weight_kg.toFixed(3)}kg
                    </Typography>
                  </Grid>
                </Grid>

                <Box sx={{ mt: 2 }}>
                  <Button
                    variant="contained"
                    onClick={sealCart}
                    disabled={loading}
                    startIcon={loading ? <CircularProgress size={20} /> : <QrCode />}
                    fullWidth
                  >
                    {loading ? 'Gerando QR...' : 'Gerar QR Checkout'}
                  </Button>
                </Box>
              </CardContent>
            </Card>
          )}
        </Grid>

        {/* Teste de Peso */}
        {cart && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  ⚖️ Simulação de Pesagem
                </Typography>
                
                <Typography gutterBottom>
                  Peso Esperado: {cart.expected_total_weight_kg.toFixed(3)}kg
                </Typography>
                
                <Typography gutterBottom>
                  Peso Medido: {testWeight.toFixed(3)}kg
                </Typography>
                
                <Slider
                  value={testWeight}
                  onChange={(_, value) => setTestWeight(value as number)}
                  min={cart.expected_total_weight_kg * 0.5}
                  max={cart.expected_total_weight_kg * 1.5}
                  step={0.01}
                  marks={[
                    { value: cart.expected_total_weight_kg * 0.85, label: '-15%' },
                    { value: cart.expected_total_weight_kg, label: 'Correto' },
                    { value: cart.expected_total_weight_kg * 1.15, label: '+15%' }
                  ]}
                />

                <Button
                  variant="outlined"
                  onClick={testAnomalyScore}
                  disabled={loading}
                  startIcon={<Scale />}
                  fullWidth
                  sx={{ mt: 2 }}
                >
                  Testar Score de Anomalia
                </Button>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Resultado do Score */}
        {anomalyScore && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🎯 Score de Anomalia
                </Typography>
                
                <Alert
                  severity={getDecisionColor(anomalyScore.decision) as any}
                  icon={getDecisionIcon(anomalyScore.decision)}
                  sx={{ mb: 2 }}
                >
                  <Typography variant="h6">
                    {anomalyScore.decision.toUpperCase()}
                  </Typography>
                  Score: {anomalyScore.score.toFixed(3)}
                </Alert>

                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body2">
                      Δ Peso: {(anomalyScore.delta_weight_ratio * 100).toFixed(1)}%
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2">
                      Itens Sensíveis: {anomalyScore.sensitive_items_flag ? 'Sim' : 'Não'}
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

      {/* Dialog do QR Code */}
      <Dialog open={qrDialogOpen} onClose={() => setQrDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          ✅ QR Checkout Gerado
        </DialogTitle>
        <DialogContent>
          {sealResponse && (
            <Box textAlign="center">
              <Box
                sx={{
                  p: 3,
                  border: '2px solid #ccc',
                  borderRadius: 2,
                  mb: 2,
                  fontFamily: 'monospace',
                  fontSize: '0.8rem',
                  wordBreak: 'break-all',
                  backgroundColor: '#f5f5f5'
                }}
              >
                {sealResponse.qr_token}
              </Box>
              
              <Grid container spacing={2} sx={{ mt: 2 }}>
                <Grid item xs={6}>
                  <Chip
                    icon={<Timer />}
                    label={`${sealResponse.estimated_time_saved_minutes.toFixed(1)}min economizados`}
                    color="primary"
                  />
                </Grid>
                <Grid item xs={6}>
                  <Chip
                    icon={<Speed />}
                    label={sealResponse.agility_tax_applicable ? 'Agility Tax' : 'Sem Taxa'}
                    color={sealResponse.agility_tax_applicable ? 'success' : 'default'}
                  />
                </Grid>
              </Grid>

              {sealResponse.esg_impact_score && (
                <Box sx={{ mt: 2 }}>
                  <Chip
                    icon={<Eco />}
                    label={`ESG Score: ${sealResponse.esg_impact_score.toFixed(1)}`}
                    color="success"
                    size="medium"
                  />
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default QRCheckoutDemo;
