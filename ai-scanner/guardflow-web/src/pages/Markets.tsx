import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  useTheme,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  Store,
  LocationOn,
  Phone,
  Email,
  CheckCircle,
  Cancel,
} from '@mui/icons-material';

// Tipos
interface Market {
  id: string;
  name: string;
  address: string;
  phone: string;
  email: string;
  status: 'active' | 'inactive' | 'pending';
  type: 'supermarket' | 'convenience' | 'pharmacy' | 'other';
  created_at: string;
  updated_at: string;
}

// Componente Markets
const Markets: React.FC = () => {
  // Hooks
  const theme = useTheme();
  
  // Local state
  const [markets, setMarkets] = useState<Market[]>([]);
  const [open, setOpen] = useState(false);
  const [editingMarket, setEditingMarket] = useState<Market | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    phone: '',
    email: '',
    status: 'active' as const,
    type: 'supermarket' as const,
  });
  
  // Effects
  useEffect(() => {
    // Simular dados de mercados
    setMarkets([
      {
        id: '1',
        name: 'Supermercado Central',
        address: 'Rua das Flores, 123 - Centro',
        phone: '(11) 99999-9999',
        email: 'contato@supercentral.com',
        status: 'active',
        type: 'supermarket',
        created_at: '2024-01-15',
        updated_at: '2024-01-15',
      },
      {
        id: '2',
        name: 'Farmácia Saúde',
        address: 'Av. Principal, 456 - Bairro Novo',
        phone: '(11) 88888-8888',
        email: 'contato@farmaciasaude.com',
        status: 'active',
        type: 'pharmacy',
        created_at: '2024-01-10',
        updated_at: '2024-01-10',
      },
      {
        id: '3',
        name: 'Conveniência 24h',
        address: 'Rua da Conveniência, 789 - Centro',
        phone: '(11) 77777-7777',
        email: 'contato@conveniencia24h.com',
        status: 'pending',
        type: 'convenience',
        created_at: '2024-01-20',
        updated_at: '2024-01-20',
      },
    ]);
  }, []);
  
  // Handlers
  const handleOpen = () => {
    setEditingMarket(null);
    setFormData({
      name: '',
      address: '',
      phone: '',
      email: '',
      status: 'active',
      type: 'supermarket',
    });
    setOpen(true);
  };
  
  const handleClose = () => {
    setOpen(false);
    setEditingMarket(null);
  };
  
  const handleEdit = (market: Market) => {
    setEditingMarket(market);
    setFormData({
      name: market.name,
      address: market.address,
      phone: market.phone,
      email: market.email,
      status: market.status,
      type: market.type,
    });
    setOpen(true);
  };
  
  const handleDelete = (id: string) => {
    setMarkets(markets.filter(market => market.id !== id));
  };
  
  const handleSubmit = () => {
    if (editingMarket) {
      // Atualizar mercado existente
      setMarkets(markets.map(market => 
        market.id === editingMarket.id 
          ? { ...market, ...formData, updated_at: new Date().toISOString() }
          : market
      ));
    } else {
      // Criar novo mercado
      const newMarket: Market = {
        id: Date.now().toString(),
        ...formData,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setMarkets([...markets, newMarket]);
    }
    handleClose();
  };
  
  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };
  
  // Renderizar status
  const renderStatus = (status: string) => {
    const statusConfig = {
      active: { color: 'success', icon: <CheckCircle />, label: 'Ativo' },
      inactive: { color: 'error', icon: <Cancel />, label: 'Inativo' },
      pending: { color: 'warning', icon: <Cancel />, label: 'Pendente' },
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
  
  // Renderizar tipo
  const renderType = (type: string) => {
    const typeConfig = {
      supermarket: 'Supermercado',
      convenience: 'Conveniência',
      pharmacy: 'Farmácia',
      other: 'Outro',
    };
    
    return typeConfig[type as keyof typeof typeConfig] || type;
  };
  
  // Renderizar card de mercado
  const renderMarketCard = (market: Market) => (
    <Card key={market.id} sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Avatar sx={{ bgcolor: theme.palette.primary.main, mr: 2 }}>
            <Store />
          </Avatar>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" component="div">
              {market.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {renderType(market.type)}
            </Typography>
          </Box>
          {renderStatus(market.status)}
        </Box>
        
        <List dense>
          <ListItem sx={{ px: 0 }}>
            <ListItemText
              primary="Endereço"
              secondary={market.address}
              primaryTypographyProps={{ variant: 'body2' }}
              secondaryTypographyProps={{ variant: 'body2' }}
            />
          </ListItem>
          <ListItem sx={{ px: 0 }}>
            <ListItemText
              primary="Telefone"
              secondary={market.phone}
              primaryTypographyProps={{ variant: 'body2' }}
              secondaryTypographyProps={{ variant: 'body2' }}
            />
          </ListItem>
          <ListItem sx={{ px: 0 }}>
            <ListItemText
              primary="Email"
              secondary={market.email}
              primaryTypographyProps={{ variant: 'body2' }}
              secondaryTypographyProps={{ variant: 'body2' }}
            />
          </ListItem>
        </List>
        
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
          <IconButton
            size="small"
            onClick={() => handleEdit(market)}
            sx={{ mr: 1 }}
          >
            <Edit />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleDelete(market.id)}
            color="error"
          >
            <Delete />
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  );
  
  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Gestão de Mercados
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Gerencie os mercados parceiros do sistema
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={handleOpen}
        >
          Novo Mercado
        </Button>
      </Box>
      
      {/* Lista de mercados */}
      <Grid container spacing={3}>
        {markets.map(renderMarketCard)}
      </Grid>
      
      {/* Dialog de criação/edição */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingMarket ? 'Editar Mercado' : 'Novo Mercado'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <TextField
              fullWidth
              label="Nome"
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Endereço"
              value={formData.address}
              onChange={(e) => handleInputChange('address', e.target.value)}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Telefone"
              value={formData.phone}
              onChange={(e) => handleInputChange('phone', e.target.value)}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>Tipo</InputLabel>
              <Select
                value={formData.type}
                onChange={(e) => handleInputChange('type', e.target.value)}
                label="Tipo"
              >
                <MenuItem value="supermarket">Supermercado</MenuItem>
                <MenuItem value="convenience">Conveniência</MenuItem>
                <MenuItem value="pharmacy">Farmácia</MenuItem>
                <MenuItem value="other">Outro</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth margin="normal">
              <InputLabel>Status</InputLabel>
              <Select
                value={formData.status}
                onChange={(e) => handleInputChange('status', e.target.value)}
                label="Status"
              >
                <MenuItem value="active">Ativo</MenuItem>
                <MenuItem value="inactive">Inativo</MenuItem>
                <MenuItem value="pending">Pendente</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancelar</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingMarket ? 'Atualizar' : 'Criar'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Markets;