/**
 * Hook personalizado para API otimizada
 */

import { useState, useEffect, useCallback, useRef } from 'react';

interface UseOptimizedApiOptions {
  retryAttempts?: number;
  retryDelay?: number;
  cache?: boolean;
  cacheTTL?: number;
}

interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  retryCount: number;
}

export const useOptimizedApi = <T>(
  apiCall: () => Promise<T>,
  options: UseOptimizedApiOptions = {}
) => {
  const {
    retryAttempts = 3,
    retryDelay = 1000,
    cache = true,
    cacheTTL = 300000, // 5 minutos
  } = options;

  const [state, setState] = useState<ApiState<T>>({
    data: null,
    loading: false,
    error: null,
    retryCount: 0,
  });

  const cacheRef = useRef<Map<string, { data: T; timestamp: number }>>(new Map());
  const abortControllerRef = useRef<AbortController | null>(null);

  const executeApiCall = useCallback(async (): Promise<T> => {
    // Verificar cache
    if (cache) {
      const cacheKey = apiCall.toString();
      const cached = cacheRef.current.get(cacheKey);
      
      if (cached && Date.now() - cached.timestamp < cacheTTL) {
        return cached.data;
      }
    }

    // Cancelar requisição anterior se existir
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Criar novo AbortController
    abortControllerRef.current = new AbortController();

    try {
      const result = await apiCall();
      
      // Salvar no cache
      if (cache) {
        const cacheKey = apiCall.toString();
        cacheRef.current.set(cacheKey, {
          data: result,
          timestamp: Date.now(),
        });
      }

      return result;
    } catch (error: any) {
      if (error.name === 'AbortError') {
        throw new Error('Requisição cancelada');
      }
      throw error;
    }
  }, [apiCall, cache, cacheTTL]);

  const execute = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const data = await executeApiCall();
      setState({
        data,
        loading: false,
        error: null,
        retryCount: 0,
      });
    } catch (error: any) {
      const currentRetryCount = state.retryCount;
      
      if (currentRetryCount < retryAttempts) {
        // Tentar novamente
        setTimeout(() => {
          setState(prev => ({ ...prev, retryCount: prev.retryCount + 1 }));
          execute();
        }, retryDelay);
      } else {
        setState({
          data: null,
          loading: false,
          error: error.message || 'Erro na requisição',
          retryCount: currentRetryCount,
        });
      }
    }
  }, [executeApiCall, state.retryCount, retryAttempts, retryDelay]);

  const clearCache = useCallback(() => {
    cacheRef.current.clear();
  }, []);

  const reset = useCallback(() => {
    setState({
      data: null,
      loading: false,
      error: null,
      retryCount: 0,
    });
  }, []);

  // Cleanup ao desmontar
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  return {
    ...state,
    execute,
    clearCache,
    reset,
  };
};

export default useOptimizedApi;


