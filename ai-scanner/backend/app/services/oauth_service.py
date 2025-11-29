"""
OAuth2 Service - Integração com Google e Microsoft
Serviço de autenticação OAuth2 para GuardFlow SaaS
"""
import httpx
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.config import settings

logger = logging.getLogger("guardflow.oauth")

class OAuth2Service:
    """Serviço OAuth2 para integração com Google e Microsoft"""
    
    def __init__(self):
        self.google_client_id = settings.GOOGLE_CLIENT_ID
        self.google_client_secret = settings.GOOGLE_CLIENT_SECRET
        self.microsoft_client_id = settings.MICROSOFT_CLIENT_ID
        self.microsoft_client_secret = settings.MICROSOFT_CLIENT_SECRET
        
        # URLs OAuth2
        self.google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.google_token_url = "https://oauth2.googleapis.com/token"
        self.google_user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        
        self.microsoft_auth_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
        self.microsoft_token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        self.microsoft_user_info_url = "https://graph.microsoft.com/v1.0/me"
        
        # Scopes padrão
        self.default_scopes = [
            "openid",
            "profile", 
            "email"
        ]
    
    async def get_google_auth_url(self, redirect_uri: str, state: Optional[str] = None) -> str:
        """
        Gerar URL de autorização do Google
        """
        try:
            params = {
                "client_id": self.google_client_id,
                "redirect_uri": redirect_uri,
                "scope": " ".join(self.default_scopes),
                "response_type": "code",
                "access_type": "offline",
                "prompt": "consent"
            }
            
            if state:
                params["state"] = state
                
            # Construir URL
            from urllib.parse import urlencode
            auth_url = f"{self.google_auth_url}?{urlencode(params)}"
            
            logger.info(f"🔗 URL de autorização Google gerada")
            return auth_url
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar URL Google: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar URL de autorização"
            )
    
    async def get_microsoft_auth_url(self, redirect_uri: str, state: Optional[str] = None) -> str:
        """
        Gerar URL de autorização do Microsoft
        """
        try:
            params = {
                "client_id": self.microsoft_client_id,
                "redirect_uri": redirect_uri,
                "scope": " ".join(self.default_scopes),
                "response_type": "code",
                "response_mode": "query"
            }
            
            if state:
                params["state"] = state
                
            # Construir URL
            from urllib.parse import urlencode
            auth_url = f"{self.microsoft_auth_url}?{urlencode(params)}"
            
            logger.info(f"🔗 URL de autorização Microsoft gerada")
            return auth_url
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar URL Microsoft: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar URL de autorização"
            )
    
    async def exchange_google_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        Trocar código de autorização por token do Google
        """
        try:
            async with httpx.AsyncClient() as client:
                # Solicitar token
                token_data = {
                    "client_id": self.google_client_id,
                    "client_secret": self.google_client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri
                }
                
                response = await client.post(
                    self.google_token_url,
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Erro ao trocar código Google: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Erro ao trocar código de autorização"
                    )
                
                token_info = response.json()
                
                # Obter informações do usuário
                user_info = await self.get_google_user_info(token_info["access_token"])
                
                return {
                    "access_token": token_info["access_token"],
                    "refresh_token": token_info.get("refresh_token"),
                    "expires_in": token_info.get("expires_in"),
                    "token_type": token_info.get("token_type", "Bearer"),
                    "user_info": user_info
                }
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao trocar código Google: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao processar autorização"
            )
    
    async def exchange_microsoft_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        Trocar código de autorização por token do Microsoft
        """
        try:
            async with httpx.AsyncClient() as client:
                # Solicitar token
                token_data = {
                    "client_id": self.microsoft_client_id,
                    "client_secret": self.microsoft_client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri
                }
                
                response = await client.post(
                    self.microsoft_token_url,
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Erro ao trocar código Microsoft: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Erro ao trocar código de autorização"
                    )
                
                token_info = response.json()
                
                # Obter informações do usuário
                user_info = await self.get_microsoft_user_info(token_info["access_token"])
                
                return {
                    "access_token": token_info["access_token"],
                    "refresh_token": token_info.get("refresh_token"),
                    "expires_in": token_info.get("expires_in"),
                    "token_type": token_info.get("token_type", "Bearer"),
                    "user_info": user_info
                }
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao trocar código Microsoft: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao processar autorização"
            )
    
    async def get_google_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Obter informações do usuário do Google
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.google_user_info_url,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Erro ao obter informações do usuário"
                    )
                
                user_data = response.json()
                
                return {
                    "id": user_data.get("id"),
                    "email": user_data.get("email"),
                    "name": user_data.get("name"),
                    "given_name": user_data.get("given_name"),
                    "family_name": user_data.get("family_name"),
                    "picture": user_data.get("picture"),
                    "verified_email": user_data.get("verified_email", False),
                    "provider": "google"
                }
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao obter info usuário Google: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao obter informações do usuário"
            )
    
    async def get_microsoft_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Obter informações do usuário do Microsoft
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.microsoft_user_info_url,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Erro ao obter informações do usuário"
                    )
                
                user_data = response.json()
                
                return {
                    "id": user_data.get("id"),
                    "email": user_data.get("mail") or user_data.get("userPrincipalName"),
                    "name": user_data.get("displayName"),
                    "given_name": user_data.get("givenName"),
                    "family_name": user_data.get("surname"),
                    "picture": None,  # Microsoft não fornece foto por padrão
                    "verified_email": True,  # Microsoft sempre verifica
                    "provider": "microsoft"
                }
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao obter info usuário Microsoft: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao obter informações do usuário"
            )
    
    async def refresh_google_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Renovar token do Google
        """
        try:
            async with httpx.AsyncClient() as client:
                token_data = {
                    "client_id": self.google_client_id,
                    "client_secret": self.google_client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }
                
                response = await client.post(
                    self.google_token_url,
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Erro ao renovar token"
                    )
                
                return response.json()
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao renovar token Google: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao renovar token"
            )
    
    async def refresh_microsoft_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Renovar token do Microsoft
        """
        try:
            async with httpx.AsyncClient() as client:
                token_data = {
                    "client_id": self.microsoft_client_id,
                    "client_secret": self.microsoft_client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }
                
                response = await client.post(
                    self.microsoft_token_url,
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Erro ao renovar token"
                    )
                
                return response.json()
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao renovar token Microsoft: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao renovar token"
            )
    
    def validate_oauth_scopes(self, requested_scopes: list, allowed_scopes: list) -> bool:
        """
        Validar scopes OAuth2
        """
        try:
            for scope in requested_scopes:
                if scope not in allowed_scopes:
                    logger.warning(f"⚠️ Scope não permitido: {scope}")
                    return False
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao validar scopes: {str(e)}")
            return False

# Instância global do serviço
oauth_service = OAuth2Service()
