"""
API do Agente Simbiótico MCP
Endpoints para interação com o agente simbiótico
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from app.agents.symbiotic_agent import SymbioticAgent, SymbioticInsight
from app.core.auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

# Instância global do agente simbiótico
symbiotic_agent = SymbioticAgent()

class UserInput(BaseModel):
    text: str
    context: Optional[Dict[str, Any]] = {}
    user_id: str
    session_id: Optional[str] = None

class SymbioticResponse(BaseModel):
    response: Dict[str, Any]
    learning_data: Dict[str, Any]
    symbiotic_insights: List[Dict[str, Any]]
    emotional_state: str
    confidence: float
    timestamp: datetime

class LearningRecommendation(BaseModel):
    recommendation_type: str
    description: str
    priority: str
    actionable: bool
    confidence: float

class SymbioticSummary(BaseModel):
    user_profile: Dict[str, Any]
    system_context: Dict[str, Any]
    symbiotic_insights: List[Dict[str, Any]]
    learning_recommendations: List[LearningRecommendation]

@router.post("/chat", response_model=SymbioticResponse)
async def chat_with_agent(
    input_data: UserInput,
    current_user: dict = Depends(get_current_user)
):
    """
    Chat com o agente simbiótico
    """
    try:
        # Processar input do usuário
        result = await symbiotic_agent.process_user_input(
            input_data.user_id,
            {
                "text": input_data.text,
                "context": input_data.context,
                "session_id": input_data.session_id
            }
        )
        
        return SymbioticResponse(
            response=result["response"],
            learning_data=result["learning_data"],
            symbiotic_insights=[
                {
                    "type": insight.insight_type,
                    "description": insight.description,
                    "confidence": insight.confidence,
                    "source": insight.source,
                    "actionable": insight.actionable
                }
                for insight in result["symbiotic_insights"]
            ],
            emotional_state=result["emotional_state"],
            confidence=result["confidence"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Erro no chat com agente: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do agente simbiótico")

@router.get("/profile/{user_id}", response_model=Dict[str, Any])
async def get_user_profile(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém perfil simbiótico do usuário
    """
    try:
        profile = symbiotic_agent.user_profiles.get(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Perfil não encontrado")
        
        return {
            "user_id": profile.user_id,
            "learning_level": profile.learning_level.value,
            "emotional_state": profile.emotional_state.value,
            "interaction_count": len(profile.interaction_history),
            "goals": profile.goals,
            "pain_points": profile.pain_points,
            "success_patterns": profile.success_patterns,
            "preferences": profile.preferences
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter perfil: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.get("/summary/{user_id}", response_model=SymbioticSummary)
async def get_symbiotic_summary(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém resumo simbiótico completo
    """
    try:
        summary = await symbiotic_agent.get_symbiotic_summary(user_id)
        
        # Gerar recomendações de aprendizado
        learning_recommendations = await _generate_learning_recommendations(
            summary["user_profile"], summary["system_context"]
        )
        
        return SymbioticSummary(
            user_profile=summary["user_profile"],
            system_context=summary["system_context"],
            symbiotic_insights=summary["symbiotic_insights"],
            learning_recommendations=learning_recommendations
        )
        
    except Exception as e:
        logger.error(f"Erro ao obter resumo simbiótico: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.post("/learn")
async def submit_learning_feedback(
    user_id: str,
    feedback: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """
    Submete feedback de aprendizado para o agente
    """
    try:
        # Processar feedback de aprendizado
        learning_data = {
            "user_id": user_id,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat(),
            "type": feedback.get("type", "general")
        }
        
        # Atualizar perfil do usuário
        if user_id in symbiotic_agent.user_profiles:
            profile = symbiotic_agent.user_profiles[user_id]
            
            # Atualizar baseado no feedback
            if feedback.get("goal_achieved"):
                profile.success_patterns.append(feedback.get("pattern", ""))
            
            if feedback.get("pain_point"):
                profile.pain_points.append(feedback.get("pain_point", ""))
            
            if feedback.get("preference"):
                profile.preferences.update(feedback.get("preference", {}))
        
        return {
            "status": "success",
            "message": "Feedback processado com sucesso",
            "learning_data": learning_data
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar feedback: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.get("/insights/{user_id}")
async def get_symbiotic_insights(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém insights simbióticos para o usuário
    """
    try:
        if user_id not in symbiotic_agent.user_profiles:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        user_profile = symbiotic_agent.user_profiles[user_id]
        system_context = await symbiotic_agent._get_system_context()
        
        # Gerar insights baseados no contexto
        insights = await symbiotic_agent._generate_symbiotic_insights(
            user_profile, system_context, {}
        )
        
        return {
            "user_id": user_id,
            "insights": [
                {
                    "type": insight.insight_type,
                    "description": insight.description,
                    "confidence": insight.confidence,
                    "source": insight.source,
                    "actionable": insight.actionable,
                    "timestamp": insight.timestamp.isoformat()
                }
                for insight in insights
            ],
            "total_insights": len(insights),
            "actionable_insights": len([i for i in insights if i.actionable])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter insights: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.post("/optimize")
async def request_optimization(
    user_id: str,
    optimization_request: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """
    Solicita otimização baseada no contexto simbiótico
    """
    try:
        if user_id not in symbiotic_agent.user_profiles:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        user_profile = symbiotic_agent.user_profiles[user_id]
        system_context = await symbiotic_agent._get_system_context()
        
        # Gerar sugestões de otimização
        optimization_result = await symbiotic_agent._suggest_optimizations(
            optimization_request, user_profile, system_context
        )
        
        return {
            "user_id": user_id,
            "optimization_type": optimization_request.get("type", "general"),
            "suggestions": optimization_result.get("suggestions", []),
            "priority": optimization_result.get("priority", "medium"),
            "impact": optimization_result.get("impact", "Médio impacto esperado"),
            "confidence": 0.8
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao gerar otimização: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.get("/mcp-tools")
async def get_mcp_tools(
    current_user: dict = Depends(get_current_user)
):
    """
    Lista ferramentas MCP disponíveis
    """
    try:
        tools = list(symbiotic_agent.mcp_tools.keys())
        
        return {
            "available_tools": tools,
            "total_tools": len(tools),
            "description": "Ferramentas MCP disponíveis para o agente simbiótico"
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar ferramentas MCP: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

async def _generate_learning_recommendations(
    user_profile: Dict[str, Any], 
    system_context: Dict[str, Any]
) -> List[LearningRecommendation]:
    """Gera recomendações de aprendizado baseadas no contexto"""
    recommendations = []
    
    # Recomendação baseada no nível de aprendizado
    learning_level = user_profile.get("learning_level", "beginner")
    if learning_level == "beginner":
        recommendations.append(LearningRecommendation(
            recommendation_type="basic_training",
            description="Complete o tutorial básico do sistema",
            priority="high",
            actionable=True,
            confidence=0.9
        ))
    
    # Recomendação baseada na performance do sistema
    performance = system_context.get("performance", {})
    if performance.get("checkout_speed", 0) > 3.0:
        recommendations.append(LearningRecommendation(
            recommendation_type="performance_optimization",
            description="Aprenda sobre otimização de checkout",
            priority="high",
            actionable=True,
            confidence=0.8
        ))
    
    # Recomendação baseada no score ESG
    esg_score = system_context.get("esg_score", 0)
    if esg_score < 0.7:
        recommendations.append(LearningRecommendation(
            recommendation_type="esg_improvement",
            description="Melhore seu conhecimento sobre ESG",
            priority="medium",
            actionable=True,
            confidence=0.7
        ))
    
    return recommendations
