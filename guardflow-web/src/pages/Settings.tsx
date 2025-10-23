import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Switch,
  FormControlLabel,
  Button,
  Divider,
  Alert,
  Snackbar,
  Tabs,
  Tab,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  useTheme,
} from '@mui/material';
import {
  Save,
  Add,
  Edit,
  Delete,
  Security,
  Integration,
  Notifications,
  Theme,
  Language,
  Storage,
  Api,
  Webhook,
} from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { setTheme, setPrimaryColor, setSecondaryColor } from '../store/slices/themeSlice';

// Tipos
interface IntegrationConfig {
  id: string;
  name: string;
  type: 'payment' | 'erp' | 'analytics' | 'notification';
  status: 'active' | 'inactive' | 'error';
  apiKey: string;
  webhookUrl?: string;
  lastSync?: string;
}

// Componente Settings
const Settings: React.FC = () => {
  // Hooks
  const theme = useTheme();
  const dispatch = useDispatch();
  
  // Redux state
  const { mode, primaryColor, secondaryColor } = useSelector((state: RootState) => state.theme);
  
  // Local state
  const [selectedTab, setSelectedTab] = useState(0);
  const [settings, setSettings] = useState({
    // Sistema
    systemName: 'Agilizia AI',
    systemVersion: '1.0.0',
    maintenanceMode: false,
    debugMode: false,
    
    // Notificações
    notifications: {
      email: true,
      push: true,
      sms: false,
      webhook: true,
    },
    
    // Integrações
    integrations: [] as IntegrationConfig[],
    
    // API
    apiRateLimit: 1000,
    apiTimeout: 30,
    corsEnabled: true,
    
    // Segurança
    passwordMinLength: 8,
    sessionTimeout: 30,
    twoFactorEnabled: false,
    
    // Backup
    backupEnabled: true,
    backupFrequency: 'daily',
    backupRetention: 30,
  });
  
  const [openIntegration, setOpenIntegration] = useState(false);
  const [editingIntegration, setEditingIntegration] = useState<IntegrationConfig | null>(null);
  const [integrationForm, setIntegrationForm] = useState({
    name: '',
    type: 'payment' as const,
    apiKey: '',
    webhookUrl: '',
  });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });
  
  // Effects
  useEffect(() => {
    // Simular carregamento de configurações
    setSettings(prev => ({
      ...prev,
      integrations: [
        {
          id: '1',
          name: 'Mercado Pago',
          type: 'payment',
          status: 'active',
          apiKey: '***',
          webhookUrl: 'https://api.agilizia.ai/webhooks/mercadopago',
          lastSync: '2024-01-20T10:30:00Z',
        },
        {
          id: '2',
          name: 'SAP ERP',
          type: 'erp',
          status: 'active',
          apiKey: '***',
          lastSync: '2024-01-20T10:25:00Z',
        },
        {
          id: '3',
          name: 'Google Analytics',
          type: 'analytics',
          status: 'inactive',
          apiKey: '***',
        },
      ],
    }));
  }, []);
  
  // Handlers
  const handleTabChange = (event: any, newValue: number) => {
    setSelectedTab(newValue);
  };
  
  const handleSettingChange = (key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [key]: value,
    }));
  };
  
  const handleNestedSettingChange = (parent: string, key: string, value: any) => {
    setSettings(prev => ({
      ...prev,
      [parent]: {
        ...prev[parent as keyof typeof prev],
        [key]: value,
      },
    }));
  };
  
  const handleSave = () => {
    // Simular salvamento
    setSnackbar({ open: true, message: 'Configurações salvas com sucesso!', severity: 'success' });
  };
  
  const handleOpenIntegration = () => {
    setEditingIntegration(null);
    setIntegrationForm({ name: '', type: 'payment', apiKey: '', webhookUrl: '' });
    setOpenIntegration(true);
  };
  
  const handleEditIntegration = (integration: IntegrationConfig) => {
    setEditingIntegration(integration);
    setIntegrationForm({
      name: integration.name,
      type: integration.type,
      apiKey: integration.apiKey,
      webhookUrl: integration.webhookUrl || '',
    });
    setOpenIntegration(true);
  };
  
  const handleCloseIntegration = () => {
    setOpenIntegration(false);
    setEditingIntegration(null);
  };
  
  const handleSaveIntegration = () => {
    if (editingIntegration) {
      // Atualizar integração existente
      setSettings(prev => ({
        ...prev,
        integrations: prev.integrations.map(integration =>
          integration.id === editingIntegration.id
            ? { ...integration, ...integrationForm }
            : integration
        ),
      }));
    } else {
      // Criar nova integração
      const newIntegration: IntegrationConfig = {
        id: Date.now().toString(),
        ...integrationForm,
        status: 'active',
      };
      setSettings(prev => ({
        ...prev,
        integrations: [...prev.integrations, newIntegration],
      }));
    }
    handleCloseIntegration();
    setSnackbar({ open: true, message: 'Integração salva com sucesso!', severity: 'success' });
  };
  
  const handleDeleteIntegration = (id: string) => {
    setSettings(prev => ({
      ...prev,
      integrations: prev.integrations.filter(integration => integration.id !== id),
    }));
    setSnackbar({ open: true, message: 'Integração removida!', severity: 'success' });
  };
  
  const handleThemeChange = (color: string, type: 'primary' | 'secondary') => {
    if (type === 'primary') {
      dispatch(setPrimaryColor(color));
    } else {
      dispatch(setSecondaryColor(color));
    }
  };
  
  // Renderizar status da integração
  const renderIntegrationStatus = (status: string) => {
    const statusConfig = {
      active: { color: 'success', label: 'Ativo' },
      inactive: { color: 'default', label: 'Inativo' },
      error: { color: 'error', label: 'Erro' },
    };
    
    const config = statusConfig[status as keyof typeof statusConfig];
    
    return (
      <Chip
        label={config.label}
        color={config.color as any}
        size="small"
      />
    );
  };
  
  // Renderizar integração
  const renderIntegration = (integration: IntegrationConfig) => (
    <ListItem key={integration.id} sx={{ px: 0 }}>
      <ListItemText
        primary={integration.name}
        secondary={`${integration.type} • ${integration.lastSync ? `Última sincronização: ${new Date(integration.lastSync).toLocaleString()}` : 'Nunca sincronizado'}`}
      />
      <ListItemSecondaryAction>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {renderIntegrationStatus(integration.status)}
          <IconButton
            size="small"
            onClick={() => handleEditIntegration(integration)}
          >
            <Edit />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleDeleteIntegration(integration.id)}
            color="error"
          >
            <Delete />
          </IconButton>
        </Box>
      </ListItemSecondaryAction>
    </ListItem>
  );
  
  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Configurações
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Gerencie as configurações do sistema e integrações
        </Typography>
      </Box>
      
      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={selectedTab} onChange={handleTabChange}>
          <Tab label="Sistema" />
          <Tab label="Integrações" />
          <Tab label="Notificações" />
          <Tab label="Segurança" />
          <Tab label="Aparência" />
        </Tabs>
      </Box>
      
      {/* Conteúdo baseado na tab selecionada */}
      {selectedTab === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Configurações Gerais
                </Typography>
                <TextField
                  fullWidth
                  label="Nome do Sistema"
                  value={settings.systemName}
                  onChange={(e) => handleSettingChange('systemName', e.target.value)}
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="Versão"
                  value={settings.systemVersion}
                  onChange={(e) => handleSettingChange('systemVersion', e.target.value)}
                  margin="normal"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.maintenanceMode}
                      onChange={(e) => handleSettingChange('maintenanceMode', e.target.checked)}
                    />
                  }
                  label="Modo de Manutenção"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.debugMode}
                      onChange={(e) => handleSettingChange('debugMode', e.target.checked)}
                    />
                  }
                  label="Modo Debug"
                />
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Configurações de API
                </Typography>
                <TextField
                  fullWidth
                  label="Rate Limit (req/min)"
                  type="number"
                  value={settings.apiRateLimit}
                  onChange={(e) => handleSettingChange('apiRateLimit', parseInt(e.target.value))}
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="Timeout (segundos)"
                  type="number"
                  value={settings.apiTimeout}
                  onChange={(e) => handleSettingChange('apiTimeout', parseInt(e.target.value))}
                  margin="normal"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.corsEnabled}
                      onChange={(e) => handleSettingChange('corsEnabled', e.target.checked)}
                    />
                  }
                  label="CORS Habilitado"
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
      
      {selectedTab === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Integrações
                  </Typography>
                  <Button
                    variant="contained"
                    startIcon={<Add />}
                    onClick={handleOpenIntegration}
                  >
                    Nova Integração
                  </Button>
                </Box>
                <List>
                  {settings.integrations.map(renderIntegration)}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
      
      {selectedTab === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Configurações de Notificação
                </Typography>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.email}
                      onChange={(e) => handleNestedSettingChange('notifications', 'email', e.target.checked)}
                    />
                  }
                  label="Email"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.push}
                      onChange={(e) => handleNestedSettingChange('notifications', 'push', e.target.checked)}
                    />
                  }
                  label="Push Notifications"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.sms}
                      onChange={(e) => handleNestedSettingChange('notifications', 'sms', e.target.checked)}
                    />
                  }
                  label="SMS"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.notifications.webhook}
                      onChange={(e) => handleNestedSettingChange('notifications', 'webhook', e.target.checked)}
                    />
                  }
                  label="Webhook"
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
      
      {selectedTab === 3 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Configurações de Segurança
                </Typography>
                <TextField
                  fullWidth
                  label="Tamanho mínimo da senha"
                  type="number"
                  value={settings.passwordMinLength}
                  onChange={(e) => handleSettingChange('passwordMinLength', parseInt(e.target.value))}
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="Timeout da sessão (minutos)"
                  type="number"
                  value={settings.sessionTimeout}
                  onChange={(e) => handleSettingChange('sessionTimeout', parseInt(e.target.value))}
                  margin="normal"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.twoFactorEnabled}
                      onChange={(e) => handleSettingChange('twoFactorEnabled', e.target.checked)}
                    />
                  }
                  label="Autenticação de dois fatores"
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
      
      {selectedTab === 4 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Configurações de Aparência
                </Typography>
                <TextField
                  fullWidth
                  label="Cor Primária"
                  type="color"
                  value={primaryColor}
                  onChange={(e) => handleThemeChange(e.target.value, 'primary')}
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="Cor Secundária"
                  type="color"
                  value={secondaryColor}
                  onChange={(e) => handleThemeChange(e.target.value, 'secondary')}
                  margin="normal"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={mode === 'dark'}
                      onChange={(e) => dispatch(setTheme(e.target.checked ? 'dark' : 'light'))}
                    />
                  }
                  label="Modo Escuro"
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
      
      {/* Botão salvar */}
      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          startIcon={<Save />}
          onClick={handleSave}
          size="large"
        >
          Salvar Configurações
        </Button>
      </Box>
      
      {/* Dialog de integração */}
      <Dialog open={openIntegration} onClose={handleCloseIntegration} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingIntegration ? 'Editar Integração' : 'Nova Integração'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <TextField
              fullWidth
              label="Nome"
              value={integrationForm.name}
              onChange={(e) => setIntegrationForm(prev => ({ ...prev, name: e.target.value }))}
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>Tipo</InputLabel>
              <Select
                value={integrationForm.type}
                onChange={(e) => setIntegrationForm(prev => ({ ...prev, type: e.target.value as any }))}
                label="Tipo"
              >
                <MenuItem value="payment">Pagamento</MenuItem>
                <MenuItem value="erp">ERP</MenuItem>
                <MenuItem value="analytics">Analytics</MenuItem>
                <MenuItem value="notification">Notificação</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="API Key"
              value={integrationForm.apiKey}
              onChange={(e) => setIntegrationForm(prev => ({ ...prev, apiKey: e.target.value }))}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Webhook URL"
              value={integrationForm.webhookUrl}
              onChange={(e) => setIntegrationForm(prev => ({ ...prev, webhookUrl: e.target.value }))}
              margin="normal"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseIntegration}>Cancelar</Button>
          <Button onClick={handleSaveIntegration} variant="contained">
            {editingIntegration ? 'Atualizar' : 'Criar'}
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Snackbar */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
      >
        <Alert
          onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
          severity={snackbar.severity}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Settings;