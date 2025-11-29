"""
OAuth2 Schemas
Schemas para autenticação OAuth2
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class OAuth2LoginRequest(BaseModel):
    """Request para login OAuth2"""
    provider: str  # "google" ou "microsoft"
    redirect_uri: str
    state: Optional[str] = None
    scopes: Optional[list] = None

class OAuth2CallbackRequest(BaseModel):
    """Request para callback OAuth2"""
    code: str
    redirect_uri: str
    state: Optional[str] = None

class OAuth2UserInfo(BaseModel):
    """Informações do usuário OAuth2"""
    id: str
    email: EmailStr
    name: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    verified_email: bool = False
    provider: str

class OAuth2UserResponse(BaseModel):
    """Response OAuth2 com usuário"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict
    provider: str
    message: str

class OAuth2TokenResponse(BaseModel):
    """Response com token OAuth2"""
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str = "Bearer"
    scope: Optional[str] = None

class OAuth2ScopeRequest(BaseModel):
    """Request para validar scopes"""
    scopes: list
    provider: Optional[str] = None

class OAuth2ScopeResponse(BaseModel):
    """Response de scopes"""
    valid: bool
    requested_scopes: list
    allowed_scopes: list
    message: str

class OAuth2ConfigResponse(BaseModel):
    """Response de configuração OAuth2"""
    google_client_id: str
    microsoft_client_id: str
    default_scopes: list
    google_auth_url: str
    microsoft_auth_url: str
