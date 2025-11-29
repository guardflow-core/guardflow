"""
Authentication API Endpoints
Endpoints de autenticação integrados com GuardPass
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_db
from app.config import settings, AppMessages
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, UserResponse, TokenRefreshRequest
from app.services.auth_service import AuthService
from app.services.guardpass_service import GuardPassService
from app.utils.security import get_current_user, create_access_token

# Logger
logger = logging.getLogger("guardflow.auth")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Security
security = HTTPBearer()

# Services
auth_service = AuthService()
guardpass_service = GuardPassService()

@router.post("/login", response_model=LoginResponse)
@limiter.limit("10/minute")
async def login(
    request: Request,
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login com GuardPass
    Autentica usuário via GuardPass e retorna token JWT
    """
    try:
        logger.info(f"🔐 Tentativa de login: {login_data.email}")
        
        # Validar credenciais com GuardPass (simulado para MVP)
        guardpass_user = await guardpass_service.authenticate_user(
            email=login_data.email,
            password=login_data.password
        )
        
        if not guardpass_user:
            logger.warning(f"❌ Login falhou para: {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AppMessages.LOGIN_FAILED
            )
        
        # Buscar ou criar usuário local
        user = await auth_service.get_or_create_user(
            db=db,
            guardpass_data=guardpass_user,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        # Criar token de acesso
        access_token = create_access_token(
            data={"user_id": str(user.id), "guardpass_id": user.guardpass_id}
        )
        
        # Atualizar informações de login
        user.update_login_info(
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        await db.commit()
        
        logger.info(f"✅ Login bem-sucedido: {user.name} ({user.email})")
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.from_orm(user),
            message=AppMessages.LOGIN_SUCCESS
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.post("/refresh", response_model=LoginResponse)
@limiter.limit("20/minute")
async def refresh_token(
    request: Request,
    refresh_data: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Renovar token de acesso
    """
    try:
        # Validar token atual
        user = await get_current_user(refresh_data.access_token, db)
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou usuário inativo"
            )
        
        # Criar novo token
        new_access_token = create_access_token(
            data={"user_id": str(user.id), "guardpass_id": user.guardpass_id}
        )
        
        # Atualizar último acesso
        user.last_login = datetime.utcnow()
        await db.commit()
        
        logger.info(f"🔄 Token renovado: {user.email}")
        
        return LoginResponse(
            access_token=new_access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.from_orm(user),
            message="Token agilizado! ⚡"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao renovar token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Obter informações do usuário atual
    """
    try:
        logger.info(f"👤 Informações solicitadas: {current_user.email}")
        return UserResponse.from_orm(current_user)
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout do usuário
    Nota: Com JWT stateless, logout é principalmente do lado cliente
    """
    try:
        logger.info(f"👋 Logout: {current_user.email}")
        
        return {
            "success": True,
            "message": "Logout agilizado! Até a próxima! 👋",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no logout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Obter perfil completo do usuário
    """
    try:
        logger.info(f"📋 Perfil solicitado: {current_user.email}")
        
        # Atualizar ESG score do GuardPass (simulado)
        if current_user.guardpass_id:
            esg_data = await guardpass_service.get_user_esg_score(current_user.guardpass_id)
            if esg_data:
                current_user.update_esg_score(esg_data.get("score", current_user.esg_score))
        
        return UserResponse.from_orm(current_user)
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter perfil: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Atualizar perfil do usuário
    """
    try:
        logger.info(f"✏️ Atualizando perfil: {current_user.email}")
        
        # Campos permitidos para atualização
        allowed_fields = {
            "name", "phone", "preferred_language", "preferred_currency",
            "email_notifications", "push_notifications", "sms_notifications"
        }
        
        # Atualizar campos permitidos
        for field, value in profile_data.items():
            if field in allowed_fields and hasattr(current_user, field):
                setattr(current_user, field, value)
        
        current_user.updated_at = datetime.utcnow()
        await db.commit()
        
        logger.info(f"✅ Perfil atualizado: {current_user.email}")
        
        return UserResponse.from_orm(current_user)
        
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar perfil: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user)
):
    """
    Obter estatísticas do usuário
    """
    try:
        logger.info(f"📊 Estatísticas solicitadas: {current_user.email}")
        
        return {
            "success": True,
            "message": "Estatísticas agilizadas! 📊",
            "data": {
                "total_purchases": current_user.total_purchases,
                "total_amount_spent": current_user.total_amount_spent,
                "loyalty_points": current_user.loyalty_points,
                "loyalty_level": current_user.loyalty_level,
                "esg_score": current_user.esg_score,
                "esg_level": current_user.esg_level,
                "account_age_days": (datetime.utcnow() - current_user.created_at).days if current_user.created_at else 0,
                "is_new_user": current_user.is_new_user,
                "login_count": current_user.login_count,
                "last_login": current_user.last_login.isoformat() if current_user.last_login else None
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.delete("/account")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Desativar conta do usuário
    Nota: Não deletamos fisicamente por questões legais e de auditoria
    """
    try:
        logger.warning(f"🗑️ Desativação de conta solicitada: {current_user.email}")
        
        # Desativar conta
        current_user.is_active = False
        current_user.updated_at = datetime.utcnow()
        
        await db.commit()
        
        logger.info(f"✅ Conta desativada: {current_user.email}")
        
        return {
            "success": True,
            "message": "Conta desativada. Esperamos que volte a agilizar conosco! 😢",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao desativar conta: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

# Endpoint de desenvolvimento (apenas debug)
if settings.DEBUG:
    @router.get("/debug/token-info")
    async def debug_token_info(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        """
        Debug: Informações do token (apenas desenvolvimento)
        """
        try:
            from app.utils.security import decode_token
            
            payload = decode_token(credentials.credentials)
            
            return {
                "success": True,
                "message": "Token decodificado! 🔍",
                "data": {
                    "payload": payload,
                    "token_preview": credentials.credentials[:20] + "...",
                    "expires_in": payload.get("exp", 0) - datetime.utcnow().timestamp() if payload.get("exp") else None
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao decodificar token: {str(e)}",
                "error": str(e)
            }


