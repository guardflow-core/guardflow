// GuardFlow Web - Configuração Unificada
const CONFIG = {
  API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
  FEATURES: {
    SCANNER: true,
    ESG_DASHBOARD: true,
    PAYMENT_PIX: true,
    TOKEN_GST: true
  },
  THEME: {
    PRIMARY_COLOR: '#2E7D32',
    SECONDARY_COLOR: '#4CAF50',
    ACCENT_COLOR: '#FFC107'
  }
};

export default CONFIG;


