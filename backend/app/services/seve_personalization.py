"""
SEVE Personalization Engine - Camada de Personalização Inicial
Integração do SYMBEON SEVE na jornada do usuário desde o primeiro contato
"""

import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass, asdict
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class PersonalizationProfile:
    """Perfil de personalização anônimo"""
    anonymous_id: str
    behavioral_hash: str
    preferences: Dict
    esg_affinity: float
    brand_preferences: List[str]
    category_interests: List[str]
    price_sensitivity: str  # low, medium, high
    sustainability_score: float
    created_at: datetime
    last_interaction: datetime
    interaction_count: int

@dataclass
class ProductRecommendation:
    """Recomendação personalizada de produto"""
    sku: str
    name: str
    brand: str
    esg_score: float
    price: float
    discount_percentage: float
    reason: str
    confidence: float
    category: str

class SEVEPersonalizationEngine:
    """Engine de personalização ética usando SYMBEON SEVE"""
    
    def __init__(self):
        self.profiles_cache = {}  # Cache em memória (em produção usar Redis)
        self.esg_brands_db = self._load_esg_brands()
        self.behavioral_patterns = {}
        
    def _load_esg_brands(self) -> Dict:
        """Carrega base de marcas ESG parceiras"""
        return {
            "alimentacao": {
                "premium_esg": ["Organic", "Native", "Taeq", "Carrefour Bio"],
                "mainstream_esg": ["Nestlé", "Unilever", "Danone"],
                "local_sustainable": ["Fazenda Futuro", "Superbom", "Wickbold"]
            },
            "limpeza": {
                "premium_esg": ["Ypê", "Minuano", "Extrato"],
                "mainstream_esg": ["OMO", "Comfort", "Veja"],
                "eco_friendly": ["Biowash", "Ecover", "Seventh Generation"]
            },
            "higiene": {
                "premium_esg": ["Natura", "Boticário", "Granado"],
                "mainstream_esg": ["Unilever", "P&G", "Johnson's"],
                "natural": ["Weleda", "Davene", "Sallve"]
            }
        }
    
    async def create_anonymous_profile(self, interaction_data: Dict) -> PersonalizationProfile:
        """Cria perfil anônimo inicial baseado na primeira interação"""
        
        # Gerar ID anônimo criptográfico
        timestamp = str(time.time())
        device_fingerprint = interaction_data.get("device_info", "unknown")
        location_hash = hashlib.sha256(
            f"{interaction_data.get('store_id', '')}{timestamp}".encode()
        ).hexdigest()[:16]
        
        anonymous_id = hashlib.sha256(
            f"{device_fingerprint}{location_hash}{timestamp}".encode()
        ).hexdigest()[:32]
        
        # Análise comportamental inicial (sem dados pessoais)
        behavioral_signals = {
            "entry_time": interaction_data.get("entry_time", datetime.now().hour),
            "device_type": interaction_data.get("device_type", "mobile"),
            "interaction_speed": interaction_data.get("interaction_speed", "medium"),
            "store_section": interaction_data.get("store_section", "entrance")
        }
        
        behavioral_hash = hashlib.sha256(
            json.dumps(behavioral_signals, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        # Inferir preferências iniciais baseadas em contexto
        initial_preferences = await self._infer_initial_preferences(behavioral_signals)
        
        profile = PersonalizationProfile(
            anonymous_id=anonymous_id,
            behavioral_hash=behavioral_hash,
            preferences=initial_preferences,
            esg_affinity=0.5,  # Neutro inicial
            brand_preferences=[],
            category_interests=[],
            price_sensitivity="medium",
            sustainability_score=0.0,
            created_at=datetime.now(),
            last_interaction=datetime.now(),
            interaction_count=1
        )
        
        # Cache do perfil
        self.profiles_cache[anonymous_id] = profile
        
        logger.info(f"🎯 Perfil anônimo criado: {anonymous_id[:8]}...")
        return profile
    
    async def _infer_initial_preferences(self, behavioral_signals: Dict) -> Dict:
        """Infere preferências iniciais baseadas em sinais comportamentais"""
        preferences = {
            "time_conscious": False,
            "tech_savvy": False,
            "sustainability_interested": False,
            "premium_oriented": False,
            "family_oriented": False
        }
        
        # Análise por horário
        entry_hour = behavioral_signals.get("entry_time", 12)
        if 7 <= entry_hour <= 9 or 17 <= entry_hour <= 19:
            preferences["time_conscious"] = True
        
        # Análise por dispositivo
        if behavioral_signals.get("device_type") == "smartphone":
            preferences["tech_savvy"] = True
        
        # Análise por velocidade de interação
        if behavioral_signals.get("interaction_speed") == "fast":
            preferences["time_conscious"] = True
        elif behavioral_signals.get("interaction_speed") == "slow":
            preferences["premium_oriented"] = True
        
        # Análise por seção da loja
        store_section = behavioral_signals.get("store_section", "")
        if "organicos" in store_section.lower() or "sustentavel" in store_section.lower():
            preferences["sustainability_interested"] = True
        
        return preferences
    
    async def generate_personalized_recommendations(
        self, 
        anonymous_id: str, 
        context: Dict
    ) -> List[ProductRecommendation]:
        """Gera recomendações personalizadas baseadas no perfil"""
        
        profile = self.profiles_cache.get(anonymous_id)
        if not profile:
            logger.warning(f"Perfil não encontrado: {anonymous_id}")
            return []
        
        recommendations = []
        store_section = context.get("current_section", "geral")
        
        # Recomendações baseadas em ESG affinity
        if profile.esg_affinity > 0.6:
            esg_recs = await self._get_esg_recommendations(profile, store_section)
            recommendations.extend(esg_recs)
        
        # Recomendações baseadas em preferências
        pref_recs = await self._get_preference_recommendations(profile, store_section)
        recommendations.extend(pref_recs)
        
        # Recomendações baseadas em contexto temporal
        temporal_recs = await self._get_temporal_recommendations(profile, context)
        recommendations.extend(temporal_recs)
        
        # Ordenar por confidence e limitar
        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        return recommendations[:5]  # Top 5 recomendações
    
    async def _get_esg_recommendations(
        self, 
        profile: PersonalizationProfile, 
        section: str
    ) -> List[ProductRecommendation]:
        """Recomendações focadas em ESG"""
        recommendations = []
        
        # Mapear seção para categoria ESG
        category_map = {
            "alimentacao": "alimentacao",
            "limpeza": "limpeza", 
            "higiene": "higiene",
            "bebidas": "alimentacao"
        }
        
        category = category_map.get(section, "alimentacao")
        esg_brands = self.esg_brands_db.get(category, {})
        
        # Produtos ESG premium
        if profile.preferences.get("premium_oriented"):
            premium_brands = esg_brands.get("premium_esg", [])
            for brand in premium_brands[:2]:
                recommendations.append(ProductRecommendation(
                    sku=f"esg_{brand.lower().replace(' ', '_')}_001",
                    name=f"Produto {brand} Sustentável",
                    brand=brand,
                    esg_score=8.5,
                    price=15.90,
                    discount_percentage=10.0,
                    reason="Marca premium com alto impacto ESG",
                    confidence=0.85,
                    category=category
                ))
        
        # Produtos ESG mainstream
        else:
            mainstream_brands = esg_brands.get("mainstream_esg", [])
            for brand in mainstream_brands[:2]:
                recommendations.append(ProductRecommendation(
                    sku=f"esg_{brand.lower().replace(' ', '_')}_002",
                    name=f"Produto {brand} Eco",
                    brand=brand,
                    esg_score=7.2,
                    price=8.90,
                    discount_percentage=15.0,
                    reason="Marca conhecida com compromisso sustentável",
                    confidence=0.75,
                    category=category
                ))
        
        return recommendations
    
    async def _get_preference_recommendations(
        self, 
        profile: PersonalizationProfile, 
        section: str
    ) -> List[ProductRecommendation]:
        """Recomendações baseadas em preferências comportamentais"""
        recommendations = []
        
        # Time-conscious: produtos de conveniência
        if profile.preferences.get("time_conscious"):
            recommendations.append(ProductRecommendation(
                sku="conv_ready_meal_001",
                name="Refeição Pronta Saudável",
                brand="Sadia",
                esg_score=6.0,
                price=12.90,
                discount_percentage=20.0,
                reason="Economia de tempo para rotina corrida",
                confidence=0.80,
                category="conveniencia"
            ))
        
        # Family-oriented: produtos familiares
        if profile.preferences.get("family_oriented"):
            recommendations.append(ProductRecommendation(
                sku="fam_pack_001",
                name="Pack Familiar Econômico",
                brand="Nestlé",
                esg_score=6.5,
                price=25.90,
                discount_percentage=25.0,
                reason="Ideal para famílias, melhor custo-benefício",
                confidence=0.75,
                category="familia"
            ))
        
        return recommendations
    
    async def _get_temporal_recommendations(
        self, 
        profile: PersonalizationProfile, 
        context: Dict
    ) -> List[ProductRecommendation]:
        """Recomendações baseadas em contexto temporal"""
        recommendations = []
        current_hour = datetime.now().hour
        
        # Manhã: café da manhã
        if 6 <= current_hour <= 10:
            recommendations.append(ProductRecommendation(
                sku="breakfast_001",
                name="Combo Café da Manhã Saudável",
                brand="Wickbold",
                esg_score=7.0,
                price=18.90,
                discount_percentage=15.0,
                reason="Perfeito para começar o dia com energia",
                confidence=0.70,
                category="cafe_manha"
            ))
        
        # Tarde: lanche
        elif 14 <= current_hour <= 17:
            recommendations.append(ProductRecommendation(
                sku="snack_001",
                name="Lanche Natural Orgânico",
                brand="Native",
                esg_score=8.0,
                price=8.90,
                discount_percentage=10.0,
                reason="Lanche saudável para a tarde",
                confidence=0.65,
                category="lanche"
            ))
        
        return recommendations
    
    async def update_profile_interaction(
        self, 
        anonymous_id: str, 
        interaction_data: Dict
    ) -> PersonalizationProfile:
        """Atualiza perfil baseado em nova interação"""
        
        profile = self.profiles_cache.get(anonymous_id)
        if not profile:
            logger.warning(f"Perfil não encontrado para atualização: {anonymous_id}")
            return None
        
        # Atualizar contadores
        profile.interaction_count += 1
        profile.last_interaction = datetime.now()
        
        # Atualizar ESG affinity baseado em comportamento
        if interaction_data.get("viewed_esg_products"):
            profile.esg_affinity = min(1.0, profile.esg_affinity + 0.1)
        
        if interaction_data.get("purchased_esg_products"):
            profile.esg_affinity = min(1.0, profile.esg_affinity + 0.2)
        
        # Atualizar preferências de marca
        viewed_brands = interaction_data.get("viewed_brands", [])
        for brand in viewed_brands:
            if brand not in profile.brand_preferences:
                profile.brand_preferences.append(brand)
        
        # Atualizar interesses de categoria
        viewed_categories = interaction_data.get("viewed_categories", [])
        for category in viewed_categories:
            if category not in profile.category_interests:
                profile.category_interests.append(category)
        
        # Atualizar sensibilidade a preço
        if interaction_data.get("price_comparison_behavior"):
            profile.price_sensitivity = "high"
        elif interaction_data.get("premium_product_views"):
            profile.price_sensitivity = "low"
        
        # Calcular sustainability score
        profile.sustainability_score = self._calculate_sustainability_score(profile)
        
        logger.info(f"🔄 Perfil atualizado: {anonymous_id[:8]}... (ESG: {profile.esg_affinity:.2f})")
        return profile
    
    def _calculate_sustainability_score(self, profile: PersonalizationProfile) -> float:
        """Calcula score de sustentabilidade do usuário"""
        score = 0.0
        
        # Base ESG affinity
        score += profile.esg_affinity * 0.4
        
        # Preferências sustentáveis
        if profile.preferences.get("sustainability_interested"):
            score += 0.3
        
        # Marcas ESG nas preferências
        esg_brand_count = 0
        all_esg_brands = []
        for category in self.esg_brands_db.values():
            for tier in category.values():
                all_esg_brands.extend(tier)
        
        for brand in profile.brand_preferences:
            if brand in all_esg_brands:
                esg_brand_count += 1
        
        if profile.brand_preferences:
            esg_ratio = esg_brand_count / len(profile.brand_preferences)
            score += esg_ratio * 0.3
        
        return min(1.0, score)
    
    async def get_guardpass_upgrade_suggestion(
        self, 
        anonymous_id: str
    ) -> Optional[Dict]:
        """Sugere upgrade para GuardPass baseado no perfil"""
        
        profile = self.profiles_cache.get(anonymous_id)
        if not profile:
            return None
        
        # Critérios para sugerir upgrade
        should_suggest = (
            profile.interaction_count >= 3 or
            profile.esg_affinity > 0.7 or
            profile.sustainability_score > 0.6 or
            len(profile.brand_preferences) >= 5
        )
        
        if not should_suggest:
            return None
        
        # Personalizar benefícios baseado no perfil
        benefits = []
        
        if profile.esg_affinity > 0.6:
            benefits.append("🌱 Cashback duplo em produtos ESG")
            benefits.append("📊 Relatório pessoal de impacto ambiental")
        
        if profile.preferences.get("time_conscious"):
            benefits.append("⚡ Checkout prioritário sem filas")
            benefits.append("🚀 Recomendações express personalizadas")
        
        if profile.sustainability_score > 0.5:
            benefits.append("🏆 Acesso ao marketplace sustentável exclusivo")
            benefits.append("🎯 Metas de sustentabilidade gamificadas")
        
        return {
            "should_suggest": True,
            "confidence": min(0.95, profile.sustainability_score + profile.esg_affinity),
            "personalized_benefits": benefits,
            "suggested_tier": "premium" if profile.esg_affinity > 0.8 else "basic",
            "incentive": "15% desconto no primeiro mês" if profile.price_sensitivity == "high" else "Primeiro mês grátis"
        }
    
    async def export_anonymous_insights(self, store_id: str) -> Dict:
        """Exporta insights anônimos agregados para o varejista"""
        
        # Agregar dados de todos os perfis (anonimizados)
        total_profiles = len(self.profiles_cache)
        if total_profiles == 0:
            return {"error": "Nenhum perfil disponível"}
        
        # Métricas agregadas
        avg_esg_affinity = sum(p.esg_affinity for p in self.profiles_cache.values()) / total_profiles
        avg_sustainability = sum(p.sustainability_score for p in self.profiles_cache.values()) / total_profiles
        
        # Top categorias de interesse
        all_categories = []
        for profile in self.profiles_cache.values():
            all_categories.extend(profile.category_interests)
        
        category_counts = {}
        for cat in all_categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Distribuição de sensibilidade a preço
        price_sensitivity_dist = {"low": 0, "medium": 0, "high": 0}
        for profile in self.profiles_cache.values():
            price_sensitivity_dist[profile.price_sensitivity] += 1
        
        return {
            "store_id": store_id,
            "total_anonymous_profiles": total_profiles,
            "avg_esg_affinity": round(avg_esg_affinity, 2),
            "avg_sustainability_score": round(avg_sustainability, 2),
            "top_categories": top_categories,
            "price_sensitivity_distribution": price_sensitivity_dist,
            "guardpass_conversion_potential": sum(
                1 for p in self.profiles_cache.values() 
                if p.esg_affinity > 0.6 or p.sustainability_score > 0.5
            ),
            "generated_at": datetime.now().isoformat()
        }

# Instância global do engine
seve_personalization = SEVEPersonalizationEngine()
