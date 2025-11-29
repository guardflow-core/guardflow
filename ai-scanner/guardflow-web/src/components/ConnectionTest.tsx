/**
 * Componente de teste de conexão moderno
 */

import React, { useState, useEffect } from 'react';
import { 
  Button, 
  Card, 
  CardContent, 
  Typography, 
  Box, 
  Alert,
  Chip,
  LinearProgress,
  Fade
} from '@mui/material';
import { 
  CheckCircle, 
  Error, 
  Refresh, 
  Speed,
  Wifi,
  WifiOff
} from '@mui/icons-material';
import { testConnection } from '../utils/testConnection';

const ConnectionTest: React.FC = () => {
  const [testing, setTesting] = useState(false);
  const [result, setResult] = useState<{ success: boolean; data?: any; error?: string } | null>(null);
  const [autoTest, setAutoTest] = useState(true);

  useEffect(() => {
    if (autoTest) {
      handleTest();
    }
  }, [autoTest]);

  const handleTest = async () => {
    setTesting(true);
    setResult(null);
    
    try {
      const testResult = await testConnection();
      setResult(testResult);
    } catch (error: any) {
      setResult({
        success: false,
        error: error.message,
      });
    } finally {
      setTesting(false);
    }
  };

  const getStatusIcon = () => {
    if (testing) return <Refresh sx={{ animation: 'spin 1s linear infinite' }} />;
    if (result?.success) return <CheckCircle color="success" />;
    return <Error color="error" />;
  };

  const getStatusColor = () => {
    if (testing) return 'info';
    if (result?.success) return 'success';
    return 'error';
  };

  const getStatusText = () => {
    if (testing) return 'Testando conexão...';
    if (result?.success) return 'Conectado';
    return 'Desconectado';
  };

  return (
    <Card sx={{ 
      mb: 3, 
      background: result?.success 
        ? 'linear-gradient(135deg, #4caf50 0%, #45a049 100%)' 
        : 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)',
      color: 'white',
      transition: 'all 0.3s ease'
    }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box display="flex" alignItems="center" gap={2}>
            <Box display="flex" alignItems="center" gap={1}>
              {result?.success ? <Wifi /> : <WifiOff />}
              <Typography variant="h6" fontWeight="bold">
                Status da Conexão
              </Typography>
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
          
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={handleTest}
            disabled={testing}
            sx={{ 
              borderColor: 'rgba(255,255,255,0.5)', 
              color: 'white',
              '&:hover': { 
                borderColor: 'white', 
                bgcolor: 'rgba(255,255,255,0.1)' 
              }
            }}
          >
            {testing ? 'Testando...' : 'Testar'}
          </Button>
        </Box>

        {testing && (
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

        <Fade in={!!result}>
          <Box>
            {result?.success ? (
              <Alert 
                severity="success" 
                sx={{ 
                  bgcolor: 'rgba(255,255,255,0.1)',
                  color: 'white',
                  '& .MuiAlert-icon': { color: 'white' }
                }}
              >
                <Typography variant="body1" fontWeight="bold">
                  ✅ Conexão estabelecida com sucesso!
                </Typography>
                <Box mt={1}>
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    <strong>Serviço:</strong> {result.data?.service}
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    <strong>Status:</strong> {result.data?.status}
                  </Typography>
                  <Typography variant="body2" sx={{ opacity: 0.9 }}>
                    <strong>Versão:</strong> {result.data?.version}
                  </Typography>
                </Box>
              </Alert>
            ) : result ? (
              <Alert 
                severity="error"
                sx={{ 
                  bgcolor: 'rgba(255,255,255,0.1)',
                  color: 'white',
                  '& .MuiAlert-icon': { color: 'white' }
                }}
              >
                <Typography variant="body1" fontWeight="bold">
                  ❌ Erro na conexão
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  {result.error}
                </Typography>
              </Alert>
            ) : null}
          </Box>
        </Fade>

        {result?.success && (
          <Box display="flex" alignItems="center" gap={1} mt={2}>
            <Speed sx={{ fontSize: 16 }} />
            <Typography variant="caption" sx={{ opacity: 0.8 }}>
              Sistema operacional • Latência baixa • Alta disponibilidade
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default ConnectionTest;