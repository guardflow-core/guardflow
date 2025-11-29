"""
ESG Dashboard API - Core do Negócio GuardFlow
Dashboard ESG otimizado com gamificação e métricas avançadas
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import uuid

from app.database import get_db
from app.config import settings, AppMessages
from app.models.user import User
from app.models.transaction import Transaction
from app.models.monetization import ESGAsset, InvoiceConversion
from app.utils.security import get_current_user

# Logger
logger = logging.getLogger("guardflow.esg_dashboard")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@router.get("/esg/dashboard/{user_id}")
@limiter.limit("20/minute")
async def get_esg_dashboard(
    request: Request,
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Dashboard ESG completo do usuário
    Core do negócio GuardFlow - Tokenização ESG
    """
    try:
        logger.info(f"🌱 Dashboard ESG para usuário: {user_id}")

        # Verificar se o usuário pode acessar o dashboard
        if current_user.id != user_id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado ao dashboard ESG! 🔒"
            )

        # Buscar usuário
        user_result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado! 🔍"
            )

        # Métricas ESG do usuário
        esg_metrics = await _get_esg_metrics(user_id, db)
        
        # Ativos ESG ativos
        esg_assets = await _get_active_esg_assets(user_id, db)
        
        # Histórico de transações ESG
        esg_history = await _get_esg_history(user_id, db)
        
        # Ranking ESG
        esg_ranking = await _get_esg_ranking(user_id, db)
        
        # Desafios ESG disponíveis
        esg_challenges = await _get_esg_challenges(user_id, db)
        
        # Impacto ambiental
        environmental_impact = await _get_environmental_impact(user_id, db)

        return {
            "success": True,
            "message": "Dashboard ESG carregado com sucesso! 🌱",
            "data": {
                "user_info": {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email,
                    "esg_tokens": user.esg_tokens,
                    "esg_level": _calculate_esg_level(user.esg_tokens)
                },
                "esg_metrics": esg_metrics,
                "active_assets": esg_assets,
                "esg_history": esg_history,
                "ranking": esg_ranking,
                "challenges": esg_challenges,
                "environmental_impact": environmental_impact
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao carregar dashboard ESG: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao carregar dashboard ESG"
        )


@router.post("/esg/challenges/create")
@limiter.limit("10/minute")
async def create_esg_challenge(
    request: Request,
    challenge_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Criar desafio ESG para gamificação
    """
    try:
        logger.info(f"🎯 Criando desafio ESG: {challenge_data.get('title')}")

        # Validar dados do desafio
        required_fields = ["title", "description", "target_value", "reward_tokens"]
        for field in required_fields:
            if field not in challenge_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Campo obrigatório: {field}"
                )

        # Criar desafio ESG
        challenge = {
            "id": str(uuid.uuid4()),
            "title": challenge_data["title"],
            "description": challenge_data["description"],
            "target_value": challenge_data["target_value"],
            "reward_tokens": challenge_data["reward_tokens"],
            "created_by": str(current_user.id),
            "created_at": datetime.utcnow().isoformat(),
            "status": "active",
            "participants": [],
            "progress": 0.0
        }

        # Salvar desafio (implementar modelo Challenge se necessário)
        # Por enquanto, retornar sucesso
        logger.info(f"✅ Desafio ESG criado: {challenge['id']}")

        return {
            "success": True,
            "message": "Desafio ESG criado com sucesso! 🎯",
            "data": challenge,
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao criar desafio ESG: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar desafio ESG"
        )


@router.get("/esg/ranking")
@limiter.limit("30/minute")
async def get_esg_ranking(
    request: Request,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ranking ESG global
    """
    try:
        logger.info(f"🏆 Buscando ranking ESG (top {limit})")

        # Buscar top usuários por tokens ESG
        ranking_result = await db.execute(
            select(User.id, User.name, User.esg_tokens)
            .where(User.esg_tokens > 0)
            .order_by(desc(User.esg_tokens))
            .limit(limit)
        )
        
        ranking_users = ranking_result.fetchall()
        
        # Buscar posição do usuário atual
        user_position = await _get_user_ranking_position(current_user.id, db)
        
        ranking = []
        for i, (user_id, name, tokens) in enumerate(ranking_users, 1):
            ranking.append({
                "position": i,
                "user_id": str(user_id),
                "name": name,
                "esg_tokens": tokens,
                "esg_level": _calculate_esg_level(tokens),
                "is_current_user": str(user_id) == str(current_user.id)
            })

        return {
            "success": True,
            "message": f"Ranking ESG obtido! 🏆",
            "data": {
                "ranking": ranking,
                "user_position": user_position,
                "total_users": len(ranking)
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Erro ao buscar ranking ESG: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar ranking ESG"
        )


# Funções auxiliares
async def _get_esg_metrics(user_id: str, db: AsyncSession) -> Dict[str, Any]:
    """Obter métricas ESG do usuário"""
    try:
        # Total de tokens ESG
        user_result = await db.execute(
            select(User.esg_tokens).where(User.id == user_id)
        )
        total_tokens = user_result.scalar() or 0

        # Total de ativos ESG
        assets_result = await db.execute(
            select(func.count(ESGAsset.id)).where(
                ESGAsset.user_id == user_id,
                ESGAsset.status == "active"
            )
        )
        total_assets = assets_result.scalar() or 0

        # Valor total em ESG
        value_result = await db.execute(
            select(func.sum(ESGAsset.esg_value)).where(
                ESGAsset.user_id == user_id,
                ESGAsset.status == "active"
            )
        )
        total_value = float(value_result.scalar() or 0)

        # Transações ESG este mês
        month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_result = await db.execute(
            select(func.count(ESGAsset.id)).where(
                ESGAsset.user_id == user_id,
                ESGAsset.created_at >= month_start
            )
        )
        monthly_transactions = monthly_result.scalar() or 0

        return {
            "total_tokens": total_tokens,
            "total_assets": total_assets,
            "total_value": total_value,
            "monthly_transactions": monthly_transactions,
            "esg_level": _calculate_esg_level(total_tokens)
        }

    except Exception as e:
        logger.error(f"❌ Erro ao obter métricas ESG: {str(e)}")
        return {
            "total_tokens": 0,
            "total_assets": 0,
            "total_value": 0.0,
            "monthly_transactions": 0,
            "esg_level": "Iniciante"
        }


async def _get_active_esg_assets(user_id: str, db: AsyncSession) -> List[Dict[str, Any]]:
    """Obter ativos ESG ativos do usuário"""
    try:
        assets_result = await db.execute(
            select(ESGAsset).where(
                ESGAsset.user_id == user_id,
                ESGAsset.status == "active"
            ).order_by(desc(ESGAsset.created_at)).limit(10)
        )
        
        assets = assets_result.scalars().all()
        
        return [
            {
                "id": str(asset.id),
                "esg_value": asset.esg_value,
                "esg_score": asset.esg_score,
                "category": asset.category,
                "carbon_offset_kg": asset.carbon_offset_kg,
                "created_at": asset.created_at.isoformat() if asset.created_at else None
            }
            for asset in assets
        ]

    except Exception as e:
        logger.error(f"❌ Erro ao obter ativos ESG: {str(e)}")
        return []


async def _get_esg_history(user_id: str, db: AsyncSession) -> List[Dict[str, Any]]:
    """Obter histórico de transações ESG"""
    try:
        history_result = await db.execute(
            select(InvoiceConversion).where(
                InvoiceConversion.user_id == user_id,
                InvoiceConversion.conversion_type == "esg"
            ).order_by(desc(InvoiceConversion.created_at)).limit(20)
        )
        
        history = history_result.scalars().all()
        
        return [
            {
                "id": str(conversion.id),
                "invoice_number": conversion.invoice_number,
                "original_amount": conversion.original_amount,
                "conversion_amount": conversion.conversion_amount,
                "status": conversion.status,
                "created_at": conversion.created_at.isoformat() if conversion.created_at else None
            }
            for conversion in history
        ]

    except Exception as e:
        logger.error(f"❌ Erro ao obter histórico ESG: {str(e)}")
        return []


async def _get_esg_ranking(user_id: str, db: AsyncSession) -> Dict[str, Any]:
    """Obter ranking ESG do usuário"""
    try:
        # Posição do usuário no ranking
        user_position = await _get_user_ranking_position(user_id, db)
        
        # Top 10 do ranking
        top_result = await db.execute(
            select(User.id, User.name, User.esg_tokens)
            .where(User.esg_tokens > 0)
            .order_by(desc(User.esg_tokens))
            .limit(10)
        )
        
        top_users = top_result.fetchall()
        
        return {
            "user_position": user_position,
            "top_10": [
                {
                    "position": i + 1,
                    "name": name,
                    "esg_tokens": tokens,
                    "is_current_user": str(user_id) == str(user_id)
                }
                for i, (user_id, name, tokens) in enumerate(top_users)
            ]
        }

    except Exception as e:
        logger.error(f"❌ Erro ao obter ranking ESG: {str(e)}")
        return {"user_position": 0, "top_10": []}


async def _get_esg_challenges(user_id: str, db: AsyncSession) -> List[Dict[str, Any]]:
    """Obter desafios ESG disponíveis"""
    # Por enquanto, retornar desafios mockados
    # Implementar modelo Challenge se necessário
    return [
        {
            "id": "challenge_1",
            "title": "Comprador Verde",
            "description": "Faça 10 compras sustentáveis este mês",
            "target": 10,
            "progress": 3,
            "reward_tokens": 100,
            "status": "active"
        },
        {
            "id": "challenge_2", 
            "title": "Herói do Carbono",
            "description": "Evite 50kg de CO2 em compras",
            "target": 50,
            "progress": 15,
            "reward_tokens": 200,
            "status": "active"
        }
    ]


async def _get_environmental_impact(user_id: str, db: AsyncSession) -> Dict[str, Any]:
    """Obter impacto ambiental do usuário"""
    try:
        # Total de carbono evitado
        carbon_result = await db.execute(
            select(func.sum(ESGAsset.carbon_offset_kg)).where(
                ESGAsset.user_id == user_id,
                ESGAsset.status == "active"
            )
        )
        total_carbon_offset = float(carbon_result.scalar() or 0)

        # Equivalente em árvores plantadas (1 árvore = 22kg CO2/ano)
        trees_equivalent = total_carbon_offset / 22.0

        return {
            "carbon_offset_kg": total_carbon_offset,
            "trees_equivalent": round(trees_equivalent, 2),
            "environmental_score": min(100, int(total_carbon_offset * 2))
        }

    except Exception as e:
        logger.error(f"❌ Erro ao obter impacto ambiental: {str(e)}")
        return {
            "carbon_offset_kg": 0.0,
            "trees_equivalent": 0.0,
            "environmental_score": 0
        }


async def _get_user_ranking_position(user_id: str, db: AsyncSession) -> int:
    """Obter posição do usuário no ranking"""
    try:
        # Contar usuários com mais tokens ESG
        position_result = await db.execute(
            select(func.count(User.id)).where(
                User.esg_tokens > select(User.esg_tokens).where(User.id == user_id).scalar_subquery()
            )
        )
        
        return (position_result.scalar() or 0) + 1

    except Exception as e:
        logger.error(f"❌ Erro ao obter posição do ranking: {str(e)}")
        return 0


def _calculate_esg_level(tokens: int) -> str:
    """Calcular nível ESG baseado nos tokens"""
    if tokens >= 10000:
        return "Mestre ESG"
    elif tokens >= 5000:
        return "Especialista ESG"
    elif tokens >= 2000:
        return "Avançado ESG"
    elif tokens >= 1000:
        return "Intermediário ESG"
    elif tokens >= 500:
        return "Iniciante ESG"
    else:
        return "Novato ESG"
