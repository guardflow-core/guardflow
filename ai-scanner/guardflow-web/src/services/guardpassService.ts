/**
 * GuardPass Integration Service
 * Serviço de integração com o ecossistema GuardPass
 */

export interface GuardPassUser {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'manager';
  permissions: string[];
  guardpass_token: string;
  expires_at: string;
}

export interface GuardPassAuth {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  scope: string[];
}

export interface GuardPassConfig {
  api_url: string;
  client_id: string;
  client_secret: string;
  redirect_uri: string;
  scopes: string[];
}

class GuardPassService {
  private config: GuardPassConfig;
  private baseURL: string;

  constructor() {
    this.config = {
      api_url: process.env.REACT_APP_GUARDPASS_API_URL || 'https://api.guardpass.com',
      client_id: process.env.REACT_APP_GUARDPASS_CLIENT_ID || 'guardflow-client',
      client_secret: process.env.REACT_APP_GUARDPASS_CLIENT_SECRET || '',
      redirect_uri: process.env.REACT_APP_GUARDPASS_REDIRECT_URI || 'http://localhost:3000/auth/callback',
      scopes: ['read:profile', 'read:permissions', 'write:scans', 'read:esg']
    };
    this.baseURL = this.config.api_url;
  }

  /**
   * Autenticação OAuth2 com GuardPass
   */
  async authenticate(): Promise<GuardPassAuth> {
    try {
      const response = await fetch(`${this.baseURL}/oauth/authorize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          client_id: this.config.client_id,
          client_secret: this.config.client_secret,
          grant_type: 'client_credentials',
          scope: this.config.scopes.join(' ')
        })
      });

      if (!response.ok) {
        throw new Error(`GuardPass authentication failed: ${response.statusText}`);
      }

      const authData: GuardPassAuth = await response.json();
      
      // Armazenar tokens no localStorage
      localStorage.setItem('guardpass_access_token', authData.access_token);
      localStorage.setItem('guardpass_refresh_token', authData.refresh_token);
      localStorage.setItem('guardpass_expires_at', 
        (Date.now() + authData.expires_in * 1000).toString()
      );

      return authData;
    } catch (error) {
      console.error('GuardPass authentication error:', error);
      throw error;
    }
  }

  /**
   * Obter informações do usuário autenticado
   */
  async getCurrentUser(): Promise<GuardPassUser> {
    try {
      const token = this.getValidToken();
      
      const response = await fetch(`${this.baseURL}/api/v1/user/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to get user info: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('GuardPass getCurrentUser error:', error);
      throw error;
    }
  }

  /**
   * Verificar permissões do usuário
   */
  async checkPermission(permission: string): Promise<boolean> {
    try {
      const user = await this.getCurrentUser();
      return user.permissions.includes(permission);
    } catch (error) {
      console.error('GuardPass permission check error:', error);
      return false;
    }
  }

  /**
   * Sincronizar dados ESG com GuardPass
   */
  async syncESGData(esgData: any): Promise<boolean> {
    try {
      const token = this.getValidToken();
      
      const response = await fetch(`${this.baseURL}/api/v1/esg/sync`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(esgData)
      });

      return response.ok;
    } catch (error) {
      console.error('GuardPass ESG sync error:', error);
      return false;
    }
  }

  /**
   * Enviar dados de scan para GuardPass
   */
  async sendScanData(scanData: any): Promise<boolean> {
    try {
      const token = this.getValidToken();
      
      const response = await fetch(`${this.baseURL}/api/v1/scans`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(scanData)
      });

      return response.ok;
    } catch (error) {
      console.error('GuardPass scan data error:', error);
      return false;
    }
  }

  /**
   * Obter configurações do GuardPass
   */
  async getGuardPassConfig(): Promise<any> {
    try {
      const token = this.getValidToken();
      
      const response = await fetch(`${this.baseURL}/api/v1/config`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to get GuardPass config: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('GuardPass config error:', error);
      throw error;
    }
  }

  /**
   * Verificar status da conexão com GuardPass
   */
  async checkConnection(): Promise<{ connected: boolean; status: string; version?: string }> {
    try {
      const response = await fetch(`${this.baseURL}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        return {
          connected: true,
          status: 'online',
          version: data.version
        };
      } else {
        return {
          connected: false,
          status: 'offline'
        };
      }
    } catch (error) {
      return {
        connected: false,
        status: 'error'
      };
    }
  }

  /**
   * Obter token válido (com refresh automático)
   */
  private getValidToken(): string {
    const accessToken = localStorage.getItem('guardpass_access_token');
    const expiresAt = localStorage.getItem('guardpass_expires_at');
    
    if (!accessToken || !expiresAt) {
      throw new Error('No valid GuardPass token found');
    }

    // Verificar se o token expirou
    if (Date.now() >= parseInt(expiresAt)) {
      // Token expirado, tentar refresh
      this.refreshToken();
      throw new Error('Token expired, refresh required');
    }

    return accessToken;
  }

  /**
   * Renovar token de acesso
   */
  private async refreshToken(): Promise<void> {
    try {
      const refreshToken = localStorage.getItem('guardpass_refresh_token');
      
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await fetch(`${this.baseURL}/oauth/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          grant_type: 'refresh_token',
          refresh_token: refreshToken,
          client_id: this.config.client_id,
          client_secret: this.config.client_secret
        })
      });

      if (response.ok) {
        const authData: GuardPassAuth = await response.json();
        
        localStorage.setItem('guardpass_access_token', authData.access_token);
        localStorage.setItem('guardpass_refresh_token', authData.refresh_token);
        localStorage.setItem('guardpass_expires_at', 
          (Date.now() + authData.expires_in * 1000).toString()
        );
      } else {
        // Refresh falhou, limpar tokens
        this.logout();
        throw new Error('Token refresh failed');
      }
    } catch (error) {
      console.error('GuardPass token refresh error:', error);
      this.logout();
      throw error;
    }
  }

  /**
   * Logout do GuardPass
   */
  logout(): void {
    localStorage.removeItem('guardpass_access_token');
    localStorage.removeItem('guardpass_refresh_token');
    localStorage.removeItem('guardpass_expires_at');
  }

  /**
   * Verificar se está autenticado
   */
  isAuthenticated(): boolean {
    const accessToken = localStorage.getItem('guardpass_access_token');
    const expiresAt = localStorage.getItem('guardpass_expires_at');
    
    return !!(accessToken && expiresAt && Date.now() < parseInt(expiresAt));
  }
}

// Instância singleton
export const guardpassService = new GuardPassService();
export default guardpassService;
