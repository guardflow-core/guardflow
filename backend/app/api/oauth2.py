"""
OAuth2 API Endpoints
Endpoints de autenticação OAuth2 com Google e Microsoft
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from typing import Optional
from urllib.parse import urlencode

from app.database import get_db
from app.config import settings, AppMessages
from app.models.user import User
from app.schemas.auth import OAuth2LoginRequest, OAuth2CallbackRequest, OAuth2UserResponse
from app.services.oauth_service import oauth_service
from app.services.auth_service import AuthService
from app.utils.security import create_access_token

# Logger
logger = logging.getLogger("guardflow.oauth2")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Services
auth_service = AuthService()

@router.get("/google/auth")
@limiter.limit("20/minute")
async def google_auth(
    request: Request,
    redirect_uri: str,
    state: Optional[str] = None
):
    """
    Iniciar fluxo OAuth2 do Google
    """
    try:
        logger.info("🔗 Iniciando OAuth2 Google")
        
        # Gerar URL de autorização
        auth_url = await oauth_service.get_google_auth_url(
            redirect_uri=redirect_uri,
            state=state
        )
        
        # Redirecionar para Google
        return RedirectResponse(url=auth_url)
        
    except Exception as e:
        logger.error(f"❌ Erro no OAuth2 Google: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao iniciar OAuth2"
        )

@router.get("/microsoft/auth")
@limiter.limit("20/minute")
async def microsoft_auth(
    request: Request,
    redirect_uri: str,
    state: Optional[str] = None
):
    """
    Iniciar fluxo OAuth2 do Microsoft
    """
    try:
        logger.info("🔗 Iniciando OAuth2 Microsoft")
        
        # Gerar URL de autorização
        auth_url = await oauth_service.get_microsoft_auth_url(
            redirect_uri=redirect_uri,
            state=state
        )
        
        # Redirecionar para Microsoft
        return RedirectResponse(url=auth_url)
        
    except Exception as e:
        logger.error(f"❌ Erro no OAuth2 Microsoft: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao iniciar OAuth2"
        )

@router.post("/google/callback", response_model=OAuth2UserResponse)
@limiter.limit("30/minute")
async def google_callback(
    request: Request,
    callback_data: OAuth2CallbackRequest,
    db = Depends(get_db)
):
    """
    Callback OAuth2 do Google
    """
    try:
        logger.info(f"🔄 Processando callback Google: {callback_data.code[:10]}...")
        
        # Trocar código por token
        oauth_data = await oauth_service.exchange_google_code(
            code=callback_data.code,
            redirect_uri=callback_data.redirect_uri
        )
        
        user_info = oauth_data["user_info"]
        
        # Buscar ou criar usuário
        user = await auth_service.get_or_create_oauth_user(
            db=db,
            oauth_data=user_info,
            provider="google",
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        # Criar token JWT
        access_token = create_access_token(
            data={"user_id": str(user.id), "guardpass_id": user.guardpass_id}
        )
        
        logger.info(f"✅ OAuth2 Google bem-sucedido: {user.email}")
        
        return OAuth2UserResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user,
            provider="google",
            message="Login agilizado com Google! 🚀"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no callback Google: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar callback"
        )

@router.post("/microsoft/callback", response_model=OAuth2UserResponse)
@limiter.limit("30/minute")
async def microsoft_callback(
    request: Request,
    callback_data: OAuth2CallbackRequest,
    db = Depends(get_db)
):
    """
    Callback OAuth2 do Microsoft
    """
    try:
        logger.info(f"🔄 Processando callback Microsoft: {callback_data.code[:10]}...")
        
        # Trocar código por token
        oauth_data = await oauth_service.exchange_microsoft_code(
            code=callback_data.code,
            redirect_uri=callback_data.redirect_uri
        )
        
        user_info = oauth_data["user_info"]
        
        # Buscar ou criar usuário
        user = await auth_service.get_or_create_oauth_user(
            db=db,
            oauth_data=user_info,
            provider="microsoft",
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        # Criar token JWT
        access_token = create_access_token(
            data={"user_id": str(user.id), "guardpass_id": user.guardpass_id}
        )
        
        logger.info(f"✅ OAuth2 Microsoft bem-sucedido: {user.email}")
        
        return OAuth2UserResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user,
            provider="microsoft",
            message="Login agilizado com Microsoft! 🚀"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no callback Microsoft: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar callback"
        )

@router.post("/google/refresh")
@limiter.limit("20/minute")
async def refresh_google_token(
    request: Request,
    refresh_token: str
):
    """
    Renovar token do Google
    """
    try:
        logger.info("🔄 Renovando token Google")
        
        # Renovar token
        new_token = await oauth_service.refresh_google_token(refresh_token)
        
        logger.info("✅ Token Google renovado")
        
        return {
            "success": True,
            "message": "Token agilizado! ⚡",
            "data": new_token
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao renovar token Google: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao renovar token"
        )

@router.post("/microsoft/refresh")
@limiter.limit("20/minute")
async def refresh_microsoft_token(
    request: Request,
    refresh_token: str
):
    """
    Renovar token do Microsoft
    """
    try:
        logger.info("🔄 Renovando token Microsoft")
        
        # Renovar token
        new_token = await oauth_service.refresh_microsoft_token(refresh_token)
        
        logger.info("✅ Token Microsoft renovado")
        
        return {
            "success": True,
            "message": "Token agilizado! ⚡",
            "data": new_token
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao renovar token Microsoft: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao renovar token"
        )

@router.get("/scopes")
async def get_available_scopes():
    """
    Obter scopes disponíveis
    """
    try:
        scopes = {
            "google": [
                "openid",
                "profile",
                "email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email"
            ],
            "microsoft": [
                "openid",
                "profile", 
                "email",
                "User.Read"
            ],
            "default": oauth_service.default_scopes
        }
        
        return {
            "success": True,
            "message": "Scopes disponíveis! 📋",
            "data": scopes
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter scopes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter scopes"
        )

@router.post("/validate-scopes")
@limiter.limit("50/minute")
async def validate_scopes(
    request: Request,
    scopes: list
):
    """
    Validar scopes OAuth2
    """
    try:
        allowed_scopes = oauth_service.default_scopes + [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "User.Read"
        ]
        
        is_valid = oauth_service.validate_oauth_scopes(scopes, allowed_scopes)
        
        return {
            "success": True,
            "message": "Scopes validados! ✅" if is_valid else "Scopes inválidos! ❌",
            "data": {
                "valid": is_valid,
                "requested_scopes": scopes,
                "allowed_scopes": allowed_scopes
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao validar scopes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao validar scopes"
        )

# Endpoint de desenvolvimento (apenas debug)
if settings.DEBUG:
    @router.get("/debug/oauth-config")
    async def debug_oauth_config():
        """
        Debug: Configuração OAuth2 (apenas desenvolvimento)
        """
        try:
            return {
                "success": True,
                "message": "Configuração OAuth2! 🔍",
                "data": {
                    "google_client_id": oauth_service.google_client_id[:10] + "...",
                    "microsoft_client_id": oauth_service.microsoft_client_id[:10] + "...",
                    "default_scopes": oauth_service.default_scopes,
                    "google_auth_url": oauth_service.google_auth_url,
                    "microsoft_auth_url": oauth_service.microsoft_auth_url
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro na configuração: {str(e)}",
                "error": str(e)
            }
