/**
 * GuardPass Integration Component
 * Componente para gerenciar a integração com GuardPass
 */

import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Chip,
  Alert,
  LinearProgress,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Security,
  CheckCircle,
  Error,
  Refresh,
  Settings,
  Sync,
  CloudSync,
  Shield,
  Key,
  Person,
} from '@mui/icons-material';
import { guardpassService, GuardPassUser } from '../services/guardpassService';

interface GuardPassStatus {
  connected: boolean;
  status: string;
  version?: string;
  user?: GuardPassUser;
  permissions: string[];
}

const GuardPassIntegration: React.FC = () => {
  const [status, setStatus] = useState<GuardPassStatus>({
    connected: false,
    status: 'disconnected',
    permissions: []
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAuthDialog, setShowAuthDialog] = useState(false);

  useEffect(() => {
    checkGuardPassConnection();
  }, []);

  const checkGuardPassConnection = async () => {
    setLoading(true);
    setError(null);

    try {
      // Verificar conexão básica
      const connectionStatus = await guardpassService.checkConnection();
      
      if (connectionStatus.connected) {
        // Se conectado, tentar obter dados do usuário
        try {
          const user = await guardpassService.getCurrentUser();
          setStatus({
            connected: true,
            status: 'authenticated',
            version: connectionStatus.version,
            user,
            permissions: user.permissions
          });
        } catch (userError) {
          setStatus({
            connected: true,
            status: 'connected',
            version: connectionStatus.version,
            permissions: []
          });
        }
      } else {
        setStatus({
          connected: false,
          status: connectionStatus.status,
          permissions: []
        });
      }
    } catch (err: any) {
      setError(err.message);
      setStatus({
        connected: false,
        status: 'error',
        permissions: []
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAuthenticate = async () => {
    setLoading(true);
    setError(null);

    try {
      await guardpassService.authenticate();
      await checkGuardPassConnection();
      setShowAuthDialog(false);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSyncESG = async () => {
    setLoading(true);
    setError(null);

    try {
      // Dados ESG de exemplo para sincronização
      const esgData = {
        total_score: 87,
        total_points: 2450,
        total_tokens: 125,
        last_updated: new Date().toISOString()
      };

      const success = await guardpassService.syncESGData(esgData);
      
      if (success) {
        setError(null);
        // Mostrar sucesso
      } else {
        setError('Falha na sincronização ESG');
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = () => {
    if (status.connected && status.status === 'authenticated') return 'success';
    if (status.connected) return 'warning';
    return 'error';
  };

  const getStatusIcon = () => {
    if (status.connected && status.status === 'authenticated') return <CheckCircle />;
    if (status.connected) return <CloudSync />;
    return <Error />;
  };

  const getStatusText = () => {
    if (status.connected && status.status === 'authenticated') return 'Autenticado';
    if (status.connected) return 'Conectado';
    return 'Desconectado';
  };

  return (
    <Card sx={{ 
      mb: 3, 
      background: status.connected 
        ? 'linear-gradient(135deg, #4caf50 0%, #45a049 100%)' 
        : 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)',
      color: 'white',
      transition: 'all 0.3s ease'
    }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box display="flex" alignItems="center" gap={2}>
            <Shield sx={{ fontSize: 32 }} />
            <Box>
              <Typography variant="h6" fontWeight="bold">
                GuardPass Integration
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>
                Ecossistema de Segurança e Autenticação
              </Typography>
            </Box>
          </Box>
          
          <Chip
            icon={getStatusIcon()}
            label={getStatusText()}
            color={getStatusColor()}
            variant="filled"
            sx={{ 
              bgcolor: 'rgba(255,255,255,0.2)',
              color: 'white',
              '& .MuiChip-icon': { color: 'white' }
            }}
          />
        </Box>

        {loading && (
          <Box sx={{ mb: 2 }}>
            <LinearProgress 
              sx={{ 
                height: 4, 
                borderRadius: 2,
                bgcolor: 'rgba(255,255,255,0.2)',
                '& .MuiLinearProgress-bar': {
                  bgcolor: 'white'
                }
              }} 
            />
          </Box>
        )}

        {error && (
          <Alert 
            severity="error" 
            sx={{ 
              mb: 2,
              bgcolor: 'rgba(255,255,255,0.1)',
              color: 'white',
              '& .MuiAlert-icon': { color: 'white' }
            }}
          >
            {error}
          </Alert>
        )}

        {status.connected && status.user && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" sx={{ opacity: 0.9, mb: 1 }}>
              <strong>Usuário:</strong> {status.user.name} ({status.user.email})
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.9, mb: 1 }}>
              <strong>Função:</strong> {status.user.role}
            </Typography>
            {status.version && (
              <Typography variant="body2" sx={{ opacity: 0.9 }}>
                <strong>Versão GuardPass:</strong> {status.version}
              </Typography>
            )}
          </Box>
        )}

        <Box display="flex" gap={2} flexWrap="wrap">
          {!status.connected ? (
            <Button
              variant="contained"
              startIcon={<Key />}
              onClick={() => setShowAuthDialog(true)}
              sx={{ 
                bgcolor: 'rgba(255,255,255,0.2)', 
                '&:hover': { bgcolor: 'rgba(255,255,255,0.3)' },
                color: 'white',
                border: '1px solid rgba(255,255,255,0.3)'
              }}
            >
              Conectar ao GuardPass
            </Button>
          ) : (
            <>
              <Button
                variant="outlined"
                startIcon={<Sync />}
                onClick={handleSyncESG}
                disabled={loading}
                sx={{ 
                  borderColor: 'rgba(255,255,255,0.5)', 
                  color: 'white',
                  '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
                }}
              >
                Sincronizar ESG
              </Button>
              
              <Button
                variant="outlined"
                startIcon={<Refresh />}
                onClick={checkGuardPassConnection}
                disabled={loading}
                sx={{ 
                  borderColor: 'rgba(255,255,255,0.5)', 
                  color: 'white',
                  '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' }
                }}
              >
                Atualizar Status
              </Button>
            </>
          )}
        </Box>

        {status.permissions.length > 0 && (
          <>
            <Divider sx={{ my: 2, bgcolor: 'rgba(255,255,255,0.2)' }} />
            <Typography variant="body2" sx={{ opacity: 0.9, mb: 1 }}>
              <strong>Permissões:</strong>
            </Typography>
            <Box display="flex" gap={1} flexWrap="wrap">
              {status.permissions.map((permission, index) => (
                <Chip
                  key={index}
                  label={permission}
                  size="small"
                  sx={{ 
                    bgcolor: 'rgba(255,255,255,0.2)',
                    color: 'white',
                    fontSize: '0.75rem'
                  }}
                />
              ))}
            </Box>
          </>
        )}
      </CardContent>

      {/* Dialog de Autenticação */}
      <Dialog open={showAuthDialog} onClose={() => setShowAuthDialog(false)}>
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <Security />
            <Typography variant="h6">Conectar ao GuardPass</Typography>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant="body1" sx={{ mb: 2 }}>
            Para conectar ao GuardPass, você precisa de credenciais válidas.
          </Typography>
          <List>
            <ListItem>
              <ListItemIcon>
                <Person />
              </ListItemIcon>
              <ListItemText 
                primary="Autenticação OAuth2"
                secondary="Login seguro com GuardPass"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Shield />
              </ListItemIcon>
              <ListItemText 
                primary="Permissões de Acesso"
                secondary="Controle de acesso granular"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CloudSync />
              </ListItemIcon>
              <ListItemText 
                primary="Sincronização de Dados"
                secondary="Integração com ecossistema GuardPass"
              />
            </ListItem>
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAuthDialog(false)}>
            Cancelar
          </Button>
          <Button 
            variant="contained" 
            onClick={handleAuthenticate}
            disabled={loading}
            startIcon={<Key />}
          >
            {loading ? 'Conectando...' : 'Conectar'}
          </Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
};

export default GuardPassIntegration;
