/**
 * GuardFlow GST Ecosystem SDK
 * SDK oficial para integração com o ecossistema GST
 */

const { ethers } = require('ethers');
const axios = require('axios');

class GuardFlowGST {
  constructor(config) {
    this.config = {
      network: config.network || 'mainnet',
      contracts: config.contracts || {},
      api: config.api || {},
      provider: config.provider || null,
      signer: config.signer || null,
      ...config
    };
    
    this.provider = this.config.provider || this._createProvider();
    this.signer = this.config.signer || this.provider.getSigner();
    
    this.contracts = {};
    this._initializeContracts();
  }

  _createProvider() {
    const rpcUrls = {
      mainnet: 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID',
      testnet: 'https://goerli.infura.io/v3/YOUR_PROJECT_ID',
      localhost: 'http://localhost:8545'
    };
    
    return new ethers.providers.JsonRpcProvider(rpcUrls[this.config.network]);
  }

  _initializeContracts() {
    // Em produção, os contratos seriam inicializados aqui
    // Por simplicidade, retornamos objetos mock
    this.contracts = {
      gstToken: null,
      invoiceNFT: null,
      marketplace: null,
      gamification: null,
      governance: null,
      nfeConverter: null,
      smartCart: null
    };
  }

  /**
   * Converter NFe em NFT
   * @param {Object} nfeData - Dados da NFe
   * @returns {Promise<Object>} Resultado da conversão
   */
  async convertNFEToNFT(nfeData) {
    try {
      const response = await axios.post('/api/convert-nfe', nfeData);
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao converter NFe: ${error.message}`);
    }
  }

  /**
   * Escanear produto no carrinho
   * @param {string} cartId - ID do carrinho
   * @param {string} productId - ID do produto
   * @param {number} quantity - Quantidade
   * @returns {Promise<Object>} Resultado do escaneamento
   */
  async scanProduct(cartId, productId, quantity) {
    try {
      const response = await axios.post('/api/scan-product', {
        cartId,
        productId,
        quantity
      });
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao escanear produto: ${error.message}`);
    }
  }

  /**
   * Obter NFTs do usuário
   * @param {string} address - Endereço do usuário
   * @returns {Promise<Array>} Lista de NFTs
   */
  async getUserNFTs(address) {
    try {
      const response = await axios.get(`/api/user/${address}/nfts`);
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao obter NFTs: ${error.message}`);
    }
  }

  /**
   * Obter dados do marketplace
   * @returns {Promise<Object>} Dados do marketplace
   */
  async getMarketplace() {
    try {
      const response = await axios.get('/api/marketplace');
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao obter marketplace: ${error.message}`);
    }
  }

  /**
   * Obter dados de gamificação
   * @param {string} address - Endereço do usuário
   * @returns {Promise<Object>} Dados de gamificação
   */
  async getGamification(address) {
    try {
      const response = await axios.get(`/api/gamification/${address}`);
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao obter gamificação: ${error.message}`);
    }
  }

  /**
   * Obter dados de governança
   * @returns {Promise<Object>} Dados de governança
   */
  async getGovernance() {
    try {
      const response = await axios.get('/api/governance');
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao obter governança: ${error.message}`);
    }
  }

  /**
   * Obter saldo de tokens GST
   * @param {string} address - Endereço do usuário
   * @returns {Promise<number>} Saldo de tokens
   */
  async getGSTBalance(address) {
    try {
      // Em produção, isso seria uma chamada para o contrato
      return 1000; // Mock
    } catch (error) {
      throw new Error(`Erro ao obter saldo GST: ${error.message}`);
    }
  }

  /**
   * Transferir tokens GST
   * @param {string} to - Endereço de destino
   * @param {number} amount - Quantidade
   * @returns {Promise<Object>} Resultado da transferência
   */
  async transferGST(to, amount) {
    try {
      // Em produção, isso seria uma transação no contrato
      return { success: true, txHash: '0x...' };
    } catch (error) {
      throw new Error(`Erro ao transferir GST: ${error.message}`);
    }
  }

  /**
   * Obter estatísticas do ecossistema
   * @returns {Promise<Object>} Estatísticas
   */
  async getEcosystemStats() {
    try {
      const response = await axios.get('/api/stats');
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao obter estatísticas: ${error.message}`);
    }
  }

  /**
   * Verificar saúde do sistema
   * @returns {Promise<Object>} Status de saúde
   */
  async healthCheck() {
    try {
      const response = await axios.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(`Erro no health check: ${error.message}`);
    }
  }
}

module.exports = GuardFlowGST;
