"""
Authentication Schemas
Schemas Pydantic para autenticação
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    """Request de login"""
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=6, description="Senha do usuário")
    remember_me: bool = Field(default=False, description="Lembrar login")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@guardpass.com",
                "password": "senha123",
                "remember_me": True
            }
        }

class TokenRefreshRequest(BaseModel):
    """Request para renovar token"""
    access_token: str = Field(..., description="Token atual para renovação")
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }

class UserResponse(BaseModel):
    """Response com dados do usuário"""
    id: str = Field(..., description="ID único do usuário")
    guardpass_id: str = Field(..., description="ID do GuardPass")
    name: str = Field(..., description="Nome do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    phone: Optional[str] = Field(None, description="Telefone do usuário")
    avatar_url: Optional[str] = Field(None, description="URL do avatar")
    
    # Preferências
    preferred_language: str = Field(default="pt-BR", description="Idioma preferido")
    preferred_currency: str = Field(default="BRL", description="Moeda preferida")
    
    # Notificações
    email_notifications: bool = Field(default=True, description="Notificações por email")
    push_notifications: bool = Field(default=True, description="Notificações push")
    sms_notifications: bool = Field(default=False, description="Notificações SMS")
    
    # ESG e gamificação
    esg_score: int = Field(..., description="Score ESG do usuário")
    esg_level: str = Field(..., description="Nível ESG")
    total_purchases: int = Field(..., description="Total de compras")
    loyalty_points: int = Field(..., description="Pontos de fidelidade")
    loyalty_level: str = Field(..., description="Nível de fidelidade")
    
    # Status
    is_active: bool = Field(..., description="Usuário ativo")
    is_verified: bool = Field(..., description="Usuário verificado")
    is_premium: bool = Field(..., description="Usuário premium")
    is_new_user: bool = Field(..., description="Usuário novo")
    
    # Timestamps
    last_login: Optional[datetime] = Field(None, description="Último login")
    created_at: Optional[datetime] = Field(None, description="Data de criação")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "guardpass_id": "gp_user_12345",
                "name": "João Silva",
                "email": "joao@guardpass.com",
                "phone": "+5511999999999",
                "avatar_url": "https://guardflow.app/avatars/joao.jpg",
                "preferred_language": "pt-BR",
                "preferred_currency": "BRL",
                "email_notifications": True,
                "push_notifications": True,
                "sms_notifications": False,
                "esg_score": 75,
                "esg_level": "Bom",
                "total_purchases": 42,
                "loyalty_points": 1250,
                "loyalty_level": "Prata",
                "is_active": True,
                "is_verified": True,
                "is_premium": False,
                "is_new_user": False,
                "last_login": "2024-01-15T10:30:00Z",
                "created_at": "2024-01-01T08:00:00Z"
            }
        }

class LoginResponse(BaseModel):
    """Response de login bem-sucedido"""
    access_token: str = Field(..., description="Token JWT de acesso")
    token_type: str = Field(default="bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")
    user: UserResponse = Field(..., description="Dados do usuário")
    message: str = Field(..., description="Mensagem de sucesso")
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 604800,
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "João Silva",
                    "email": "joao@guardpass.com",
                    "esg_score": 75
                },
                "message": "Agilizou! Bem-vindo ao GuardFlow! 🎯"
            }
        }

class UserUpdateRequest(BaseModel):
    """Request para atualizar dados do usuário"""
    name: Optional[str] = Field(None, min_length=2, max_length=255, description="Nome do usuário")
    phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]+$', description="Telefone do usuário")
    preferred_language: Optional[str] = Field(None, pattern=r'^[a-z]{2}-[A-Z]{2}$', description="Idioma (ex: pt-BR)")
    preferred_currency: Optional[str] = Field(None, pattern=r'^[A-Z]{3}$', description="Moeda (ex: BRL)")
    email_notifications: Optional[bool] = Field(None, description="Receber notificações por email")
    push_notifications: Optional[bool] = Field(None, description="Receber notificações push")
    sms_notifications: Optional[bool] = Field(None, description="Receber notificações SMS")
    
    @validator('name')
    def validate_name(cls, v):
        if v and len(v.strip()) < 2:
            raise ValueError('Nome deve ter pelo menos 2 caracteres')
        return v.strip() if v else v
    
    @validator('phone')
    def validate_phone(cls, v):
        if v:
            # Remover caracteres não numéricos para validação
            digits_only = ''.join(filter(str.isdigit, v))
            if len(digits_only) < 10 or len(digits_only) > 15:
                raise ValueError('Telefone deve ter entre 10 e 15 dígitos')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "João Silva Santos",
                "phone": "+5511999999999",
                "preferred_language": "pt-BR",
                "preferred_currency": "BRL",
                "email_notifications": True,
                "push_notifications": True,
                "sms_notifications": False
            }
        }

class PasswordChangeRequest(BaseModel):
    """Request para alterar senha"""
    current_password: str = Field(..., min_length=6, description="Senha atual")
    new_password: str = Field(..., min_length=8, description="Nova senha")
    confirm_password: str = Field(..., min_length=8, description="Confirmação da nova senha")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Senhas não conferem')
        return v
    
    @validator('new_password')
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Nova senha deve ter pelo menos 8 caracteres')
        
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError('Nova senha deve conter ao menos: 1 maiúscula, 1 minúscula e 1 número')
        
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "current_password": "senha123",
                "new_password": "NovaSenha123!",
                "confirm_password": "NovaSenha123!"
            }
        }

class UserStatsResponse(BaseModel):
    """Response com estatísticas do usuário"""
    total_purchases: int = Field(..., description="Total de compras realizadas")
    total_amount_spent: str = Field(..., description="Valor total gasto")
    loyalty_points: int = Field(..., description="Pontos de fidelidade")
    loyalty_level: str = Field(..., description="Nível de fidelidade")
    esg_score: int = Field(..., description="Score ESG")
    esg_level: str = Field(..., description="Nível ESG")
    account_age_days: int = Field(..., description="Idade da conta em dias")
    is_new_user: bool = Field(..., description="É usuário novo")
    login_count: int = Field(..., description="Número de logins")
    last_login: Optional[datetime] = Field(None, description="Último login")
    
    # Estatísticas de sustentabilidade
    carbon_footprint_saved_kg: Optional[float] = Field(None, description="CO2 economizado em kg")
    organic_purchases: Optional[int] = Field(None, description="Compras de produtos orgânicos")
    local_purchases: Optional[int] = Field(None, description="Compras de produtos locais")
    
    class Config:
        schema_extra = {
            "example": {
                "total_purchases": 42,
                "total_amount_spent": "1250.75",
                "loyalty_points": 1250,
                "loyalty_level": "Prata",
                "esg_score": 75,
                "esg_level": "Bom",
                "account_age_days": 45,
                "is_new_user": False,
                "login_count": 128,
                "last_login": "2024-01-15T10:30:00Z",
                "carbon_footprint_saved_kg": 12.5,
                "organic_purchases": 15,
                "local_purchases": 8
            }
        }


