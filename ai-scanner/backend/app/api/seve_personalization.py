"""
API Endpoints para SEVE Personalization Engine
Integração da camada de personalização ética na jornada do usuário
"""

from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

from app.services.seve_personalization import seve_personalization, PersonalizationProfile, ProductRecommendation

router = APIRouter(prefix="/seve", tags=["SEVE Personalization"])

# === MODELS ===

class InitialInteractionRequest(BaseModel):
    store_id: str
    device_info: Optional[str] = None
    device_type: str = Field(default="mobile", pattern="^(mobile|tablet|kiosk)$")
    store_section: Optional[str] = "entrance"
    interaction_speed: Optional[str] = Field(default="medium", pattern="^(slow|medium|fast)$")

class PersonalizationResponse(BaseModel):
    anonymous_id: str
    behavioral_hash: str
    esg_affinity: float
    sustainability_score: float
    interaction_count: int
    created_at: datetime
    recommendations: List[Dict]
    guardpass_suggestion: Optional[Dict] = None

class InteractionUpdateRequest(BaseModel):
    viewed_esg_products: Optional[bool] = False
    purchased_esg_products: Optional[bool] = False
    viewed_brands: Optional[List[str]] = []
    viewed_categories: Optional[List[str]] = []
    price_comparison_behavior: Optional[bool] = False
    premium_product_views: Optional[bool] = False
    current_section: Optional[str] = "geral"

class RecommendationRequest(BaseModel):
    current_section: str = "geral"
    time_context: Optional[str] = None
    budget_range: Optional[str] = Field(None, pattern="^(low|medium|high)$")

# === ENDPOINTS ===

@router.post("/initialize", response_model=PersonalizationResponse)
async def initialize_personalization(req: InitialInteractionRequest):
    """
    Inicializa a camada de personalização SEVE
    Primeira interação do usuário - cria perfil anônimo
    """
    try:
        # Preparar dados de interação
        interaction_data = {
            "store_id": req.store_id,
            "device_info": req.device_info,
            "device_type": req.device_type,
            "store_section": req.store_section,
            "interaction_speed": req.interaction_speed,
            "entry_time": datetime.now().hour
        }
        
        # Criar perfil anônimo
        profile = await seve_personalization.create_anonymous_profile(interaction_data)
        
        # Gerar recomendações iniciais
        initial_context = {"current_section": req.store_section}
        recommendations = await seve_personalization.generate_personalized_recommendations(
            profile.anonymous_id, 
            initial_context
        )
        
        # Verificar sugestão de GuardPass
        guardpass_suggestion = await seve_personalization.get_guardpass_upgrade_suggestion(
            profile.anonymous_id
        )
        
        return PersonalizationResponse(
            anonymous_id=profile.anonymous_id,
            behavioral_hash=profile.behavioral_hash,
            esg_affinity=profile.esg_affinity,
            sustainability_score=profile.sustainability_score,
            interaction_count=profile.interaction_count,
            created_at=profile.created_at,
            recommendations=[
                {
                    "sku": rec.sku,
                    "name": rec.name,
                    "brand": rec.brand,
                    "esg_score": rec.esg_score,
                    "price": rec.price,
                    "discount_percentage": rec.discount_percentage,
                    "reason": rec.reason,
                    "confidence": rec.confidence,
                    "category": rec.category
                }
                for rec in recommendations
            ],
            guardpass_suggestion=guardpass_suggestion
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na inicialização SEVE: {str(e)}")


@router.post("/update/{anonymous_id}", response_model=PersonalizationResponse)
async def update_personalization(anonymous_id: str, req: InteractionUpdateRequest):
    """
    Atualiza perfil de personalização baseado em nova interação
    Aprendizado contínuo do comportamento do usuário
    """
    try:
        # Preparar dados de atualização
        interaction_data = {
            "viewed_esg_products": req.viewed_esg_products,
            "purchased_esg_products": req.purchased_esg_products,
            "viewed_brands": req.viewed_brands,
            "viewed_categories": req.viewed_categories,
            "price_comparison_behavior": req.price_comparison_behavior,
            "premium_product_views": req.premium_product_views
        }
        
        # Atualizar perfil
        updated_profile = await seve_personalization.update_profile_interaction(
            anonymous_id, 
            interaction_data
        )
        
        if not updated_profile:
            raise HTTPException(status_code=404, detail="Perfil anônimo não encontrado")
        
        # Gerar novas recomendações
        context = {"current_section": req.current_section}
        recommendations = await seve_personalization.generate_personalized_recommendations(
            anonymous_id, 
            context
        )
        
        # Verificar sugestão de GuardPass atualizada
        guardpass_suggestion = await seve_personalization.get_guardpass_upgrade_suggestion(
            anonymous_id
        )
        
        return PersonalizationResponse(
            anonymous_id=updated_profile.anonymous_id,
            behavioral_hash=updated_profile.behavioral_hash,
            esg_affinity=updated_profile.esg_affinity,
            sustainability_score=updated_profile.sustainability_score,
            interaction_count=updated_profile.interaction_count,
            created_at=updated_profile.created_at,
            recommendations=[
                {
                    "sku": rec.sku,
                    "name": rec.name,
                    "brand": rec.brand,
                    "esg_score": rec.esg_score,
                    "price": rec.price,
                    "discount_percentage": rec.discount_percentage,
                    "reason": rec.reason,
                    "confidence": rec.confidence,
                    "category": rec.category
                }
                for rec in recommendations
            ],
            guardpass_suggestion=guardpass_suggestion
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na atualização SEVE: {str(e)}")


@router.get("/recommendations/{anonymous_id}")
async def get_personalized_recommendations(
    anonymous_id: str,
    section: str = Query("geral", description="Seção atual da loja"),
    budget: Optional[str] = Query(None, pattern="^(low|medium|high)$")
):
    """
    Obtém recomendações personalizadas para contexto específico
    """
    try:
        context = {
            "current_section": section,
            "budget_range": budget,
            "timestamp": datetime.now().isoformat()
        }
        
        recommendations = await seve_personalization.generate_personalized_recommendations(
            anonymous_id, 
            context
        )
        
        return {
            "anonymous_id": anonymous_id,
            "context": context,
            "recommendations": [
                {
                    "sku": rec.sku,
                    "name": rec.name,
                    "brand": rec.brand,
                    "esg_score": rec.esg_score,
                    "price": rec.price,
                    "discount_percentage": rec.discount_percentage,
                    "reason": rec.reason,
                    "confidence": rec.confidence,
                    "category": rec.category
                }
                for rec in recommendations
            ],
            "total_recommendations": len(recommendations)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter recomendações: {str(e)}")


@router.get("/profile/{anonymous_id}")
async def get_anonymous_profile(anonymous_id: str):
    """
    Obtém perfil anônimo atual (dados não sensíveis)
    """
    try:
        profile = seve_personalization.profiles_cache.get(anonymous_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Perfil anônimo não encontrado")
        
        return {
            "anonymous_id": profile.anonymous_id,
            "behavioral_hash": profile.behavioral_hash,
            "esg_affinity": profile.esg_affinity,
            "sustainability_score": profile.sustainability_score,
            "price_sensitivity": profile.price_sensitivity,
            "interaction_count": profile.interaction_count,
            "created_at": profile.created_at,
            "last_interaction": profile.last_interaction,
            "preferences": profile.preferences,
            "category_interests": profile.category_interests[:5],  # Top 5
            "brand_preferences": profile.brand_preferences[:5]    # Top 5
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter perfil: {str(e)}")


@router.get("/guardpass-suggestion/{anonymous_id}")
async def get_guardpass_suggestion(anonymous_id: str):
    """
    Obtém sugestão personalizada de upgrade para GuardPass
    """
    try:
        suggestion = await seve_personalization.get_guardpass_upgrade_suggestion(anonymous_id)
        
        if not suggestion:
            return {
                "should_suggest": False,
                "reason": "Perfil ainda não elegível para GuardPass",
                "anonymous_id": anonymous_id
            }
        
        return {
            "anonymous_id": anonymous_id,
            **suggestion
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter sugestão GuardPass: {str(e)}")


@router.post("/convert-to-guardpass/{anonymous_id}")
async def convert_to_guardpass(anonymous_id: str, guardpass_token: str = Header(...)):
    """
    Converte perfil anônimo em GuardPass definitivo
    Migra dados de personalização para conta real
    """
    try:
        # Obter perfil anônimo
        profile = seve_personalization.profiles_cache.get(anonymous_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Perfil anônimo não encontrado")
        
        # Integrar com GuardPass (simulado)
        from app.services.guardpass_integration import guardpass_service
        guardpass_profile = await guardpass_service.get_user_profile(guardpass_token)
        
        if not guardpass_profile.get("user_id"):
            raise HTTPException(status_code=401, detail="Token GuardPass inválido")
        
        # Migrar dados de personalização (anonimizados)
        migration_data = {
            "esg_affinity": profile.esg_affinity,
            "sustainability_score": profile.sustainability_score,
            "preferences": profile.preferences,
            "category_interests": profile.category_interests,
            "price_sensitivity": profile.price_sensitivity,
            "interaction_count": profile.interaction_count,
            "behavioral_patterns": profile.behavioral_hash  # Hash apenas, não dados brutos
        }
        
        # Registrar conversão no GuardPass
        conversion_success = await guardpass_service.record_transaction(
            guardpass_profile["user_id"],
            {
                "transaction_type": "seve_conversion",
                "anonymous_profile_data": migration_data,
                "conversion_timestamp": datetime.now().isoformat()
            }
        )
        
        # Limpar cache anônimo
        if conversion_success:
            del seve_personalization.profiles_cache[anonymous_id]
        
        return {
            "conversion_success": conversion_success,
            "guardpass_user_id": guardpass_profile["user_id"],
            "migrated_data": {
                "esg_affinity": migration_data["esg_affinity"],
                "sustainability_score": migration_data["sustainability_score"],
                "interaction_count": migration_data["interaction_count"]
            },
            "message": "Perfil SEVE migrado com sucesso para GuardPass"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na conversão para GuardPass: {str(e)}")


@router.get("/analytics/{store_id}")
async def get_store_analytics(store_id: str):
    """
    Analytics agregados e anônimos para o varejista
    Insights de comportamento sem dados pessoais
    """
    try:
        insights = await seve_personalization.export_anonymous_insights(store_id)
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter analytics: {str(e)}")


@router.post("/reset/{anonymous_id}")
async def reset_anonymous_profile(anonymous_id: str):
    """
    Reset do perfil anônimo (LGPD compliance)
    """
    try:
        if anonymous_id in seve_personalization.profiles_cache:
            del seve_personalization.profiles_cache[anonymous_id]
            return {
                "reset_success": True,
                "anonymous_id": anonymous_id,
                "message": "Perfil anônimo removido com sucesso"
            }
        else:
            return {
                "reset_success": False,
                "anonymous_id": anonymous_id,
                "message": "Perfil não encontrado"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao resetar perfil: {str(e)}")


@router.get("/health")
async def seve_health_check():
    """Health check do SEVE Personalization Engine"""
    try:
        total_profiles = len(seve_personalization.profiles_cache)
        avg_esg = sum(p.esg_affinity for p in seve_personalization.profiles_cache.values()) / max(total_profiles, 1)
        
        return {
            "status": "healthy",
            "service": "SEVE Personalization Engine",
            "version": "1.0.0",
            "active_profiles": total_profiles,
            "avg_esg_affinity": round(avg_esg, 2),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "service": "SEVE Personalization Engine", 
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
