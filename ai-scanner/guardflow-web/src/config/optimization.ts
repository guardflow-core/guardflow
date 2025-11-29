/**
 * Configurações de otimização do GuardFlow Web
 */

export const optimizationConfig = {
  // Configurações de API
  api: {
    timeout: 10000,
    retryAttempts: 3,
    retryDelay: 1000,
  },

  // Configurações de cache
  cache: {
    enabled: true,
    ttl: 300000, // 5 minutos
    maxSize: 100,
  },

  // Configurações de performance
  performance: {
    lazyLoading: true,
    imageOptimization: true,
    bundleSplitting: true,
  },

  // Configurações de monitoramento
  monitoring: {
    enabled: true,
    logLevel: 'info',
    trackErrors: true,
    trackPerformance: true,
  },

  // Configurações de desenvolvimento
  development: {
    hotReload: true,
    sourceMaps: true,
    debugMode: true,
  },

  // Configurações de produção
  production: {
    minify: true,
    compress: true,
    cacheHeaders: true,
  },
};

export default optimizationConfig;


