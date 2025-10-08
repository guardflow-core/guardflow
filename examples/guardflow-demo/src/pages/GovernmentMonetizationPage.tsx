import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface GovernmentIncentive {
  type: string;
  name: string;
  description: string;
  potential_percentage: number;
  processing_time: string;
  requirements: string[];
  benefits: string[];
}

interface MonetizationPotential {
  invoice_value: number;
  monetization_type: string;
  estimated_government_value: number;
  guardflow_share: number;
  user_share: number;
  processing_time: string;
  requirements: string[];
  benefits: string[];
  roi_percentage: number;
}

const GovernmentMonetizationPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [incentives, setIncentives] = useState<GovernmentIncentive[]>([]);
  const [selectedIncentive, setSelectedIncentive] = useState<string>('icms_credits');
  const [invoiceValue, setInvoiceValue] = useState<number>(0);
  const [potential, setPotential] = useState<MonetizationPotential | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadIncentives();
  }, []);

  useEffect(() => {
    if (invoiceValue > 0) {
      calculatePotential();
    }
  }, [invoiceValue, selectedIncentive]);

  const loadIncentives = async () => {
    try {
      // Simular carregamento de dados
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Dados mock baseados em incentivos fiscais reais
      setIncentives([
        {
          type: "icms_credits",
          name: "Créditos de ICMS",
          description: "Créditos de ICMS para compensação tributária",
          potential_percentage: 12.0,
          processing_time: "30-60 dias",
          requirements: [
            "Nota fiscal de entrada válida",
            "CNPJ ativo",
            "Regime tributário adequado"
          ],
          benefits: [
            "Compensação de débitos de ICMS",
            "Redução do custo tributário",
            "Melhoria do fluxo de caixa"
          ]
        },
        {
          type: "ipi_credits",
          name: "Créditos de IPI",
          description: "Créditos de IPI para indústrias",
          potential_percentage: 8.0,
          processing_time: "45-90 dias",
          requirements: [
            "Nota fiscal de entrada de indústria",
            "Produto com IPI",
            "Regime especial de tributação"
          ],
          benefits: [
            "Compensação de IPI",
            "Redução de custos industriais",
            "Competitividade no mercado"
          ]
        },
        {
          type: "pis_cofins",
          name: "PIS/COFINS",
          description: "Créditos de PIS e COFINS",
          potential_percentage: 3.65,
          processing_time: "60-120 dias",
          requirements: [
            "Nota fiscal de entrada",
            "Regime cumulativo ou não-cumulativo",
            "Documentação fiscal completa"
          ],
          benefits: [
            "Compensação de PIS/COFINS",
            "Redução de custos",
            "Compliance tributário"
          ]
        },
        {
          type: "lei_bem",
          name: "Lei do Bem",
          description: "Incentivos fiscais para inovação",
          potential_percentage: 20.0,
          processing_time: "90-180 dias",
          requirements: [
            "Investimento em P&D",
            "Projetos aprovados",
            "Documentação técnica"
          ],
          benefits: [
            "Desconto no IRPJ",
            "Desconto no CSLL",
            "Incentivo à inovação"
          ]
        },
        {
          type: "lei_informatica",
          name: "Lei de Informática",
          description: "Desconto em IPI para TI",
          potential_percentage: 15.0,
          processing_time: "60-150 dias",
          requirements: [
            "Produto de informática",
            "Certificação de software",
            "Regime especial"
          ],
          benefits: [
            "Desconto em IPI",
            "Competitividade",
            "Incentivo à tecnologia"
          ]
        }
      ]);
    } catch (error) {
      console.error('Erro ao carregar incentivos:', error);
    }
  };

  const calculatePotential = async () => {
    try {
      setLoading(true);
      
      // Simular cálculo
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const incentive = incentives.find(i => i.type === selectedIncentive);
      if (!incentive) return;

      const estimatedValue = invoiceValue * (incentive.potential_percentage / 100);
      const guardflowShare = estimatedValue * 0.70;
      const userShare = estimatedValue * 0.30;
      const roiPercentage = (userShare / invoiceValue) * 100;

      setPotential({
        invoice_value: invoiceValue,
        monetization_type: selectedIncentive,
        estimated_government_value: estimatedValue,
        guardflow_share: guardflowShare,
        user_share: userShare,
        processing_time: incentive.processing_time,
        requirements: incentive.requirements,
        benefits: incentive.benefits,
        roi_percentage: roiPercentage
      });
    } catch (error) {
      console.error('Erro ao calcular potencial:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAuthorizeMonetization = async () => {
    if (!invoiceValue) {
      alert('Valor da nota fiscal não informado');
      return;
    }

    setLoading(true);
    try {
      // Simular autorização
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      alert(`Autorização confirmada! Monetização governamental ativada para ${selectedIncentive}`);
      navigate('/monetization');
    } catch (error) {
      alert('Erro ao autorizar monetização');
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div>
        <div className="header">
          <h1>Monetização Governamental</h1>
          <p>Monetize suas notas fiscais junto ao governo</p>
        </div>
        <div className="nav">
          <button className="nav-button" onClick={() => navigate('/')}>
            🏠 Início
          </button>
        </div>
        <div className="main-content">
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🏛️</div>
            <h2>Faça Login</h2>
            <p style={{ marginBottom: '2rem', color: '#666' }}>
              Entre na sua conta para acessar a monetização governamental
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
        <h1>Monetização Governamental</h1>
        <p>Monetize suas notas fiscais junto ao governo através de créditos fiscais</p>
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

        {/* Incentivos Fiscais Disponíveis */}
        <div className="card">
          <h2>Incentivos Fiscais Disponíveis</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
            {incentives.map((incentive) => (
              <div
                key={incentive.type}
                style={{
                  border: selectedIncentive === incentive.type ? '2px solid #4CAF50' : '1px solid #ddd',
                  borderRadius: '12px',
                  padding: '1.5rem',
                  cursor: 'pointer',
                  background: selectedIncentive === incentive.type ? '#f8fff8' : 'white',
                  position: 'relative'
                }}
                onClick={() => setSelectedIncentive(incentive.type)}
              >
                <h3 style={{ marginBottom: '0.5rem', color: '#333' }}>{incentive.name}</h3>
                <div style={{ 
                  fontSize: '2rem', 
                  fontWeight: 'bold', 
                  color: '#4CAF50',
                  marginBottom: '0.5rem'
                }}>
                  {incentive.potential_percentage}%
                </div>
                <p style={{ color: '#666', marginBottom: '1rem' }}>{incentive.description}</p>
                
                <div style={{ marginBottom: '1rem' }}>
                  <h4 style={{ fontSize: '0.9rem', marginBottom: '0.5rem', color: '#333' }}>
                    Benefícios:
                  </h4>
                  <ul style={{ fontSize: '0.8rem', color: '#666', paddingLeft: '1rem' }}>
                    {incentive.benefits.map((benefit, index) => (
                      <li key={index} style={{ marginBottom: '0.25rem' }}>✓ {benefit}</li>
                    ))}
                  </ul>
                </div>

                <div style={{
                  background: '#f0f0f0',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '0.25rem' }}>
                    Tempo de processamento:
                  </div>
                  <div style={{ fontSize: '1rem', fontWeight: 'bold', color: '#4CAF50' }}>
                    {incentive.processing_time}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Potencial de Monetização */}
        {potential && (
          <div className="card">
            <h2>Potencial de Monetização</h2>
            <div style={{
              background: '#e8f5e8',
              padding: '1.5rem',
              borderRadius: '8px',
              border: '1px solid #4CAF50',
              marginBottom: '1rem'
            }}>
              <h3 style={{ color: '#2E7D32', marginBottom: '1rem' }}>
                Resumo da Monetização
              </h3>
              <div style={{ display: 'grid', gap: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Valor da nota fiscal:</span>
                  <span style={{ fontWeight: 'bold' }}>R$ {potential.invoice_value.toFixed(2)}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Valor estimado com governo:</span>
                  <span style={{ fontWeight: 'bold', color: '#4CAF50' }}>
                    R$ {potential.estimated_government_value.toFixed(2)}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Sua parte (30%):</span>
                  <span style={{ fontWeight: 'bold', color: '#4CAF50' }}>
                    R$ {potential.user_share.toFixed(2)}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Parte do GuardFlow (70%):</span>
                  <span style={{ fontWeight: 'bold', color: '#666' }}>
                    R$ {potential.guardflow_share.toFixed(2)}
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
                  <span>ROI para você:</span>
                  <span style={{ color: '#4CAF50' }}>
                    {potential.roi_percentage.toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <h4 style={{ marginBottom: '0.5rem', color: '#333' }}>Requisitos:</h4>
              <ul style={{ fontSize: '0.9rem', color: '#666', paddingLeft: '1rem' }}>
                {potential.requirements.map((req, index) => (
                  <li key={index} style={{ marginBottom: '0.25rem' }}>• {req}</li>
                ))}
              </ul>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <h4 style={{ marginBottom: '0.5rem', color: '#333' }}>Benefícios:</h4>
              <ul style={{ fontSize: '0.9rem', color: '#666', paddingLeft: '1rem' }}>
                {potential.benefits.map((benefit, index) => (
                  <li key={index} style={{ marginBottom: '0.25rem' }}>✓ {benefit}</li>
                ))}
              </ul>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input type="checkbox" required />
                <span>Autorizo o GuardFlow a monetizar minha nota fiscal junto ao governo</span>
              </label>
            </div>

            <button
              className="button"
              onClick={handleAuthorizeMonetization}
              disabled={loading}
              style={{
                opacity: loading ? 0.6 : 1,
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              {loading ? 'Processando...' : 'Autorizar Monetização Governamental'}
            </button>
          </div>
        )}

        {/* Informações sobre Monetização Governamental */}
        <div className="card" style={{ background: '#f8f9fa', border: '1px solid #e9ecef' }}>
          <h3 style={{ color: '#495057', marginBottom: '1rem' }}>
            💡 Como Funciona a Monetização Governamental
          </h3>
          <div style={{ color: '#6c757d', fontSize: '0.9rem', lineHeight: '1.5' }}>
            <p style={{ marginBottom: '1rem' }}>
              O GuardFlow atua como intermediário entre você e o governo, utilizando suas notas fiscais 
              para gerar créditos fiscais e incentivos tributários.
            </p>
            <p style={{ marginBottom: '1rem' }}>
              <strong>Processo:</strong>
            </p>
            <ol style={{ paddingLeft: '1.5rem', marginBottom: '1rem' }}>
              <li>Você autoriza o uso da sua nota fiscal</li>
              <li>GuardFlow processa os créditos fiscais junto ao governo</li>
              <li>Você recebe 30% do valor gerado</li>
              <li>GuardFlow fica com 70% como taxa de serviço</li>
            </ol>
            <p>
              <strong>Vantagem:</strong> Você ganha dinheiro com notas fiscais que normalmente 
              não teriam valor monetário direto, enquanto o GuardFlow monetiza o processo.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GovernmentMonetizationPage;
