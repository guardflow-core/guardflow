"""
API do Agente Simbiótico Especializado para Checkout
Endpoints específicos para checkout com integração SYMBEON
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from app.agents.checkout_symbiotic_agent import CheckoutSymbioticAgent, CheckoutStage, CheckoutEmotion
from app.core.auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

# Instância global do agente simbiótico de checkout
checkout_agent = CheckoutSymbioticAgent()

class CheckoutInteraction(BaseModel):
    text: str
    user_id: str
    session_id: str
    stage: str
    scan_count: int = 0
    total_items: int = 0
    esg_score: float = 0.0
    checkout_speed: float = 0.0
    error_count: int = 0
    context: Optional[Dict[str, Any]] = {}

class CheckoutResponse(BaseModel):
    response: Dict[str, Any]
    symbeon_analysis: Dict[str, Any]
    checkout_insights: List[Dict[str, Any]]
    learning_data: Dict[str, Any]
    emotional_state: str
    confidence: float
    symbeon_component: str
    timestamp: datetime

class CheckoutSummary(BaseModel):
    checkout_context: Dict[str, Any]
    symbeon_personality: Dict[str, Any]
    learning_data: Dict[str, Any]
    symbeon_integration: Dict[str, Any]

@router.post("/checkout-chat", response_model=CheckoutResponse)
async def chat_with_checkout_agent(
    interaction: CheckoutInteraction,
    current_user: dict = Depends(get_current_user)
):
    """
    Chat com o agente simbiótico especializado em checkout
    """
    try:
        # Processar interação de checkout
        result = await checkout_agent.process_checkout_interaction(
            interaction.user_id,
            {
                "text": interaction.text,
                "session_id": interaction.session_id,
                "stage": interaction.stage,
                "scan_count": interaction.scan_count,
                "total_items": interaction.total_items,
                "esg_score": interaction.esg_score,
                "checkout_speed": interaction.checkout_speed,
                "error_count": interaction.error_count,
                "context": interaction.context
            }
        )
        
        return CheckoutResponse(
            response=result["response"],
            symbeon_analysis=result["symbeon_analysis"],
            checkout_insights=[
                {
                    "type": insight.insight_type,
                    "description": insight.description,
                    "confidence": insight.confidence,
                    "symbeon_component": insight.symbeon_component,
                    "actionable": insight.actionable,
                    "priority": insight.priority,
                    "emotional_impact": insight.emotional_impact
                }
                for insight in result["checkout_insights"]
            ],
            learning_data=result["learning_data"],
            emotional_state=result["emotional_state"],
            confidence=result["confidence"],
            symbeon_component=result["symbeon_component"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Erro no chat de checkout: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do agente de checkout")

@router.get("/checkout-context/{user_id}", response_model=Dict[str, Any])
async def get_checkout_context(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém contexto atual do checkout
    """
    try:
        if user_id not in checkout_agent.checkout_contexts:
            raise HTTPException(status_code=404, detail="Contexto de checkout não encontrado")
        
        context = checkout_agent.checkout_contexts[user_id]
        
        return {
            "user_id": context.user_id,
            "session_id": context.session_id,
            "current_stage": context.current_stage.value,
            "emotional_state": context.emotional_state.value,
            "scan_count": context.scan_count,
            "total_items": context.total_items,
            "esg_score": context.esg_score,
            "checkout_speed": context.checkout_speed,
            "error_count": context.error_count,
            "user_preferences": context.user_preferences,
            "system_performance": context.system_performance
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter contexto de checkout: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.get("/checkout-summary/{user_id}", response_model=CheckoutSummary)
async def get_checkout_symbiotic_summary(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém resumo simbiótico completo do checkout
    """
    try:
        summary = await checkout_agent.get_checkout_symbiotic_summary(user_id)
        
        return CheckoutSummary(
            checkout_context=summary["checkout_context"],
            symbeon_personality=summary["symbeon_personality"],
            learning_data=summary["learning_data"],
            symbeon_integration=summary["symbeon_integration"]
        )
        
    except Exception as e:
        logger.error(f"Erro ao obter resumo simbiótico de checkout: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.post("/checkout-stage/{user_id}")
async def update_checkout_stage(
    user_id: str,
    stage: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza estágio do checkout
    """
    try:
        if user_id not in checkout_agent.checkout_contexts:
            raise HTTPException(status_code=404, detail="Contexto de checkout não encontrado")
        
        context = checkout_agent.checkout_contexts[user_id]
        context.current_stage = CheckoutStage(stage)
        
        return {
            "status": "success",
            "message": f"Estágio atualizado para {stage}",
            "current_stage": context.current_stage.value,
            "timestamp": datetime.now().isoformat()
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Estágio inválido")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar estágio: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.post("/checkout-emotion/{user_id}")
async def update_checkout_emotion(
    user_id: str,
    emotion: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza estado emocional do checkout
    """
    try:
        if user_id not in checkout_agent.checkout_contexts:
            raise HTTPException(status_code=404, detail="Contexto de checkout não encontrado")
        
        context = checkout_agent.checkout_contexts[user_id]
        context.emotional_state = CheckoutEmotion(emotion)
        
        return {
            "status": "success",
            "message": f"Estado emocional atualizado para {emotion}",
            "emotional_state": context.emotional_state.value,
            "timestamp": datetime.now().isoformat()
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Emoção inválida")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar emoção: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.get("/checkout-insights/{user_id}")
async def get_checkout_insights(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém insights específicos do checkout
    """
    try:
        if user_id not in checkout_agent.checkout_contexts:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        context = checkout_agent.checkout_contexts[user_id]
        
        # Gerar insights baseados no contexto
        insights = []
        
        # Insight de performance
        if context.checkout_speed > 3.0:
            insights.append({
                "type": "performance_optimization",
                "description": "Checkout pode ser otimizado para maior velocidade",
                "confidence": 0.9,
                "priority": "high",
                "actionable": True
            })
        
        # Insight ESG
        if context.esg_score > 0.7:
            insights.append({
                "type": "esg_achievement",
                "description": "Excelente escolha de produtos sustentáveis",
                "confidence": 0.8,
                "priority": "medium",
                "actionable": False
            })
        
        # Insight de erro
        if context.error_count > 2:
            insights.append({
                "type": "error_prevention",
                "description": "Muitos erros detectados, oferecer suporte adicional",
                "confidence": 0.9,
                "priority": "high",
                "actionable": True
            })
        
        return {
            "user_id": user_id,
            "insights": insights,
            "total_insights": len(insights),
            "actionable_insights": len([i for i in insights if i["actionable"]]),
            "context": {
                "stage": context.current_stage.value,
                "emotional_state": context.emotional_state.value,
                "performance": {
                    "speed": context.checkout_speed,
                    "accuracy": 1.0 - (context.error_count / max(context.scan_count, 1)),
                    "esg_score": context.esg_score
                }
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter insights de checkout: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.post("/checkout-optimization/{user_id}")
async def request_checkout_optimization(
    user_id: str,
    optimization_type: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Solicita otimização específica do checkout
    """
    try:
        if user_id not in checkout_agent.checkout_contexts:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        context = checkout_agent.checkout_contexts[user_id]
        
        # Gerar otimizações baseadas no tipo
        optimizations = []
        
        if optimization_type == "performance":
            if context.checkout_speed > 3.0:
                optimizations.append("Implementar checkout expresso")
            if context.error_count > 1:
                optimizations.append("Melhorar precisão do scanner")
        
        elif optimization_type == "esg":
            if context.esg_score < 0.5:
                optimizations.append("Sugerir produtos mais sustentáveis")
            optimizations.append("Mostrar impacto ESG dos produtos")
        
        elif optimization_type == "user_experience":
            if context.emotional_state == CheckoutEmotion.FRUSTRATED:
                optimizations.append("Simplificar interface")
            if context.scan_count > 20:
                optimizations.append("Otimizar para muitos itens")
        
        return {
            "user_id": user_id,
            "optimization_type": optimization_type,
            "optimizations": optimizations,
            "priority": "high" if len(optimizations) > 0 else "low",
            "expected_improvement": "20-30% mais eficiente",
            "implementation_time": "Imediato"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao gerar otimização: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.get("/symbeon-tools")
async def get_symbeon_tools(
    current_user: dict = Depends(get_current_user)
):
    """
    Lista ferramentas SYMBEON disponíveis para checkout
    """
    try:
        tools = list(checkout_agent.symbeon_tools.keys())
        
        return {
            "available_tools": tools,
            "total_tools": len(tools),
            "description": "Ferramentas SYMBEON disponíveis para checkout simbiótico",
            "integration_level": "high",
            "personalization": True
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar ferramentas SYMBEON: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.get("/checkout-learning/{user_id}")
async def get_checkout_learning_data(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtém dados de aprendizado do checkout
    """
    try:
        if user_id not in checkout_agent.learning_patterns:
            return {
                "user_id": user_id,
                "learning_data": [],
                "total_interactions": 0,
                "success_rate": 0.0,
                "preferred_stage": "entry"
            }
        
        learning_data = checkout_agent.learning_patterns[user_id]
        
        return {
            "user_id": user_id,
            "learning_data": learning_data[-10:],  # Últimas 10 interações
            "total_interactions": len(learning_data),
            "success_rate": checkout_agent._calculate_success_rate(user_id),
            "preferred_stage": checkout_agent._get_preferred_stage(user_id),
            "learning_progress": min(len(learning_data) / 50, 1.0)
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter dados de aprendizado: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")
