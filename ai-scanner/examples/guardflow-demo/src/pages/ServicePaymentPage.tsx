import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface ServicePricing {
  tier: string;
  percentage: number;
  description: string;
  features: string[];
  recommended?: boolean;
}

interface ServiceBenefits {
  category: string;
  benefits: string[];
}

const ServicePaymentPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated } = useAuth();
  const [pricing, setPricing] = useState<ServicePricing[]>([]);
  const [benefits, setBenefits] = useState<ServiceBenefits[]>([]);
  const [selectedTier, setSelectedTier] = useState<string>('Padrão');
  const [invoiceValue, setInvoiceValue] = useState<number>(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadServiceData();
    
    // Pegar valor da nota fiscal da URL ou state
    const state = location.state as any;
    if (state?.invoiceValue) {
      setInvoiceValue(state.invoiceValue);
    }
  }, [location]);

  const loadServiceData = async () => {
    try {
      // Simular carregamento de dados
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Dados mock para demonstração
      setPricing([
        {
          tier: "Básico",
          percentage: 10.0,
          description: "Escaneamento básico + cálculo de totais",
          features: [
            "Escaneamento de produtos",
            "Cálculo automático",
            "Carrinho inteligente"
          ]
        },
        {
          tier: "Padrão",
          percentage: 15.0,
          description: "Serviço completo + ESG",
          features: [
            "Todas as funcionalidades básicas",
            "Integração ESG automática",
            "Múltiplas formas de pagamento",
            "Histórico de compras"
          ],
          recommended: true
        },
        {
          tier: "Premium",
          percentage: 20.0,
          description: "Serviço premium + GuardPass",
          features: [
            "Todas as funcionalidades padrão",
            "Sistema GuardPass",
            "Tokens ESG",
            "Prioridade no atendimento",
            "Relatórios avançados"
          ]
        }
      ]);

      setBenefits([
        {
          category: "Agilidade",
          benefits: [
            "Checkout 70% mais rápido",
            "Escaneamento instantâneo",
            "Cálculo automático de totais",
            "Sem filas de espera"
          ]
        },
        {
          category: "Conveniência",
          benefits: [
            "Múltiplas formas de pagamento",
            "Histórico de compras",
            "Notificações inteligentes",
            "Integração com carteira digital"
          ]
        },
        {
          category: "Sustentabilidade",
          benefits: [
            "Impacto ESG automático",
            "Tokens de sustentabilidade",
            "Relatórios de pegada de carbono",
            "Incentivos verdes"
          ]
        },
        {
          category: "Segurança",
          benefits: [
            "Sistema GuardDrive",
            "Criptografia end-to-end",
            "Proteção de dados",
            "Auditoria completa"
          ]
        }
      ]);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    }
  };

  const calculateServiceFee = (tier: string) => {
    const tierData = pricing.find(p => p.tier === tier);
    if (!tierData || !invoiceValue) return 0;
    return invoiceValue * (tierData.percentage / 100);
  };

  const calculateRemainingValue = (tier: string) => {
    const serviceFee = calculateServiceFee(tier);
    return invoiceValue - serviceFee;
  };

  const handleAuthorizeService = async () => {
    if (!invoiceValue) {
      alert('Valor da nota fiscal não informado');
      return;
    }

    setLoading(true);
    try {
      // Simular autorização
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      alert(`Autorização confirmada! Serviço "${selectedTier}" ativado por R$ ${calculateServiceFee(selectedTier).toFixed(2)}`);
      navigate('/monetization');
    } catch (error) {
      alert('Erro ao autorizar serviço');
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div>
        <div className="header">
          <h1>Pagamento por Serviço</h1>
          <p>Use sua nota fiscal como pagamento pelo "Agiliza aí!"</p>
        </div>
        <div className="nav">
          <button className="nav-button" onClick={() => navigate('/')}>
            🏠 Início
          </button>
        </div>
        <div className="main-content">
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>💳</div>
            <h2>Faça Login</h2>
            <p style={{ marginBottom: '2rem', color: '#666' }}>
              Entre na sua conta para autorizar o pagamento por serviço
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

  return (
    <div>
      <div className="header">
        <h1>Pagamento por Serviço "Agiliza aí!"</h1>
        <p>Use sua nota fiscal como pagamento pelo serviço de checkout inteligente</p>
      </div>

      <div className="nav">
        <button className="nav-button" onClick={() => navigate('/')}>
          🏠 Início
        </button>
        <button className="nav-button" onClick={() => navigate('/monetization')}>
          💰 Monetização
        </button>
      </div>

      <div className="main-content">
        {/* Valor da Nota Fiscal */}
        <div className="card">
          <h2>Valor da Nota Fiscal</h2>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '1rem',
            marginBottom: '1rem'
          }}>
            <input
              type="number"
              value={invoiceValue}
              onChange={(e) => setInvoiceValue(Number(e.target.value))}
              placeholder="Digite o valor da nota fiscal"
              style={{
                padding: '0.75rem',
                border: '1px solid #ddd',
                borderRadius: '8px',
                fontSize: '1rem',
                flex: 1
              }}
            />
            <span style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#4CAF50' }}>
              R$ {invoiceValue.toFixed(2)}
            </span>
          </div>
        </div>

        {/* Planos de Serviço */}
        <div className="card">
          <h2>Escolha o Plano do Serviço</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
            {pricing.map((tier) => (
              <div
                key={tier.tier}
                style={{
                  border: selectedTier === tier.tier ? '2px solid #4CAF50' : '1px solid #ddd',
                  borderRadius: '12px',
                  padding: '1.5rem',
                  cursor: 'pointer',
                  background: selectedTier === tier.tier ? '#f8fff8' : 'white',
                  position: 'relative'
                }}
                onClick={() => setSelectedTier(tier.tier)}
              >
                {tier.recommended && (
                  <div style={{
                    position: 'absolute',
                    top: '-10px',
                    right: '20px',
                    background: '#4CAF50',
                    color: 'white',
                    padding: '0.25rem 0.75rem',
                    borderRadius: '12px',
                    fontSize: '0.8rem',
                    fontWeight: 'bold'
                  }}>
                    RECOMENDADO
                  </div>
                )}
                
                <h3 style={{ marginBottom: '0.5rem', color: '#333' }}>{tier.tier}</h3>
                <div style={{ 
                  fontSize: '2rem', 
                  fontWeight: 'bold', 
                  color: '#4CAF50',
                  marginBottom: '0.5rem'
                }}>
                  {tier.percentage}%
                </div>
                <p style={{ color: '#666', marginBottom: '1rem' }}>{tier.description}</p>
                
                <div style={{ marginBottom: '1rem' }}>
                  <h4 style={{ fontSize: '0.9rem', marginBottom: '0.5rem', color: '#333' }}>
                    Funcionalidades:
                  </h4>
                  <ul style={{ fontSize: '0.8rem', color: '#666', paddingLeft: '1rem' }}>
                    {tier.features.map((feature, index) => (
                      <li key={index} style={{ marginBottom: '0.25rem' }}>✓ {feature}</li>
                    ))}
                  </ul>
                </div>

                {invoiceValue > 0 && (
                  <div style={{
                    background: '#f0f0f0',
                    padding: '1rem',
                    borderRadius: '8px',
                    textAlign: 'center'
                  }}>
                    <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.25rem' }}>
                      Taxa do serviço:
                    </div>
                    <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#4CAF50' }}>
                      R$ {calculateServiceFee(tier.tier).toFixed(2)}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.25rem' }}>
                      Restante: R$ {calculateRemainingValue(tier.tier).toFixed(2)}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Benefícios do Serviço */}
        <div className="card">
          <h2>Benefícios do Serviço "Agiliza aí!"</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
            {benefits.map((benefit, index) => (
              <div key={index} style={{
                background: '#f8f9fa',
                padding: '1rem',
                borderRadius: '8px',
                border: '1px solid #e9ecef'
              }}>
                <h3 style={{ color: '#4CAF50', marginBottom: '0.5rem' }}>{benefit.category}</h3>
                <ul style={{ fontSize: '0.9rem', color: '#666', paddingLeft: '1rem' }}>
                  {benefit.benefits.map((item, itemIndex) => (
                    <li key={itemIndex} style={{ marginBottom: '0.25rem' }}>• {item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* ROI Calculation */}
        <div className="card" style={{ background: '#e8f5e8', border: '1px solid #4CAF50' }}>
          <h3 style={{ color: '#2E7D32', marginBottom: '1rem' }}>💰 Retorno do Investimento</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#4CAF50' }}>70%</div>
              <div style={{ fontSize: '0.9rem', color: '#666' }}>Mais rápido</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#4CAF50' }}>5-10 min</div>
              <div style={{ fontSize: '0.9rem', color: '#666' }}>Economizados por compra</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#4CAF50' }}>R$ 50-250</div>
              <div style={{ fontSize: '0.9rem', color: '#666' }}>Valor mensal economizado</div>
            </div>
          </div>
        </div>

        {/* Autorização */}
        {invoiceValue > 0 && (
          <div className="card">
            <h2>Autorizar Pagamento por Serviço</h2>
            <div style={{
              background: '#f8fff8',
              padding: '1.5rem',
              borderRadius: '8px',
              border: '1px solid #4CAF50',
              marginBottom: '1rem'
            }}>
              <h3 style={{ color: '#2E7D32', marginBottom: '1rem' }}>
                Resumo da Autorização
              </h3>
              <div style={{ display: 'grid', gap: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Valor da nota fiscal:</span>
                  <span style={{ fontWeight: 'bold' }}>R$ {invoiceValue.toFixed(2)}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Taxa do serviço ({selectedTier}):</span>
                  <span style={{ fontWeight: 'bold', color: '#4CAF50' }}>
                    R$ {calculateServiceFee(selectedTier).toFixed(2)}
                  </span>
                </div>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between',
                  paddingTop: '0.5rem',
                  borderTop: '1px solid #ddd',
                  fontWeight: 'bold',
                  fontSize: '1.1rem'
                }}>
                  <span>Valor restante para você:</span>
                  <span style={{ color: '#4CAF50' }}>
                    R$ {calculateRemainingValue(selectedTier).toFixed(2)}
                  </span>
                </div>
              </div>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input type="checkbox" required />
                <span>Autorizo o uso da minha nota fiscal como pagamento pelo serviço "Agiliza aí!"</span>
              </label>
            </div>

            <button
              className="button"
              onClick={handleAuthorizeService}
              disabled={loading}
              style={{
                opacity: loading ? 0.6 : 1,
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              {loading ? 'Processando...' : 'Autorizar Pagamento por Serviço'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ServicePaymentPage;
