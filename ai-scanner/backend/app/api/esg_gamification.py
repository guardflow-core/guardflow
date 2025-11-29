"""
ESG Gamification API - Sistema de Gamificação ESG
Desafios, badges, rankings e recompensas ESG
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
from app.models.monetization import ESGAsset
from app.utils.security import get_current_user

# Logger
logger = logging.getLogger("guardflow.esg_gamification")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@router.post("/esg/challenges/join")
@limiter.limit("10/minute")
async def join_esg_challenge(
    request: Request,
    challenge_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Participar de um desafio ESG
    """
    try:
        logger.info(f"🎯 Usuário {current_user.id} entrando no desafio {challenge_id}")

        # Validar se o desafio existe (implementar modelo Challenge)
        # Por enquanto, simular validação
        challenge = await _get_challenge_by_id(challenge_id)
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Desafio ESG não encontrado! 🔍"
            )

        # Verificar se o usuário já está participando
        if await _is_user_in_challenge(current_user.id, challenge_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você já está participando deste desafio! ✅"
            )

        # Adicionar usuário ao desafio
        await _add_user_to_challenge(current_user.id, challenge_id)
        
        logger.info(f"✅ Usuário {current_user.id} adicionado ao desafio {challenge_id}")

        return {
            "success": True,
            "message": "Você entrou no desafio ESG! 🎯",
            "data": {
                "challenge_id": challenge_id,
                "challenge_title": challenge.get("title"),
                "user_id": str(current_user.id),
                "joined_at": datetime.utcnow().isoformat()
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao entrar no desafio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao entrar no desafio ESG"
        )


@router.get("/esg/badges/{user_id}")
@limiter.limit("30/minute")
async def get_user_badges(
    request: Request,
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obter badges ESG do usuário
    """
    try:
        logger.info(f"🏆 Buscando badges ESG do usuário: {user_id}")

        # Verificar permissão
        if current_user.id != user_id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado aos badges! 🔒"
            )

        # Calcular badges baseados nas métricas ESG
        badges = await _calculate_user_badges(user_id, db)

        return {
            "success": True,
            "message": "Badges ESG obtidos! 🏆",
            "data": {
                "user_id": user_id,
                "badges": badges,
                "total_badges": len(badges),
                "achievement_rate": len([b for b in badges if b["earned"]]) / max(len(badges), 1) * 100
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao buscar badges: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar badges ESG"
        )


@router.post("/esg/badges/claim")
@limiter.limit("5/minute")
async def claim_badge(
    request: Request,
    badge_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Reivindicar badge ESG
    """
    try:
        logger.info(f"🏆 Usuário {current_user.id} reivindicando badge {badge_id}")

        # Verificar se o badge pode ser reivindicado
        badge = await _get_badge_by_id(badge_id)
        if not badge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Badge não encontrado! 🔍"
            )

        # Verificar se o usuário já tem o badge
        if await _user_has_badge(current_user.id, badge_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você já possui este badge! ✅"
            )

        # Verificar se o usuário atende aos critérios
        if not await _user_meets_badge_criteria(current_user.id, badge_id, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você ainda não atende aos critérios para este badge! 📋"
            )

        # Reivindicar badge
        await _claim_badge_for_user(current_user.id, badge_id, badge.get("reward_tokens", 0))
        
        logger.info(f"✅ Badge {badge_id} reivindicado por {current_user.id}")

        return {
            "success": True,
            "message": f"Badge '{badge.get('title')}' reivindicado! 🏆",
            "data": {
                "badge_id": badge_id,
                "badge_title": badge.get("title"),
                "reward_tokens": badge.get("reward_tokens", 0),
                "claimed_at": datetime.utcnow().isoformat()
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao reivindicar badge: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao reivindicar badge ESG"
        )


@router.get("/esg/leaderboard")
@limiter.limit("30/minute")
async def get_esg_leaderboard(
    request: Request,
    period: str = "monthly",  # daily, weekly, monthly, yearly
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Leaderboard ESG por período
    """
    try:
        logger.info(f"🏆 Buscando leaderboard ESG ({period})")

        # Calcular período
        start_date = _calculate_period_start(period)
        
        # Buscar ranking ESG do período
        leaderboard = await _get_esg_leaderboard_data(start_date, limit, db)
        
        # Posição do usuário atual
        user_position = await _get_user_leaderboard_position(current_user.id, start_date, db)

        return {
            "success": True,
            "message": f"Leaderboard ESG ({period}) obtido! 🏆",
            "data": {
                "period": period,
                "start_date": start_date.isoformat(),
                "leaderboard": leaderboard,
                "user_position": user_position,
                "total_participants": len(leaderboard)
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Erro ao buscar leaderboard: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar leaderboard ESG"
        )


# Funções auxiliares
async def _get_challenge_by_id(challenge_id: str) -> Optional[Dict[str, Any]]:
    """Obter desafio por ID"""
    # Mock de desafios (implementar modelo Challenge)
    challenges = {
        "challenge_1": {
            "id": "challenge_1",
            "title": "Comprador Verde",
            "description": "Faça 10 compras sustentáveis este mês",
            "target": 10,
            "reward_tokens": 100,
            "status": "active"
        },
        "challenge_2": {
            "id": "challenge_2",
            "title": "Herói do Carbono",
            "description": "Evite 50kg de CO2 em compras",
            "target": 50,
            "reward_tokens": 200,
            "status": "active"
        }
    }
    return challenges.get(challenge_id)


async def _is_user_in_challenge(user_id: str, challenge_id: str) -> bool:
    """Verificar se usuário está no desafio"""
    # Mock (implementar modelo UserChallenge)
    return False


async def _add_user_to_challenge(user_id: str, challenge_id: str):
    """Adicionar usuário ao desafio"""
    # Mock (implementar modelo UserChallenge)
    pass


async def _calculate_user_badges(user_id: str, db: AsyncSession) -> List[Dict[str, Any]]:
    """Calcular badges ESG do usuário"""
    try:
        # Buscar métricas ESG do usuário
        user_result = await db.execute(
            select(User.esg_tokens).where(User.id == user_id)
        )
        esg_tokens = user_result.scalar() or 0

        # Buscar ativos ESG
        assets_result = await db.execute(
            select(func.count(ESGAsset.id), func.sum(ESGAsset.carbon_offset_kg)).where(
                ESGAsset.user_id == user_id,
                ESGAsset.status == "active"
            )
        )
        total_assets, total_carbon = assets_result.first() or (0, 0.0)

        # Definir badges ESG
        badges = [
            {
                "id": "first_esg",
                "title": "Primeiro Passo ESG",
                "description": "Faça sua primeira compra sustentável",
                "icon": "🌱",
                "criteria": {"min_assets": 1},
                "earned": total_assets >= 1,
                "reward_tokens": 50
            },
            {
                "id": "esg_collector",
                "title": "Coletor ESG",
                "description": "Acumule 10 ativos ESG",
                "icon": "📦",
                "criteria": {"min_assets": 10},
                "earned": total_assets >= 10,
                "reward_tokens": 100
            },
            {
                "id": "carbon_hero",
                "title": "Herói do Carbono",
                "description": "Evite 100kg de CO2",
                "icon": "🌍",
                "criteria": {"min_carbon": 100},
                "earned": float(total_carbon or 0) >= 100,
                "reward_tokens": 200
            },
            {
                "id": "esg_master",
                "title": "Mestre ESG",
                "description": "Acumule 1000 tokens ESG",
                "icon": "👑",
                "criteria": {"min_tokens": 1000},
                "earned": esg_tokens >= 1000,
                "reward_tokens": 500
            }
        ]

        return badges

    except Exception as e:
        logger.error(f"❌ Erro ao calcular badges: {str(e)}")
        return []


async def _get_badge_by_id(badge_id: str) -> Optional[Dict[str, Any]]:
    """Obter badge por ID"""
    badges = {
        "first_esg": {
            "id": "first_esg",
            "title": "Primeiro Passo ESG",
            "reward_tokens": 50
        },
        "esg_collector": {
            "id": "esg_collector", 
            "title": "Coletor ESG",
            "reward_tokens": 100
        },
        "carbon_hero": {
            "id": "carbon_hero",
            "title": "Herói do Carbono", 
            "reward_tokens": 200
        },
        "esg_master": {
            "id": "esg_master",
            "title": "Mestre ESG",
            "reward_tokens": 500
        }
    }
    return badges.get(badge_id)


async def _user_has_badge(user_id: str, badge_id: str) -> bool:
    """Verificar se usuário tem o badge"""
    # Mock (implementar modelo UserBadge)
    return False


async def _user_meets_badge_criteria(user_id: str, badge_id: str, db: AsyncSession) -> bool:
    """Verificar se usuário atende aos critérios do badge"""
    try:
        # Buscar métricas ESG do usuário
        user_result = await db.execute(
            select(User.esg_tokens).where(User.id == user_id)
        )
        esg_tokens = user_result.scalar() or 0

        assets_result = await db.execute(
            select(func.count(ESGAsset.id), func.sum(ESGAsset.carbon_offset_kg)).where(
                ESGAsset.user_id == user_id,
                ESGAsset.status == "active"
            )
        )
        total_assets, total_carbon = assets_result.first() or (0, 0.0)

        # Verificar critérios por badge
        if badge_id == "first_esg":
            return total_assets >= 1
        elif badge_id == "esg_collector":
            return total_assets >= 10
        elif badge_id == "carbon_hero":
            return float(total_carbon or 0) >= 100
        elif badge_id == "esg_master":
            return esg_tokens >= 1000

        return False

    except Exception as e:
        logger.error(f"❌ Erro ao verificar critérios do badge: {str(e)}")
        return False


async def _claim_badge_for_user(user_id: str, badge_id: str, reward_tokens: int):
    """Reivindicar badge para usuário"""
    # Mock (implementar modelo UserBadge e atualizar tokens)
    pass


def _calculate_period_start(period: str) -> datetime:
    """Calcular início do período"""
    now = datetime.utcnow()
    
    if period == "daily":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        days_since_monday = now.weekday()
        return (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "monthly":
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == "yearly":
        return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


async def _get_esg_leaderboard_data(start_date: datetime, limit: int, db: AsyncSession) -> List[Dict[str, Any]]:
    """Obter dados do leaderboard ESG"""
    try:
        # Buscar ranking ESG do período
        ranking_result = await db.execute(
            select(User.id, User.name, User.esg_tokens)
            .where(User.esg_tokens > 0)
            .order_by(desc(User.esg_tokens))
            .limit(limit)
        )
        
        ranking_users = ranking_result.fetchall()
        
        leaderboard = []
        for i, (user_id, name, tokens) in enumerate(ranking_users, 1):
            leaderboard.append({
                "position": i,
                "user_id": str(user_id),
                "name": name,
                "esg_tokens": tokens,
                "esg_level": _calculate_esg_level(tokens)
            })

        return leaderboard

    except Exception as e:
        logger.error(f"❌ Erro ao obter leaderboard: {str(e)}")
        return []


async def _get_user_leaderboard_position(user_id: str, start_date: datetime, db: AsyncSession) -> int:
    """Obter posição do usuário no leaderboard"""
    try:
        # Contar usuários com mais tokens ESG
        position_result = await db.execute(
            select(func.count(User.id)).where(
                User.esg_tokens > select(User.esg_tokens).where(User.id == user_id).scalar_subquery()
            )
        )
        
        return (position_result.scalar() or 0) + 1

    except Exception as e:
        logger.error(f"❌ Erro ao obter posição do leaderboard: {str(e)}")
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
