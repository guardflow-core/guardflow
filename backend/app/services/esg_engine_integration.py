"""
Integração real com ESG Engine
Conecta com o sistema de cálculo ESG existente
"""

import httpx
import os
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ESGEngineService:
    def __init__(self):
        self.base_url = os.getenv("ESG_ENGINE_URL", "http://localhost:8001")
        self.api_key = os.getenv("ESG_ENGINE_API_KEY", "")
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=15.0
        )
        
        # Cache local para NCM codes
        self.ncm_cache = {}
    
    async def calculate_product_esg(self, ncm_code: str, product_data: Dict = None) -> Dict:
        """Calcula ESG score de um produto pelo NCM"""
        try:
            # Verificar cache primeiro
            if ncm_code in self.ncm_cache:
                cached_data = self.ncm_cache[ncm_code]
                # Cache válido por 24h
                if (datetime.now() - cached_data["timestamp"]).seconds < 86400:
                    return cached_data["data"]
            
            # Buscar na API do ESG Engine
            payload = {
                "ncm_code": ncm_code,
                "product_data": product_data or {}
            }
            
            response = await self.client.post("/esg/calculate", json=payload)
            
            if response.status_code == 200:
                esg_data = response.json()
                
                # Cachear resultado
                self.ncm_cache[ncm_code] = {
                    "data": esg_data,
                    "timestamp": datetime.now()
                }
                
                return esg_data
            else:
                logger.warning(f"ESG Engine API error: {response.status_code}")
                return self._fallback_esg_calculation(ncm_code)
                
        except httpx.RequestError as e:
            logger.error(f"ESG Engine connection error: {e}")
            return self._fallback_esg_calculation(ncm_code)
        except Exception as e:
            logger.error(f"ESG calculation error: {e}")
            return self._fallback_esg_calculation(ncm_code)
    
    async def calculate_cart_esg_impact(self, items: List[Dict]) -> Dict:
        """Calcula impacto ESG total do carrinho"""
        total_environmental = 0.0
        total_social = 0.0
        total_governance = 0.0
        total_value = 0.0
        processed_items = []
        
        for item in items:
            item_value = item.get("unit_price", 0) * item.get("quantity", 1)
            total_value += item_value
            
            # Usar ESG score já calculado se disponível
            if item.get("esg_score"):
                # Assumir distribuição equilibrada E/S/G
                env_score = item["esg_score"]
                soc_score = item["esg_score"] 
                gov_score = item["esg_score"]
            else:
                # Calcular via NCM
                ncm_code = item.get("ncm_code")
                if ncm_code:
                    esg_data = await self.calculate_product_esg(ncm_code, {
                        "name": item.get("name"),
                        "price": item.get("unit_price"),
                        "weight": item.get("expected_weight_kg")
                    })
                    
                    env_score = esg_data.get("environmental_score", 5.0)
                    soc_score = esg_data.get("social_score", 5.0)
                    gov_score = esg_data.get("governance_score", 5.0)
                else:
                    # Fallback para scores médios
                    env_score = soc_score = gov_score = 5.0
            
            # Ponderar por valor do item
            total_environmental += env_score * item_value
            total_social += soc_score * item_value
            total_governance += gov_score * item_value
            
            processed_items.append({
                **item,
                "environmental_score": env_score,
                "social_score": soc_score,
                "governance_score": gov_score,
                "overall_esg_score": (env_score + soc_score + gov_score) / 3
            })
        
        if total_value == 0:
            return self._empty_cart_esg()
        
        # Calcular médias ponderadas
        avg_environmental = total_environmental / total_value
        avg_social = total_social / total_value
        avg_governance = total_governance / total_value
        overall_score = (avg_environmental + avg_social + avg_governance) / 3
        
        # Classificar impacto
        impact_level = self._classify_esg_impact(overall_score)
        
        return {
            "overall_score": round(overall_score, 2),
            "environmental_score": round(avg_environmental, 2),
            "social_score": round(avg_social, 2),
            "governance_score": round(avg_governance, 2),
            "impact_level": impact_level,
            "total_value": total_value,
            "items_analyzed": len(processed_items),
            "items": processed_items,
            "recommendations": self._generate_esg_recommendations(overall_score, processed_items),
            "calculated_at": datetime.now().isoformat()
        }
    
    async def get_esg_insights(self, store_id: str, period_days: int = 30) -> Dict:
        """Obtém insights ESG para uma loja"""
        try:
            response = await self.client.get(f"/esg/insights/{store_id}?period={period_days}")
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._default_insights()
                
        except Exception as e:
            logger.error(f"Error getting ESG insights: {e}")
            return self._default_insights()
    
    async def register_esg_transaction(self, transaction_data: Dict) -> bool:
        """Registra transação para análise ESG futura"""
        try:
            payload = {
                "store_id": transaction_data.get("store_id"),
                "cart_id": transaction_data.get("cart_id"),
                "esg_impact": transaction_data.get("esg_impact"),
                "items": transaction_data.get("items", []),
                "timestamp": datetime.now().isoformat()
            }
            
            response = await self.client.post("/esg/transactions", json=payload)
            return response.status_code == 201
            
        except Exception as e:
            logger.error(f"Error registering ESG transaction: {e}")
            return False
    
    def _fallback_esg_calculation(self, ncm_code: str) -> Dict:
        """Cálculo ESG offline baseado em regras simples"""
        # Regras básicas por categoria NCM
        ncm_rules = {
            # Alimentos básicos - ESG médio-alto
            "04": {"env": 6.0, "soc": 7.0, "gov": 6.5},  # Laticínios
            "10": {"env": 7.0, "soc": 8.0, "gov": 7.0},  # Cereais
            "17": {"env": 4.0, "soc": 5.0, "gov": 5.5},  # Açúcares
            
            # Bebidas alcoólicas - ESG baixo
            "22": {"env": 3.0, "soc": 3.5, "gov": 4.0},
            
            # Medicamentos - ESG alto
            "30": {"env": 8.0, "soc": 9.0, "gov": 8.5},
            
            # Eletrônicos - ESG médio-baixo
            "85": {"env": 4.5, "soc": 5.0, "gov": 6.0},
        }
        
        # Pegar primeiros 2 dígitos do NCM
        category = ncm_code[:2] if len(ncm_code) >= 2 else "00"
        
        if category in ncm_rules:
            scores = ncm_rules[category]
        else:
            # Scores padrão
            scores = {"env": 5.0, "soc": 5.0, "gov": 5.0}
        
        return {
            "environmental_score": scores["env"],
            "social_score": scores["soc"],
            "governance_score": scores["gov"],
            "overall_score": sum(scores.values()) / 3,
            "data_source": "fallback_rules",
            "ncm_category": category
        }
    
    def _classify_esg_impact(self, score: float) -> str:
        """Classifica o nível de impacto ESG"""
        if score >= 8.0:
            return "excellent"
        elif score >= 7.0:
            return "good"
        elif score >= 5.0:
            return "average"
        elif score >= 3.0:
            return "poor"
        else:
            return "critical"
    
    def _generate_esg_recommendations(self, overall_score: float, items: List[Dict]) -> List[str]:
        """Gera recomendações ESG baseadas no carrinho"""
        recommendations = []
        
        if overall_score < 6.0:
            recommendations.append("Considere substituir alguns produtos por alternativas mais sustentáveis")
        
        # Verificar produtos com baixo ESG
        low_esg_items = [item for item in items if item.get("overall_esg_score", 5.0) < 4.0]
        if low_esg_items:
            recommendations.append(f"Encontramos {len(low_esg_items)} produtos com baixo impacto ESG")
        
        # Verificar produtos com alto ESG
        high_esg_items = [item for item in items if item.get("overall_esg_score", 5.0) > 7.0]
        if high_esg_items:
            recommendations.append(f"Parabéns! {len(high_esg_items)} produtos têm excelente impacto ESG")
        
        if overall_score >= 8.0:
            recommendations.append("Sua compra tem impacto ESG excelente! Continue assim!")
        
        return recommendations
    
    def _empty_cart_esg(self) -> Dict:
        """Retorno para carrinho vazio"""
        return {
            "overall_score": 0.0,
            "environmental_score": 0.0,
            "social_score": 0.0,
            "governance_score": 0.0,
            "impact_level": "none",
            "total_value": 0.0,
            "items_analyzed": 0,
            "items": [],
            "recommendations": ["Adicione produtos ao carrinho para análise ESG"],
            "calculated_at": datetime.now().isoformat()
        }
    
    def _default_insights(self) -> Dict:
        """Insights padrão quando API não disponível"""
        return {
            "average_esg_score": 5.5,
            "trend": "stable",
            "top_categories": ["Alimentos básicos", "Produtos de limpeza"],
            "recommendations": ["Dados de insights não disponíveis no momento"]
        }
    
    async def close(self):
        """Fechar cliente HTTP"""
        await self.client.aclose()

# Instância global do serviço
esg_engine_service = ESGEngineService()
