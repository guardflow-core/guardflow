/**
 * GuardFlow Scanner Page
 * Página de scanner web com câmera e reconhecimento de produtos
 */

import React, { useState, useRef, useCallback, useEffect } from 'react';
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
  Fab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  LinearProgress,
  Divider,
} from '@mui/material';
import {
  CameraAlt,
  QrCodeScanner,
  Add,
  Remove,
  ShoppingCart,
  Close,
  Search,
  Inventory,
  EcoIcon,
  LocalOffer,
  Speed,
} from '@mui/icons-material';

interface Product {
  id: string;
  name: string;
  brand: string;
  price: number;
  barcode?: string;
  ncm_code?: string;
  esg_score?: number;
  category: string;
  image_url?: string;
  confidence?: number;
}

interface CartItem extends Product {
  quantity: number;
  total: number;
}

const ScannerPage: React.FC = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [scannedProducts, setScannedProducts] = useState<Product[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showManualAdd, setShowManualAdd] = useState(false);
  const [manualProduct, setManualProduct] = useState({
    name: '',
    brand: '',
    price: 0,
    category: '',
  });
  const [scanStats, setScanStats] = useState({
    totalScans: 0,
    successfulScans: 0,
    avgConfidence: 0,
  });

  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Inicializar câmera
  const startCamera = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { 
          facingMode: 'environment', // Câmera traseira
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsScanning(true);
      }
    } catch (err) {
      setError('Erro ao acessar câmera. Verifique as permissões.');
      console.error('Camera error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Parar câmera
  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setIsScanning(false);
  }, []);

  // Capturar frame e processar
  const captureAndProcess = useCallback(async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    if (!ctx) return;

    // Configurar canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Capturar frame
    ctx.drawImage(video, 0, 0);
    
    // Converter para blob
    canvas.toBlob(async (blob) => {
      if (!blob) return;

      try {
        setLoading(true);
        
        // Simular reconhecimento de produto
        // Em produção, enviaria para API de reconhecimento
        const mockProduct: Product = {
          id: `prod_${Date.now()}`,
          name: `Produto Escaneado ${scannedProducts.length + 1}`,
          brand: ['Coca-Cola', 'Nestlé', 'Unilever', 'P&G'][Math.floor(Math.random() * 4)],
          price: Math.round((Math.random() * 50 + 5) * 100) / 100,
          barcode: `${Math.floor(Math.random() * 9000000000000) + 1000000000000}`,
          ncm_code: `${Math.floor(Math.random() * 90000000) + 10000000}`,
          esg_score: Math.round((Math.random() * 4 + 6) * 10) / 10,
          category: ['Alimentação', 'Bebidas', 'Limpeza', 'Higiene'][Math.floor(Math.random() * 4)],
          confidence: Math.round((Math.random() * 20 + 80) * 10) / 10,
        };

        // Adicionar aos produtos escaneados
        setScannedProducts(prev => [mockProduct, ...prev]);
        
        // Atualizar estatísticas
        setScanStats(prev => ({
          totalScans: prev.totalScans + 1,
          successfulScans: prev.successfulScans + 1,
          avgConfidence: Math.round(((prev.avgConfidence * prev.totalScans + (mockProduct.confidence || 0)) / (prev.totalScans + 1)) * 10) / 10,
        }));

        // Feedback visual
        setError(null);
        
      } catch (err) {
        setError('Erro ao processar imagem');
        console.error('Processing error:', err);
      } finally {
        setLoading(false);
      }
    }, 'image/jpeg', 0.8);
  }, [scannedProducts.length]);

  // Adicionar ao carrinho
  const addToCart = useCallback((product: Product, quantity: number = 1) => {
    setCart(prev => {
      const existingItem = prev.find(item => item.id === product.id);
      
      if (existingItem) {
        return prev.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + quantity, total: (item.quantity + quantity) * item.price }
            : item
        );
      } else {
        return [...prev, { ...product, quantity, total: quantity * product.price }];
      }
    });
  }, []);

  // Remover do carrinho
  const removeFromCart = useCallback((productId: string) => {
    setCart(prev => prev.filter(item => item.id !== productId));
  }, []);

  // Atualizar quantidade no carrinho
  const updateQuantity = useCallback((productId: string, newQuantity: number) => {
    if (newQuantity <= 0) {
      removeFromCart(productId);
      return;
    }

    setCart(prev =>
      prev.map(item =>
        item.id === productId
          ? { ...item, quantity: newQuantity, total: newQuantity * item.price }
          : item
      )
    );
  }, [removeFromCart]);

  // Adicionar produto manual
  const addManualProduct = useCallback(() => {
    if (!manualProduct.name || !manualProduct.price) return;

    const product: Product = {
      id: `manual_${Date.now()}`,
      name: manualProduct.name,
      brand: manualProduct.brand || 'Marca Genérica',
      price: manualProduct.price,
      category: manualProduct.category || 'Outros',
      esg_score: Math.round((Math.random() * 4 + 6) * 10) / 10,
    };

    setScannedProducts(prev => [product, ...prev]);
    addToCart(product);
    
    // Limpar formulário
    setManualProduct({ name: '', brand: '', price: 0, category: '' });
    setShowManualAdd(false);
  }, [manualProduct, addToCart]);

  // Calcular totais do carrinho
  const cartTotal = cart.reduce((sum, item) => sum + item.total, 0);
  const cartItems = cart.reduce((sum, item) => sum + item.quantity, 0);
  const avgEsgScore = cart.length > 0 
    ? cart.reduce((sum, item) => sum + (item.esg_score || 0) * item.quantity, 0) / cartItems
    : 0;

  // Cleanup ao desmontar
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, [stopCamera]);

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          📱 Scanner de Produtos
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Escaneie produtos com a câmera ou adicione manualmente
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Área de Scanner */}
        <Grid item xs={12} md={8}>
          <Card sx={{ height: 'fit-content' }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  <CameraAlt sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Scanner
                </Typography>
                <Box>
                  <Button
                    variant={isScanning ? "outlined" : "contained"}
                    color={isScanning ? "error" : "primary"}
                    onClick={isScanning ? stopCamera : startCamera}
                    disabled={loading}
                    sx={{ mr: 1 }}
                  >
                    {isScanning ? 'Parar' : 'Iniciar'} Câmera
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<Add />}
                    onClick={() => setShowManualAdd(true)}
                  >
                    Manual
                  </Button>
                </Box>
              </Box>

              {/* Área de vídeo */}
              <Box sx={{ 
                position: 'relative', 
                width: '100%', 
                height: 400, 
                bgcolor: 'grey.100', 
                borderRadius: 2,
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {isScanning ? (
                  <>
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      style={{
                        width: '100%',
                        height: '100%',
                        objectFit: 'cover'
                      }}
                    />
                    <canvas ref={canvasRef} style={{ display: 'none' }} />
                    
                    {/* Overlay de scanner */}
                    <Box sx={{
                      position: 'absolute',
                      top: '50%',
                      left: '50%',
                      transform: 'translate(-50%, -50%)',
                      width: 200,
                      height: 200,
                      border: '2px solid #2196f3',
                      borderRadius: 2,
                      '&::before, &::after': {
                        content: '""',
                        position: 'absolute',
                        width: 20,
                        height: 20,
                        border: '3px solid #2196f3',
                      },
                      '&::before': {
                        top: -3,
                        left: -3,
                        borderRight: 'none',
                        borderBottom: 'none',
                      },
                      '&::after': {
                        bottom: -3,
                        right: -3,
                        borderLeft: 'none',
                        borderTop: 'none',
                      }
                    }} />
                    
                    {/* Botão de captura */}
                    <Fab
                      color="primary"
                      onClick={captureAndProcess}
                      disabled={loading}
                      sx={{
                        position: 'absolute',
                        bottom: 20,
                        left: '50%',
                        transform: 'translateX(-50%)'
                      }}
                    >
                      {loading ? <CircularProgress size={24} /> : <QrCodeScanner />}
                    </Fab>
                  </>
                ) : (
                  <Box sx={{ textAlign: 'center' }}>
                    <CameraAlt sx={{ fontSize: 64, color: 'grey.400', mb: 2 }} />
                    <Typography variant="h6" color="grey.500">
                      Clique em "Iniciar Câmera" para começar
                    </Typography>
                  </Box>
                )}
              </Box>

              {/* Estatísticas de scan */}
              {scanStats.totalScans > 0 && (
                <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                  <Chip
                    icon={<QrCodeScanner />}
                    label={`${scanStats.totalScans} scans`}
                    color="primary"
                    variant="outlined"
                  />
                  <Chip
                    icon={<Speed />}
                    label={`${scanStats.avgConfidence}% confiança`}
                    color="success"
                    variant="outlined"
                  />
                </Box>
              )}

              {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Produtos Escaneados */}
          {scannedProducts.length > 0 && (
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <Inventory sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Produtos Escaneados ({scannedProducts.length})
                </Typography>
                
                <List>
                  {scannedProducts.map((product, index) => (
                    <React.Fragment key={product.id}>
                      <ListItem
                        secondaryAction={
                          <Button
                            variant="contained"
                            size="small"
                            startIcon={<Add />}
                            onClick={() => addToCart(product)}
                          >
                            Adicionar
                          </Button>
                        }
                      >
                        <ListItemAvatar>
                          <Avatar sx={{ bgcolor: 'primary.main' }}>
                            {product.name.charAt(0)}
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography variant="subtitle1">
                                {product.name}
                              </Typography>
                              {product.esg_score && product.esg_score > 7 && (
                                <Chip
                                  icon={<EcoIcon />}
                                  label={`ESG ${product.esg_score}`}
                                  size="small"
                                  color="success"
                                />
                              )}
                              {product.confidence && (
                                <Chip
                                  label={`${product.confidence}%`}
                                  size="small"
                                  variant="outlined"
                                />
                              )}
                            </Box>
                          }
                          secondary={
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                {product.brand} • {product.category}
                              </Typography>
                              <Typography variant="h6" color="primary">
                                R$ {product.price.toFixed(2)}
                              </Typography>
                            </Box>
                          }
                        />
                      </ListItem>
                      {index < scannedProducts.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>
          )}
        </Grid>

        {/* Carrinho */}
        <Grid item xs={12} md={4}>
          <Card sx={{ position: 'sticky', top: 20 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <ShoppingCart sx={{ mr: 1, verticalAlign: 'middle' }} />
                Carrinho ({cartItems} {cartItems === 1 ? 'item' : 'itens'})
              </Typography>

              {cart.length === 0 ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <ShoppingCart sx={{ fontSize: 48, color: 'grey.400', mb: 1 }} />
                  <Typography variant="body2" color="grey.500">
                    Carrinho vazio
                  </Typography>
                </Box>
              ) : (
                <>
                  <List dense>
                    {cart.map((item) => (
                      <ListItem
                        key={item.id}
                        sx={{ px: 0 }}
                        secondaryAction={
                          <IconButton
                            edge="end"
                            onClick={() => removeFromCart(item.id)}
                            size="small"
                          >
                            <Close />
                          </IconButton>
                        }
                      >
                        <ListItemText
                          primary={
                            <Typography variant="subtitle2" noWrap>
                              {item.name}
                            </Typography>
                          }
                          secondary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                              <IconButton
                                size="small"
                                onClick={() => updateQuantity(item.id, item.quantity - 1)}
                              >
                                <Remove />
                              </IconButton>
                              <Typography variant="body2" sx={{ minWidth: 20, textAlign: 'center' }}>
                                {item.quantity}
                              </Typography>
                              <IconButton
                                size="small"
                                onClick={() => updateQuantity(item.id, item.quantity + 1)}
                              >
                                <Add />
                              </IconButton>
                              <Typography variant="body2" sx={{ ml: 'auto' }}>
                                R$ {item.total.toFixed(2)}
                              </Typography>
                            </Box>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>

                  <Divider sx={{ my: 2 }} />

                  {/* Resumo ESG */}
                  {avgEsgScore > 0 && (
                    <Box sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2">Score ESG Médio:</Typography>
                        <Chip
                          icon={<EcoIcon />}
                          label={avgEsgScore.toFixed(1)}
                          size="small"
                          color={avgEsgScore > 7 ? "success" : "warning"}
                        />
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={(avgEsgScore / 10) * 100}
                        color={avgEsgScore > 7 ? "success" : "warning"}
                        sx={{ height: 6, borderRadius: 3 }}
                      />
                    </Box>
                  )}

                  {/* Total */}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography variant="h6">Total:</Typography>
                    <Typography variant="h6" color="primary">
                      R$ {cartTotal.toFixed(2)}
                    </Typography>
                  </Box>

                  <Button
                    variant="contained"
                    fullWidth
                    size="large"
                    startIcon={<LocalOffer />}
                    onClick={() => window.open('/qr-checkout', '_blank')}
                  >
                    Finalizar com QR
                  </Button>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Dialog para adicionar produto manual */}
      <Dialog open={showManualAdd} onClose={() => setShowManualAdd(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Adicionar Produto Manualmente</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                label="Nome do Produto"
                fullWidth
                value={manualProduct.name}
                onChange={(e) => setManualProduct(prev => ({ ...prev, name: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Marca"
                fullWidth
                value={manualProduct.brand}
                onChange={(e) => setManualProduct(prev => ({ ...prev, brand: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Categoria"
                fullWidth
                value={manualProduct.category}
                onChange={(e) => setManualProduct(prev => ({ ...prev, category: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Preço (R$)"
                type="number"
                fullWidth
                value={manualProduct.price}
                onChange={(e) => setManualProduct(prev => ({ ...prev, price: parseFloat(e.target.value) || 0 }))}
                inputProps={{ step: 0.01, min: 0 }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowManualAdd(false)}>Cancelar</Button>
          <Button
            onClick={addManualProduct}
            variant="contained"
            disabled={!manualProduct.name || !manualProduct.price}
          >
            Adicionar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ScannerPage;
