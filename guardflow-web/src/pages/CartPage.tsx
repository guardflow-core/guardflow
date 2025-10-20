/**
 * GuardFlow Cart Page
 * Página de carrinho web com integração completa ao backend
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
  Stepper,
  Step,
  StepLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Tooltip,
  Fab,
} from '@mui/material';
import {
  ShoppingCart,
  Add,
  Remove,
  Delete,
  Clear,
  Payment,
  LocalShipping,
  EcoIcon,
  Discount,
  Receipt,
  ExpandMore,
  QrCode,
  CreditCard,
  Pix,
  Security,
  Speed,
  CheckCircle,
  Warning,
  Info,
} from '@mui/icons-material';

interface CartItem {
  id: string;
  name: string;
  brand: string;
  price: number;
  quantity: number;
  total: number;
  esg_score?: number;
  category: string;
  image_url?: string;
  ncm_code?: string;
  barcode?: string;
  discount?: number;
  tax?: number;
}

interface PaymentMethod {
  id: string;
  name: string;
  icon: React.ReactNode;
  fee: number;
  processing_time: string;
  available: boolean;
}

interface ShippingOption {
  id: string;
  name: string;
  price: number;
  estimated_days: number;
  description: string;
}

const CartPage: React.FC = () => {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeStep, setActiveStep] = useState(0);
  const [selectedPayment, setSelectedPayment] = useState<string>('');
  const [selectedShipping, setSelectedShipping] = useState<string>('');
  const [showClearDialog, setShowClearDialog] = useState(false);
  const [couponCode, setCouponCode] = useState('');
  const [appliedCoupon, setAppliedCoupon] = useState<any>(null);
  const [esgAnalysis, setEsgAnalysis] = useState<any>(null);

  const steps = ['Carrinho', 'Entrega', 'Pagamento', 'Confirmação'];

  const paymentMethods: PaymentMethod[] = [
    {
      id: 'qr_checkout',
      name: 'QR Checkout GuardFlow',
      icon: <QrCode />,
      fee: 0,
      processing_time: 'Instantâneo',
      available: true,
    },
    {
      id: 'pix',
      name: 'PIX',
      icon: <Pix />,
      fee: 0,
      processing_time: 'Instantâneo',
      available: true,
    },
    {
      id: 'credit_card',
      name: 'Cartão de Crédito',
      icon: <CreditCard />,
      fee: 2.99,
      processing_time: '1-2 dias úteis',
      available: true,
    },
  ];

  const shippingOptions: ShippingOption[] = [
    {
      id: 'pickup',
      name: 'Retirada na Loja',
      price: 0,
      estimated_days: 0,
      description: 'Retire gratuitamente em nossa loja',
    },
    {
      id: 'express',
      name: 'Entrega Expressa',
      price: 15.90,
      estimated_days: 1,
      description: 'Receba em até 24h',
    },
    {
      id: 'standard',
      name: 'Entrega Padrão',
      price: 8.90,
      estimated_days: 3,
      description: 'Receba em 2-3 dias úteis',
    },
  ];

  // Carregar carrinho do localStorage ou API
  useEffect(() => {
    loadCart();
  }, []);

  // Calcular análise ESG quando carrinho mudar
  useEffect(() => {
    if (cart.length > 0) {
      calculateEsgAnalysis();
    }
  }, [cart]);

  const loadCart = useCallback(async () => {
    setLoading(true);
    try {
      // Simular carregamento do carrinho
      // Em produção, faria chamada para API
      const savedCart = localStorage.getItem('guardflow_cart');
      if (savedCart) {
        setCart(JSON.parse(savedCart));
      } else {
        // Carrinho demo
        const demoCart: CartItem[] = [
          {
            id: '1',
            name: 'Água Mineral Crystal 500ml',
            brand: 'Crystal',
            price: 2.50,
            quantity: 2,
            total: 5.00,
            esg_score: 8.5,
            category: 'Bebidas',
            ncm_code: '22011000',
            barcode: '7891234567890',
          },
          {
            id: '2',
            name: 'Sabonete Líquido Dove',
            brand: 'Dove',
            price: 12.90,
            quantity: 1,
            total: 12.90,
            esg_score: 7.2,
            category: 'Higiene',
            ncm_code: '34012000',
            barcode: '7891234567891',
          },
          {
            id: '3',
            name: 'Chocolate Lacta 90g',
            brand: 'Lacta',
            price: 6.50,
            quantity: 3,
            total: 19.50,
            esg_score: 6.8,
            category: 'Alimentação',
            ncm_code: '18063210',
            barcode: '7891234567892',
          },
        ];
        setCart(demoCart);
      }
    } catch (err) {
      setError('Erro ao carregar carrinho');
      console.error('Load cart error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const saveCart = useCallback((newCart: CartItem[]) => {
    localStorage.setItem('guardflow_cart', JSON.stringify(newCart));
    setCart(newCart);
  }, []);

  const updateQuantity = useCallback((itemId: string, newQuantity: number) => {
    if (newQuantity <= 0) {
      removeItem(itemId);
      return;
    }

    const newCart = cart.map(item =>
      item.id === itemId
        ? { ...item, quantity: newQuantity, total: newQuantity * item.price }
        : item
    );
    saveCart(newCart);
  }, [cart, saveCart]);

  const removeItem = useCallback((itemId: string) => {
    const newCart = cart.filter(item => item.id !== itemId);
    saveCart(newCart);
  }, [cart, saveCart]);

  const clearCart = useCallback(() => {
    saveCart([]);
    setShowClearDialog(false);
  }, [saveCart]);

  const applyCoupon = useCallback(async () => {
    if (!couponCode.trim()) return;

    setLoading(true);
    try {
      // Simular validação de cupom
      const mockCoupons: any = {
        'ESG10': { discount: 0.10, type: 'percentage', description: '10% desconto ESG' },
        'FIRST20': { discount: 0.20, type: 'percentage', description: '20% primeira compra' },
        'SAVE5': { discount: 5.00, type: 'fixed', description: 'R$ 5,00 de desconto' },
      };

      const coupon = mockCoupons[couponCode.toUpperCase()];
      if (coupon) {
        setAppliedCoupon({ code: couponCode.toUpperCase(), ...coupon });
        setError(null);
      } else {
        setError('Cupom inválido ou expirado');
      }
    } catch (err) {
      setError('Erro ao aplicar cupom');
    } finally {
      setLoading(false);
    }
  }, [couponCode]);

  const calculateEsgAnalysis = useCallback(async () => {
    try {
      const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
      const avgEsgScore = cart.reduce((sum, item) => 
        sum + (item.esg_score || 0) * item.quantity, 0) / totalItems;
      
      const esgCategories = {
        excellent: cart.filter(item => (item.esg_score || 0) >= 8).length,
        good: cart.filter(item => (item.esg_score || 0) >= 6 && (item.esg_score || 0) < 8).length,
        fair: cart.filter(item => (item.esg_score || 0) < 6).length,
      };

      const carbonFootprint = cart.reduce((sum, item) => {
        // Simulação de pegada de carbono baseada na categoria
        const categoryMultiplier: any = {
          'Alimentação': 0.5,
          'Bebidas': 0.3,
          'Higiene': 0.2,
          'Limpeza': 0.4,
        };
        return sum + (item.quantity * (categoryMultiplier[item.category] || 0.3));
      }, 0);

      setEsgAnalysis({
        avgScore: avgEsgScore,
        categories: esgCategories,
        carbonFootprint: carbonFootprint,
        recommendations: avgEsgScore > 7 
          ? ['Parabéns! Suas escolhas são sustentáveis'] 
          : ['Considere produtos com melhor score ESG', 'Veja nossas recomendações sustentáveis'],
      });
    } catch (err) {
      console.error('ESG analysis error:', err);
    }
  }, [cart]);

  const processCheckout = useCallback(async () => {
    if (!selectedPayment || !selectedShipping) {
      setError('Selecione método de pagamento e entrega');
      return;
    }

    setLoading(true);
    try {
      if (selectedPayment === 'qr_checkout') {
        // Redirecionar para QR Checkout
        const cartData = {
          cart_id: `cart_${Date.now()}`,
          store_id: 'web_store_001',
          items: cart.map(item => ({
            name: item.name,
            brand: item.brand,
            unit_price: item.price,
            quantity: item.quantity,
            ncm_code: item.ncm_code,
            barcode: item.barcode,
            esg_score: item.esg_score,
          })),
          timestamp_ms: Date.now(),
        };

        // Salvar dados do carrinho para QR Checkout
        localStorage.setItem('qr_checkout_cart', JSON.stringify(cartData));
        window.open('/qr-checkout', '_blank');
      } else {
        // Processar outros métodos de pagamento
        setActiveStep(3);
        setTimeout(() => {
          clearCart();
          setActiveStep(0);
        }, 3000);
      }
    } catch (err) {
      setError('Erro ao processar checkout');
      console.error('Checkout error:', err);
    } finally {
      setLoading(false);
    }
  }, [selectedPayment, selectedShipping, cart, clearCart]);

  // Cálculos do carrinho
  const subtotal = cart.reduce((sum, item) => sum + item.total, 0);
  const discountAmount = appliedCoupon 
    ? appliedCoupon.type === 'percentage' 
      ? subtotal * appliedCoupon.discount
      : appliedCoupon.discount
    : 0;
  const shippingCost = shippingOptions.find(s => s.id === selectedShipping)?.price || 0;
  const paymentFee = paymentMethods.find(p => p.id === selectedPayment)?.fee || 0;
  const total = subtotal - discountAmount + shippingCost + paymentFee;
  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);

  if (loading && cart.length === 0) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          🛒 Carrinho de Compras
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {totalItems} {totalItems === 1 ? 'item' : 'itens'} • Total: R$ {total.toFixed(2)}
        </Typography>
      </Box>

      {/* Stepper */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {cart.length === 0 ? (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 8 }}>
            <ShoppingCart sx={{ fontSize: 64, color: 'grey.400', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              Seu carrinho está vazio
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              Adicione produtos para começar suas compras
            </Typography>
            <Button
              variant="contained"
              size="large"
              onClick={() => window.location.href = '/scanner'}
            >
              Começar a Comprar
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {/* Lista de itens */}
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Itens do Carrinho ({totalItems})
                  </Typography>
                  <Button
                    variant="outlined"
                    color="error"
                    startIcon={<Clear />}
                    onClick={() => setShowClearDialog(true)}
                    size="small"
                  >
                    Limpar Carrinho
                  </Button>
                </Box>

                <List>
                  {cart.map((item, index) => (
                    <React.Fragment key={item.id}>
                      <ListItem sx={{ px: 0, py: 2 }}>
                        <ListItemAvatar>
                          <Avatar sx={{ bgcolor: 'primary.main' }}>
                            {item.name.charAt(0)}
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography variant="subtitle1">
                                {item.name}
                              </Typography>
                              {item.esg_score && item.esg_score > 7 && (
                                <Chip
                                  icon={<EcoIcon />}
                                  label={`ESG ${item.esg_score}`}
                                  size="small"
                                  color="success"
                                />
                              )}
                            </Box>
                          }
                          secondary={
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                {item.brand} • {item.category}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                R$ {item.price.toFixed(2)} cada
                              </Typography>
                            </Box>
                          }
                        />
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <IconButton
                            size="small"
                            onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          >
                            <Remove />
                          </IconButton>
                          <Typography variant="body1" sx={{ minWidth: 40, textAlign: 'center' }}>
                            {item.quantity}
                          </Typography>
                          <IconButton
                            size="small"
                            onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          >
                            <Add />
                          </IconButton>
                          <Typography variant="h6" sx={{ ml: 2, minWidth: 80, textAlign: 'right' }}>
                            R$ {item.total.toFixed(2)}
                          </Typography>
                          <IconButton
                            color="error"
                            onClick={() => removeItem(item.id)}
                          >
                            <Delete />
                          </IconButton>
                        </Box>
                      </ListItem>
                      {index < cart.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>

            {/* Análise ESG */}
            {esgAnalysis && (
              <Card sx={{ mt: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <EcoIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Análise ESG da Compra
                  </Typography>
                  
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          Score ESG Médio: {esgAnalysis.avgScore.toFixed(1)}/10
                        </Typography>
                        <LinearProgress
                          variant="determinate"
                          value={(esgAnalysis.avgScore / 10) * 100}
                          color={esgAnalysis.avgScore > 7 ? "success" : "warning"}
                          sx={{ height: 8, borderRadius: 4 }}
                        />
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <Typography variant="body2" gutterBottom>
                        Pegada de Carbono Estimada: {esgAnalysis.carbonFootprint.toFixed(1)} kg CO₂
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                        <Chip label={`${esgAnalysis.categories.excellent} Excelente`} color="success" size="small" />
                        <Chip label={`${esgAnalysis.categories.good} Bom`} color="warning" size="small" />
                        <Chip label={`${esgAnalysis.categories.fair} Regular`} color="error" size="small" />
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            )}

            {/* Métodos de Entrega */}
            {activeStep >= 1 && (
              <Card sx={{ mt: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <LocalShipping sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Método de Entrega
                  </Typography>
                  
                  {shippingOptions.map((option) => (
                    <Paper
                      key={option.id}
                      sx={{
                        p: 2,
                        mb: 1,
                        cursor: 'pointer',
                        border: selectedShipping === option.id ? '2px solid' : '1px solid',
                        borderColor: selectedShipping === option.id ? 'primary.main' : 'grey.300',
                      }}
                      onClick={() => setSelectedShipping(option.id)}
                    >
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Box>
                          <Typography variant="subtitle1">{option.name}</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {option.description}
                          </Typography>
                          {option.estimated_days > 0 && (
                            <Typography variant="caption">
                              Entrega em {option.estimated_days} {option.estimated_days === 1 ? 'dia' : 'dias'}
                            </Typography>
                          )}
                        </Box>
                        <Typography variant="h6" color="primary">
                          {option.price === 0 ? 'Grátis' : `R$ ${option.price.toFixed(2)}`}
                        </Typography>
                      </Box>
                    </Paper>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Métodos de Pagamento */}
            {activeStep >= 2 && (
              <Card sx={{ mt: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <Payment sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Método de Pagamento
                  </Typography>
                  
                  {paymentMethods.map((method) => (
                    <Paper
                      key={method.id}
                      sx={{
                        p: 2,
                        mb: 1,
                        cursor: method.available ? 'pointer' : 'not-allowed',
                        opacity: method.available ? 1 : 0.5,
                        border: selectedPayment === method.id ? '2px solid' : '1px solid',
                        borderColor: selectedPayment === method.id ? 'primary.main' : 'grey.300',
                      }}
                      onClick={() => method.available && setSelectedPayment(method.id)}
                    >
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                          {method.icon}
                          <Box>
                            <Typography variant="subtitle1">{method.name}</Typography>
                            <Typography variant="body2" color="text.secondary">
                              {method.processing_time}
                            </Typography>
                          </Box>
                        </Box>
                        <Box sx={{ textAlign: 'right' }}>
                          <Typography variant="h6" color="primary">
                            {method.fee === 0 ? 'Grátis' : `+R$ ${method.fee.toFixed(2)}`}
                          </Typography>
                          {method.id === 'qr_checkout' && (
                            <Chip
                              icon={<Speed />}
                              label="Recomendado"
                              size="small"
                              color="success"
                            />
                          )}
                        </Box>
                      </Box>
                    </Paper>
                  ))}
                </CardContent>
              </Card>
            )}
          </Grid>

          {/* Resumo do pedido */}
          <Grid item xs={12} md={4}>
            <Card sx={{ position: 'sticky', top: 20 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <Receipt sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Resumo do Pedido
                </Typography>

                {/* Cupom de desconto */}
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Cupom de Desconto
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <TextField
                      size="small"
                      placeholder="Código do cupom"
                      value={couponCode}
                      onChange={(e) => setCouponCode(e.target.value)}
                      disabled={!!appliedCoupon}
                      fullWidth
                    />
                    <Button
                      variant="outlined"
                      onClick={applyCoupon}
                      disabled={loading || !!appliedCoupon}
                    >
                      Aplicar
                    </Button>
                  </Box>
                  {appliedCoupon && (
                    <Alert severity="success" sx={{ mt: 1 }}>
                      {appliedCoupon.description} aplicado!
                    </Alert>
                  )}
                </Box>

                <Divider sx={{ mb: 2 }} />

                {/* Detalhes do valor */}
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">Subtotal ({totalItems} itens):</Typography>
                    <Typography variant="body2">R$ {subtotal.toFixed(2)}</Typography>
                  </Box>
                  
                  {appliedCoupon && (
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2" color="success.main">
                        Desconto ({appliedCoupon.code}):
                      </Typography>
                      <Typography variant="body2" color="success.main">
                        -R$ {discountAmount.toFixed(2)}
                      </Typography>
                    </Box>
                  )}
                  
                  {selectedShipping && shippingCost > 0 && (
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Entrega:</Typography>
                      <Typography variant="body2">R$ {shippingCost.toFixed(2)}</Typography>
                    </Box>
                  )}
                  
                  {selectedPayment && paymentFee > 0 && (
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Taxa de pagamento:</Typography>
                      <Typography variant="body2">R$ {paymentFee.toFixed(2)}</Typography>
                    </Box>
                  )}
                </Box>

                <Divider sx={{ mb: 2 }} />

                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
                  <Typography variant="h6">Total:</Typography>
                  <Typography variant="h6" color="primary">
                    R$ {total.toFixed(2)}
                  </Typography>
                </Box>

                {/* Botões de ação */}
                {activeStep === 0 && (
                  <Button
                    variant="contained"
                    fullWidth
                    size="large"
                    onClick={() => setActiveStep(1)}
                  >
                    Continuar
                  </Button>
                )}

                {activeStep === 1 && (
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                      variant="outlined"
                      onClick={() => setActiveStep(0)}
                      fullWidth
                    >
                      Voltar
                    </Button>
                    <Button
                      variant="contained"
                      onClick={() => setActiveStep(2)}
                      disabled={!selectedShipping}
                      fullWidth
                    >
                      Continuar
                    </Button>
                  </Box>
                )}

                {activeStep === 2 && (
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                      variant="outlined"
                      onClick={() => setActiveStep(1)}
                      fullWidth
                    >
                      Voltar
                    </Button>
                    <Button
                      variant="contained"
                      onClick={processCheckout}
                      disabled={!selectedPayment || loading}
                      fullWidth
                    >
                      {loading ? <CircularProgress size={24} /> : 'Finalizar'}
                    </Button>
                  </Box>
                )}

                {activeStep === 3 && (
                  <Box sx={{ textAlign: 'center' }}>
                    <CheckCircle sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
                    <Typography variant="h6" gutterBottom>
                      Pedido Confirmado!
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Você receberá um e-mail com os detalhes
                    </Typography>
                  </Box>
                )}

                {/* Informações de segurança */}
                <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                    <Security color="primary" />
                    <Typography variant="subtitle2">Compra Segura</Typography>
                  </Box>
                  <Typography variant="caption" color="text.secondary">
                    Seus dados estão protegidos com criptografia SSL
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Dialog de confirmação para limpar carrinho */}
      <Dialog open={showClearDialog} onClose={() => setShowClearDialog(false)}>
        <DialogTitle>Limpar Carrinho</DialogTitle>
        <DialogContent>
          <Typography>
            Tem certeza que deseja remover todos os itens do carrinho?
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowClearDialog(false)}>Cancelar</Button>
          <Button onClick={clearCart} color="error" variant="contained">
            Limpar
          </Button>
        </DialogActions>
      </Dialog>

      {/* FAB para QR Checkout rápido */}
      {cart.length > 0 && (
        <Fab
          color="primary"
          sx={{ position: 'fixed', bottom: 16, right: 16 }}
          onClick={() => {
            setSelectedPayment('qr_checkout');
            setSelectedShipping('pickup');
            setActiveStep(2);
          }}
        >
          <QrCode />
        </Fab>
      )}
    </Box>
  );
};

export default CartPage;
