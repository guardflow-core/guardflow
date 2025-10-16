# -*- coding: utf-8 -*-
"""
🌱 GUARDFLOW ESG ENGINE
Sistema de cálculo de scores ESG baseado em NCM e fatores sustentáveis
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class ESGCategory(Enum):
    """Categorias ESG"""
    ENVIRONMENTAL = "environmental"
    SOCIAL = "social"
    GOVERNANCE = "governance"

class ESGImpact(Enum):
    """Níveis de impacto ESG"""
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5

@dataclass
class ESGFactor:
    """Fator ESG com peso e impacto"""
    name: str
    category: ESGCategory
    weight: float  # 0.0 a 1.0
    impact: ESGImpact
    description: str
    ncm_codes: List[str]  # Códigos NCM relacionados
    calculation_method: str

@dataclass
class ESGScore:
    """Score ESG calculado"""
    environmental: float
    social: float
    governance: float
    overall: float
    factors_applied: List[str]
    calculation_timestamp: datetime
    version: str

class ESGEngine:
    """Motor de cálculo ESG para GuardFlow"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.factors = self._load_esg_factors()
        self.ncm_mapping = self._load_ncm_mapping()
        logger.info(f"ESG Engine v{self.version} inicializado com {len(self.factors)} fatores")
    
    def _load_esg_factors(self) -> List[ESGFactor]:
        """Carrega fatores ESG do banco de dados ou arquivo"""
        return [
            # Fatores Ambientais
            ESGFactor(
                name="carbon_footprint",
                category=ESGCategory.ENVIRONMENTAL,
                weight=0.3,
                impact=ESGImpact.HIGH,
                description="Pegada de carbono do produto",
                ncm_codes=["84", "85", "87", "90"],  # Eletrônicos, veículos, equipamentos
                calculation_method="weighted_carbon_intensity"
            ),
            ESGFactor(
                name="renewable_energy",
                category=ESGCategory.ENVIRONMENTAL,
                weight=0.2,
                impact=ESGImpact.MEDIUM,
                description="Uso de energia renovável na produção",
                ncm_codes=["27", "28", "29"],  # Energia, combustíveis
                calculation_method="renewable_percentage"
            ),
            ESGFactor(
                name="waste_reduction",
                category=ESGCategory.ENVIRONMENTAL,
                weight=0.2,
                impact=ESGImpact.MEDIUM,
                description="Redução de resíduos e reciclagem",
                ncm_codes=["39", "40", "48", "49"],  # Plásticos, papel
                calculation_method="waste_ratio"
            ),
            ESGFactor(
                name="water_usage",
                category=ESGCategory.ENVIRONMENTAL,
                weight=0.15,
                impact=ESGImpact.MEDIUM,
                description="Eficiência no uso de água",
                ncm_codes=["22", "23", "24"],  # Bebidas, alimentos
                calculation_method="water_intensity"
            ),
            ESGFactor(
                name="biodiversity",
                category=ESGCategory.ENVIRONMENTAL,
                weight=0.15,
                impact=ESGImpact.LOW,
                description="Impacto na biodiversidade",
                ncm_codes=["01", "02", "03", "04"],  # Animais, plantas
                calculation_method="biodiversity_impact"
            ),
            
            # Fatores Sociais
            ESGFactor(
                name="labor_conditions",
                category=ESGCategory.SOCIAL,
                weight=0.25,
                impact=ESGImpact.HIGH,
                description="Condições de trabalho e direitos trabalhistas",
                ncm_codes=["61", "62", "63", "64"],  # Têxteis, calçados
                calculation_method="labor_score"
            ),
            ESGFactor(
                name="community_impact",
                category=ESGCategory.SOCIAL,
                weight=0.2,
                impact=ESGImpact.MEDIUM,
                description="Impacto na comunidade local",
                ncm_codes=["01", "02", "03", "04", "05"],  # Produtos locais
                calculation_method="community_benefit"
            ),
            ESGFactor(
                name="health_safety",
                category=ESGCategory.SOCIAL,
                weight=0.2,
                impact=ESGImpact.HIGH,
                description="Segurança e saúde do produto",
                ncm_codes=["30", "33", "34", "35"],  # Medicamentos, cosméticos
                calculation_method="safety_rating"
            ),
            ESGFactor(
                name="diversity_inclusion",
                category=ESGCategory.SOCIAL,
                weight=0.15,
                impact=ESGImpact.MEDIUM,
                description="Diversidade e inclusão na cadeia",
                ncm_codes=["61", "62", "63", "64"],  # Têxteis
                calculation_method="diversity_index"
            ),
            ESGFactor(
                name="education_access",
                category=ESGCategory.SOCIAL,
                weight=0.2,
                impact=ESGImpact.MEDIUM,
                description="Acesso à educação e capacitação",
                ncm_codes=["49", "85"],  # Livros, eletrônicos educacionais
                calculation_method="education_impact"
            ),
            
            # Fatores de Governança
            ESGFactor(
                name="transparency",
                category=ESGCategory.GOVERNANCE,
                weight=0.3,
                impact=ESGImpact.HIGH,
                description="Transparência e rastreabilidade",
                ncm_codes=["84", "85", "90"],  # Tecnologia
                calculation_method="transparency_score"
            ),
            ESGFactor(
                name="anti_corruption",
                category=ESGCategory.GOVERNANCE,
                weight=0.25,
                impact=ESGImpact.HIGH,
                description="Políticas anti-corrupção",
                ncm_codes=["84", "85", "90"],  # Tecnologia
                calculation_method="compliance_score"
            ),
            ESGFactor(
                name="data_privacy",
                category=ESGCategory.GOVERNANCE,
                weight=0.25,
                impact=ESGImpact.HIGH,
                description="Proteção de dados e privacidade",
                ncm_codes=["84", "85", "90"],  # Tecnologia
                calculation_method="privacy_score"
            ),
            ESGFactor(
                name="regulatory_compliance",
                category=ESGCategory.GOVERNANCE,
                weight=0.2,
                impact=ESGImpact.MEDIUM,
                description="Conformidade regulatória",
                ncm_codes=["30", "33", "34", "35"],  # Medicamentos, cosméticos
                calculation_method="compliance_rating"
            )
        ]
    
    def _load_ncm_mapping(self) -> Dict[str, List[str]]:
        """Carrega mapeamento NCM para fatores ESG"""
        return {
            # Eletrônicos e Tecnologia
            "84": ["carbon_footprint", "transparency", "anti_corruption", "data_privacy"],
            "85": ["carbon_footprint", "transparency", "anti_corruption", "data_privacy", "education_access"],
            "90": ["carbon_footprint", "transparency", "anti_corruption", "data_privacy"],
            
            # Energia e Combustíveis
            "27": ["renewable_energy", "carbon_footprint"],
            "28": ["renewable_energy", "carbon_footprint"],
            "29": ["renewable_energy", "carbon_footprint"],
            
            # Plásticos e Materiais
            "39": ["waste_reduction", "carbon_footprint"],
            "40": ["waste_reduction", "carbon_footprint"],
            "48": ["waste_reduction", "education_access"],
            "49": ["waste_reduction", "education_access"],
            
            # Bebidas e Alimentos
            "22": ["water_usage", "health_safety", "community_impact"],
            "23": ["water_usage", "health_safety", "community_impact"],
            "24": ["water_usage", "health_safety", "community_impact"],
            
            # Animais e Plantas
            "01": ["biodiversity", "community_impact", "health_safety"],
            "02": ["biodiversity", "community_impact", "health_safety"],
            "03": ["biodiversity", "community_impact", "health_safety"],
            "04": ["biodiversity", "community_impact", "health_safety"],
            "05": ["biodiversity", "community_impact"],
            
            # Têxteis e Calçados
            "61": ["labor_conditions", "diversity_inclusion"],
            "62": ["labor_conditions", "diversity_inclusion"],
            "63": ["labor_conditions", "diversity_inclusion"],
            "64": ["labor_conditions", "diversity_inclusion"],
            
            # Medicamentos e Cosméticos
            "30": ["health_safety", "regulatory_compliance"],
            "33": ["health_safety", "regulatory_compliance"],
            "34": ["health_safety", "regulatory_compliance"],
            "35": ["health_safety", "regulatory_compliance"]
        }
    
    def calculate_esg_score(self, ncm_code: str, product_data: Dict = None) -> ESGScore:
        """
        Calcula score ESG baseado no código NCM e dados do produto
        
        Args:
            ncm_code: Código NCM do produto
            product_data: Dados adicionais do produto (opcional)
        
        Returns:
            ESGScore: Score ESG calculado
        """
        try:
            # Obter fatores aplicáveis ao NCM
            applicable_factors = self._get_applicable_factors(ncm_code)
            
            if not applicable_factors:
                logger.warning(f"Nenhum fator ESG encontrado para NCM {ncm_code}")
                return self._create_default_score()
            
            # Calcular scores por categoria
            environmental_score = self._calculate_category_score(
                applicable_factors, ESGCategory.ENVIRONMENTAL, ncm_code, product_data
            )
            social_score = self._calculate_category_score(
                applicable_factors, ESGCategory.SOCIAL, ncm_code, product_data
            )
            governance_score = self._calculate_category_score(
                applicable_factors, ESGCategory.GOVERNANCE, ncm_code, product_data
            )
            
            # Calcular score geral (média ponderada)
            overall_score = (
                environmental_score * 0.4 +
                social_score * 0.3 +
                governance_score * 0.3
            )
            
            return ESGScore(
                environmental=round(environmental_score, 2),
                social=round(social_score, 2),
                governance=round(governance_score, 2),
                overall=round(overall_score, 2),
                factors_applied=[f.name for f in applicable_factors],
                calculation_timestamp=datetime.utcnow(),
                version=self.version
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular score ESG para NCM {ncm_code}: {e}")
            return self._create_default_score()
    
    def _get_applicable_factors(self, ncm_code: str) -> List[ESGFactor]:
        """Obtém fatores ESG aplicáveis ao código NCM"""
        ncm_prefix = ncm_code[:2]  # Primeiros 2 dígitos do NCM
        applicable_factor_names = self.ncm_mapping.get(ncm_prefix, [])
        
        return [f for f in self.factors if f.name in applicable_factor_names]
    
    def _calculate_category_score(
        self, 
        factors: List[ESGFactor], 
        category: ESGCategory, 
        ncm_code: str, 
        product_data: Dict = None
    ) -> float:
        """Calcula score para uma categoria ESG específica"""
        category_factors = [f for f in factors if f.category == category]
        
        if not category_factors:
            return 0.0
        
        total_weight = sum(f.weight for f in category_factors)
        weighted_score = 0.0
        
        for factor in category_factors:
            # Simular cálculo baseado no fator (implementação real seria mais complexa)
            factor_score = self._simulate_factor_calculation(factor, ncm_code, product_data)
            weighted_score += factor_score * factor.weight
        
        # Normalizar para escala 0-100
        return min(100.0, (weighted_score / total_weight) * 100) if total_weight > 0 else 0.0
    
    def _simulate_factor_calculation(
        self, 
        factor: ESGFactor, 
        ncm_code: str, 
        product_data: Dict = None
    ) -> float:
        """Simula cálculo de score para um fator ESG específico"""
        # Implementação simplificada - em produção seria mais sofisticada
        base_score = {
            ESGImpact.VERY_LOW: 20,
            ESGImpact.LOW: 40,
            ESGImpact.MEDIUM: 60,
            ESGImpact.HIGH: 80,
            ESGImpact.VERY_HIGH: 95
        }.get(factor.impact, 50)
        
        # Ajustar baseado em dados do produto se disponíveis
        if product_data:
            # Exemplo: produtos orgânicos têm score mais alto
            if product_data.get("organic", False):
                base_score += 10
            
            # Exemplo: produtos com certificação ESG
            if product_data.get("certified", False):
                base_score += 15
        
        return min(100.0, base_score)
    
    def _create_default_score(self) -> ESGScore:
        """Cria score ESG padrão quando não há dados suficientes"""
        return ESGScore(
            environmental=50.0,
            social=50.0,
            governance=50.0,
            overall=50.0,
            factors_applied=[],
            calculation_timestamp=datetime.utcnow(),
            version=self.version
        )
    
    def get_esg_factors_by_category(self, category: ESGCategory) -> List[ESGFactor]:
        """Retorna fatores ESG por categoria"""
        return [f for f in self.factors if f.category == category]
    
    def get_esg_factors_by_ncm(self, ncm_code: str) -> List[ESGFactor]:
        """Retorna fatores ESG aplicáveis a um código NCM"""
        return self._get_applicable_factors(ncm_code)
    
    def get_esg_insights(self, score: ESGScore) -> Dict[str, str]:
        """Gera insights baseados no score ESG"""
        insights = {}
        
        # Insights ambientais
        if score.environmental >= 80:
            insights["environmental"] = "Excelente performance ambiental"
        elif score.environmental >= 60:
            insights["environmental"] = "Boa performance ambiental"
        elif score.environmental >= 40:
            insights["environmental"] = "Performance ambiental moderada"
        else:
            insights["environmental"] = "Necessita melhorias ambientais"
        
        # Insights sociais
        if score.social >= 80:
            insights["social"] = "Excelente impacto social"
        elif score.social >= 60:
            insights["social"] = "Bom impacto social"
        elif score.social >= 40:
            insights["social"] = "Impacto social moderado"
        else:
            insights["social"] = "Necessita melhorias sociais"
        
        # Insights de governança
        if score.governance >= 80:
            insights["governance"] = "Excelente governança"
        elif score.governance >= 60:
            insights["governance"] = "Boa governança"
        elif score.governance >= 40:
            insights["governance"] = "Governança moderada"
        else:
            insights["governance"] = "Necessita melhorias na governança"
        
        # Insight geral
        if score.overall >= 80:
            insights["overall"] = "Produto altamente sustentável"
        elif score.overall >= 60:
            insights["overall"] = "Produto moderadamente sustentável"
        elif score.overall >= 40:
            insights["overall"] = "Produto com potencial de melhoria"
        else:
            insights["overall"] = "Produto necessita melhorias significativas"
        
        return insights

# Instância global do ESG Engine
esg_engine = ESGEngine()
