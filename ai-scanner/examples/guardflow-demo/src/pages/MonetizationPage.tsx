import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface Conversion {
  id: string;
  invoice_number: string;
  conversion_type: 'cash' | 'esg';
  original_amount: number;
  conversion_amount: number;
  guardflow_fee: number;
  user_amount: number;
  status: string;
  created_at: string;
}

interface ESGAsset {
  id: string;
  invoice_number: string;
  esg_value: number;
  esg_score: number;
  category: string;
  carbon_offset_kg: number;
  status: string;
  created_at: string;
}

const MonetizationPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [conversions, setConversions] = useState<Conversion[]>([]);
  const [esgAssets, setEsgAssets] = useState<ESGAsset[]>([]);
  const [stats, setStats] = useState({
    total_conversions: 0,
    total_cash_converted: 0,
    total_esg_value: 0,
    total_fees_paid: 0,
    esg_tokens: 0,
    cash_balance: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isAuthenticated) {
      loadData();
    }
  }, [isAuthenticated]);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Simular carregamento de dados
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Dados mock para demonstração
      setConversions([
        {
          id: '1',
          invoice_number: 'GF20250101000001',
          conversion_type: 'cash',
          original_amount: 150.00,
          conversion_amount: 142.50,
          guardflow_fee: 7.50,
          user_amount: 135.00,
          status: 'completed',
          created_at: '2025-01-01T10:00:00Z'
        },
        {
          id: '2',
          invoice_number: 'GF20250101000002',
          conversion_type: 'esg',
          original_amount: 200.00,
          conversion_amount: 180.00,
          guardflow_fee: 0.00,
          user_amount: 180.00,
          status: 'completed',
          created_at: '2025-01-01T11:00:00Z'
        }
      ]);

      setEsgAssets([
        {
          id: '1',
          invoice_number: 'GF20250101000002',
          esg_value: 180.00,
          esg_score: 90,
          category: 'sustainability',
          carbon_offset_kg: 90.0,
          status: 'active',
          created_at: '2025-01-01T11:00:00Z'
        }
      ]);

      setStats({
        total_conversions: 2,
        total_cash_converted: 135.00,
        total_esg_value: 180.00,
        total_fees_paid: 7.50,
        esg_tokens: 18,
        cash_balance: 135.00
      });

    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleConvertToCash = (transactionId: string) => {
    alert(`Funcionalidade de conversão em dinheiro será implementada para transação ${transactionId}`);
  };

  const handleConvertToESG = (transactionId: string) => {
    alert(`Funcionalidade de conversão em ESG será implementada para transação ${transactionId}`);
  };

  const handleSellESGAsset = (assetId: string) => {
    alert(`Funcionalidade de venda de ativo ESG será implementada para ativo ${assetId}`);
  };

  if (!isAuthenticated) {
    return (
      <div>
        <div className="header">
          <h1>Monetização GuardFlow</h1>
          <p>Converta suas notas fiscais em dinheiro ou ativos ESG</p>
        </div>

        <div className="nav">
          <button className="nav-button" onClick={() => navigate('/')}>
            🏠 Início
          </button>
        </div>

        <div className="main-content">
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>💰</div>
            <h2>Faça Login</h2>
            <p style={{ marginBottom: '2rem', color: '#666' }}>
              Entre na sua conta para acessar as funcionalidades de monetização
            </p>
            <button 
              className="button" 
              onClick={() => navigate('/profile')}
            >
              Fazer Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div>
        <div className="header">
          <h1>Monetização GuardFlow</h1>
          <p>Carregando seus dados de monetização...</p>
        </div>
        <div className="main-content">
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <div style={{ 
              width: '50px', 
              height: '50px', 
              border: '3px solid #4CAF50',
              borderTop: '3px solid transparent',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              margin: '0 auto 1rem'
            }}></div>
            <p>Carregando...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="header">
        <h1>Monetização GuardFlow</h1>
        <p>Converta suas notas fiscais em dinheiro ou ativos ESG</p>
      </div>

      <div className="nav">
        <button className="nav-button" onClick={() => navigate('/')}>
          🏠 Início
        </button>
        <button className="nav-button" onClick={() => navigate('/cart')}>
          🛒 Carrinho
        </button>
        <button className="nav-button secondary" onClick={() => navigate('/profile')}>
          👤 Perfil
        </button>
      </div>

      <div className="main-content">
        {/* Estatísticas */}
        <div className="card">
          <h2>Suas Estatísticas de Monetização</h2>
          <div className="stats">
            <div className="stat-item">
              <div className="stat-number">{stats.total_conversions}</div>
              <div className="stat-label">Conversões</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">R$ {stats.total_cash_converted.toFixed(2)}</div>
              <div className="stat-label">Dinheiro Convertido</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">R$ {stats.total_esg_value.toFixed(2)}</div>
              <div className="stat-label">Valor ESG</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{stats.esg_tokens}</div>
              <div className="stat-label">Tokens ESG</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">R$ {stats.cash_balance.toFixed(2)}</div>
              <div className="stat-label">Saldo Atual</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">R$ {stats.total_fees_paid.toFixed(2)}</div>
              <div className="stat-label">Taxas Pagas</div>
            </div>
          </div>
        </div>

        {/* Conversões */}
        <div className="card">
          <h2>Histórico de Conversões</h2>
          {conversions.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#666', padding: '2rem' }}>
              Nenhuma conversão realizada ainda
            </p>
          ) : (
            <div style={{ display: 'grid', gap: '1rem' }}>
              {conversions.map((conversion) => (
                <div key={conversion.id} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem',
                  border: '1px solid #eee',
                  borderRadius: '8px',
                  background: conversion.status === 'completed' ? '#f8fff8' : '#fff8f8'
                }}>
                  <div>
                    <div style={{ fontWeight: 'bold', marginBottom: '0.25rem' }}>
                      {conversion.invoice_number}
                    </div>
                    <div style={{ fontSize: '0.9rem', color: '#666' }}>
                      {conversion.conversion_type === 'cash' ? '💰 Dinheiro' : '🌱 ESG'} • 
                      R$ {conversion.original_amount.toFixed(2)} → R$ {conversion.user_amount.toFixed(2)}
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ 
                      color: conversion.status === 'completed' ? '#4CAF50' : '#FF9800',
                      fontWeight: 'bold',
                      textTransform: 'capitalize'
                    }}>
                      {conversion.status}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#666' }}>
                      {new Date(conversion.created_at).toLocaleDateString('pt-BR')}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Ativos ESG */}
        <div className="card">
          <h2>Seus Ativos ESG</h2>
          {esgAssets.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#666', padding: '2rem' }}>
              Nenhum ativo ESG criado ainda
            </p>
          ) : (
            <div style={{ display: 'grid', gap: '1rem' }}>
              {esgAssets.map((asset) => (
                <div key={asset.id} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem',
                  border: '1px solid #8BC34A',
                  borderRadius: '8px',
                  background: '#f8fff8'
                }}>
                  <div>
                    <div style={{ fontWeight: 'bold', marginBottom: '0.25rem' }}>
                      {asset.invoice_number}
                    </div>
                    <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.25rem' }}>
                      R$ {asset.esg_value.toFixed(2)} • ESG Score: {asset.esg_score}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#8BC34A' }}>
                      🌱 {asset.carbon_offset_kg.toFixed(1)}kg CO₂ compensado
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ 
                      color: asset.status === 'active' ? '#8BC34A' : '#FF9800',
                      fontWeight: 'bold',
                      textTransform: 'capitalize',
                      marginBottom: '0.5rem'
                    }}>
                      {asset.status}
                    </div>
                    {asset.status === 'active' && (
                      <button 
                        className="button secondary"
                        style={{ padding: '0.5rem 1rem', fontSize: '0.8rem' }}
                        onClick={() => handleSellESGAsset(asset.id)}
                      >
                        Vender
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Ações Rápidas */}
        <div className="card">
          <h2>Ações Rápidas</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
            <button 
              className="button"
              onClick={() => alert('Funcionalidade em desenvolvimento')}
            >
              💰 Converter Nota Fiscal em Dinheiro
            </button>
            <button 
              className="button secondary"
              onClick={() => alert('Funcionalidade em desenvolvimento')}
            >
              🌱 Converter em Ativo ESG
            </button>
            <button 
              className="button"
              onClick={() => alert('Funcionalidade em desenvolvimento')}
            >
              💱 Marketplace ESG
            </button>
            <button 
              className="button secondary"
              onClick={() => alert('Funcionalidade em desenvolvimento')}
            >
              📊 Relatórios de Monetização
            </button>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default MonetizationPage;
