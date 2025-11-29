/**
 * Brand Configuration Component
 * Componente para configurar marca e slogan do GuardFlow
 */

import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid,
  Divider,
  Alert,
  Chip,
  Avatar,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Edit,
  Save,
  Cancel,
  Palette,
  Business,
  Tag,
  Description,
} from '@mui/icons-material';
import { useTheme } from '../contexts/ThemeContext';

interface BrandConfigData {
  name: string;
  slogan: string;
  tagline: string;
  description: string;
  logo: string;
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
}

const BrandConfig: React.FC = () => {
  const { brand, isDarkMode } = useTheme();
  const [isEditing, setIsEditing] = useState(false);
  const [config, setConfig] = useState<BrandConfigData>({
    name: brand.name,
    slogan: brand.slogan,
    tagline: brand.tagline,
    description: brand.description,
    logo: brand.logo,
    primaryColor: '#2196f3',
    secondaryColor: '#9c27b0',
    accentColor: '#4caf50',
  });
  const [previewOpen, setPreviewOpen] = useState(false);

  const handleSave = () => {
    // Aqui você salvaria as configurações no backend
    console.log('Salvando configurações da marca:', config);
    setIsEditing(false);
    // Simular salvamento
    setTimeout(() => {
      alert('Configurações da marca salvas com sucesso!');
    }, 1000);
  };

  const handleCancel = () => {
    setConfig({
      name: brand.name,
      slogan: brand.slogan,
      tagline: brand.tagline,
      description: brand.description,
      logo: brand.logo,
      primaryColor: '#2196f3',
      secondaryColor: '#9c27b0',
      accentColor: '#4caf50',
    });
    setIsEditing(false);
  };

  const handlePreview = () => {
    setPreviewOpen(true);
  };

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Business color="primary" />
            <Typography variant="h6" fontWeight={600}>
              Configuração da Marca
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            {!isEditing ? (
              <>
                <Button
                  startIcon={<Edit />}
                  onClick={() => setIsEditing(true)}
                  variant="outlined"
                  size="small"
                >
                  Editar
                </Button>
                <Button
                  startIcon={<Palette />}
                  onClick={handlePreview}
                  variant="outlined"
                  size="small"
                >
                  Preview
                </Button>
              </>
            ) : (
              <>
                <Button
                  startIcon={<Save />}
                  onClick={handleSave}
                  variant="contained"
                  size="small"
                  color="primary"
                >
                  Salvar
                </Button>
                <Button
                  startIcon={<Cancel />}
                  onClick={handleCancel}
                  variant="outlined"
                  size="small"
                >
                  Cancelar
                </Button>
              </>
            )}
          </Box>
        </Box>

        <Divider sx={{ mb: 3 }} />

        {isEditing ? (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Nome da Marca"
                value={config.name}
                onChange={(e) => setConfig({ ...config, name: e.target.value })}
                variant="outlined"
                size="small"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Slogan"
                value={config.slogan}
                onChange={(e) => setConfig({ ...config, slogan: e.target.value })}
                variant="outlined"
                size="small"
                placeholder="Ex: Agiliza aí suas compras!"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Tagline"
                value={config.tagline}
                onChange={(e) => setConfig({ ...config, tagline: e.target.value })}
                variant="outlined"
                size="small"
                placeholder="Ex: Sistema de Checkout Inteligente"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Descrição"
                value={config.description}
                onChange={(e) => setConfig({ ...config, description: e.target.value })}
                variant="outlined"
                size="small"
                multiline
                rows={2}
                placeholder="Ex: Revolucione sua experiência de compras com tecnologia ESG e sustentabilidade"
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Logo (Emoji)"
                value={config.logo}
                onChange={(e) => setConfig({ ...config, logo: e.target.value })}
                variant="outlined"
                size="small"
                placeholder="🚀"
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Cor Primária"
                value={config.primaryColor}
                onChange={(e) => setConfig({ ...config, primaryColor: e.target.value })}
                variant="outlined"
                size="small"
                type="color"
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Cor Secundária"
                value={config.secondaryColor}
                onChange={(e) => setConfig({ ...config, secondaryColor: e.target.value })}
                variant="outlined"
                size="small"
                type="color"
              />
            </Grid>
          </Grid>
        ) : (
          <Box>
            <Alert severity="info" sx={{ mb: 2 }}>
              <Typography variant="body2">
                Configure a identidade visual da sua marca para personalizar a experiência do usuário.
              </Typography>
            </Alert>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Box sx={{ textAlign: 'center', p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
                  <Avatar sx={{ width: 60, height: 60, mx: 'auto', mb: 1, bgcolor: 'primary.main' }}>
                    <Typography variant="h4">{brand.logo}</Typography>
                  </Avatar>
                  <Typography variant="h6" fontWeight={600}>
                    {brand.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Logo
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Box sx={{ textAlign: 'center', p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
                  <Tag color="primary" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="body1" fontWeight={600}>
                    {brand.slogan}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Slogan
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Box sx={{ textAlign: 'center', p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
                  <Description color="primary" sx={{ fontSize: 40, mb: 1 }} />
                  <Typography variant="body1" fontWeight={600}>
                    {brand.tagline}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Tagline
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Box sx={{ textAlign: 'center', p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
                  <Palette color="primary" sx={{ fontSize: 40, mb: 1 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, mb: 1 }}>
                    <Box sx={{ width: 20, height: 20, bgcolor: '#2196f3', borderRadius: '50%' }} />
                    <Box sx={{ width: 20, height: 20, bgcolor: '#9c27b0', borderRadius: '50%' }} />
                    <Box sx={{ width: 20, height: 20, bgcolor: '#4caf50', borderRadius: '50%' }} />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Cores
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Box>
        )}
      </CardContent>

      {/* Dialog de Preview */}
      <Dialog open={previewOpen} onClose={() => setPreviewOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Preview da Marca</DialogTitle>
        <DialogContent>
          <Box sx={{ textAlign: 'center', p: 3 }}>
            <Avatar sx={{ width: 80, height: 80, mx: 'auto', mb: 2, bgcolor: 'primary.main' }}>
              <Typography variant="h3">{brand.logo}</Typography>
            </Avatar>
            <Typography variant="h4" fontWeight={700} gutterBottom>
              {brand.name}
            </Typography>
            <Typography variant="h6" color="primary" gutterBottom>
              {brand.slogan}
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
              {brand.tagline}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {brand.description}
            </Typography>
            
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 3 }}>
              <Chip label="Checkout Inteligente" color="primary" />
              <Chip label="Tokenização ESG" color="secondary" />
              <Chip label="Sustentabilidade" color="success" />
            </Box>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPreviewOpen(false)}>Fechar</Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
};

export default BrandConfig;
