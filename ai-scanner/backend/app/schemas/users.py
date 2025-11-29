"""
Users Schemas
Schemas para API de usuários
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    """Schema base para usuário"""
    email: EmailStr
    name: str
    phone: Optional[str] = None
    role: str = "user"
    is_active: bool = True

class UserCreate(UserBase):
    """Schema para criação de usuário"""
    password: str = Field(..., min_length=8, description="Senha com pelo menos 8 caracteres")
    confirm_password: str = Field(..., description="Confirmação da senha")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "name": "João Silva",
                "phone": "+5511999999999",
                "role": "user",
                "password": "senha123456",
                "confirm_password": "senha123456"
            }
        }

class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""
    name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    preferred_language: Optional[str] = None
    preferred_currency: Optional[str] = None
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "João Silva Santos",
                "phone": "+5511888888888",
                "preferred_language": "pt-BR",
                "preferred_currency": "BRL",
                "email_notifications": True,
                "push_notifications": True,
                "sms_notifications": False
            }
        }

class UserResponse(BaseModel):
    """Schema de resposta para usuário"""
    id: UUID
    email: str
    name: str
    phone: Optional[str] = None
    role: str
    is_active: bool
    preferred_language: Optional[str] = None
    preferred_currency: Optional[str] = None
    email_notifications: bool = True
    push_notifications: bool = True
    sms_notifications: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    login_count: int = 0
    total_purchases: int = 0
    total_amount_spent: float = 0.0
    loyalty_points: int = 0
    loyalty_level: str = "bronze"
    esg_score: int = 50
    esg_level: str = "neutral"
    guardpass_id: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "usuario@exemplo.com",
                "name": "João Silva",
                "phone": "+5511999999999",
                "role": "user",
                "is_active": True,
                "preferred_language": "pt-BR",
                "preferred_currency": "BRL",
                "email_notifications": True,
                "push_notifications": True,
                "sms_notifications": False,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "last_login": "2024-01-01T00:00:00Z",
                "login_count": 5,
                "total_purchases": 10,
                "total_amount_spent": 250.50,
                "loyalty_points": 100,
                "loyalty_level": "silver",
                "esg_score": 75,
                "esg_level": "good",
                "guardpass_id": "gp_123456789"
            }
        }

class UserListResponse(BaseModel):
    """Schema de resposta para lista de usuários"""
    users: List[UserResponse]
    total: int
    skip: int
    limit: int
    has_more: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "users": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "email": "usuario1@exemplo.com",
                        "name": "João Silva",
                        "role": "user",
                        "is_active": True,
                        "created_at": "2024-01-01T00:00:00Z"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 100,
                "has_more": False
            }
        }

class UserStats(BaseModel):
    """Schema para estatísticas do usuário"""
    total_purchases: int
    total_amount_spent: float
    loyalty_points: int
    loyalty_level: str
    esg_score: int
    esg_level: str
    account_age_days: int
    is_new_user: bool
    login_count: int
    last_login: Optional[datetime] = None
    average_purchase_value: float
    favorite_categories: List[str] = []
    monthly_purchases: int = 0
    monthly_amount: float = 0.0
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_purchases": 25,
                "total_amount_spent": 1250.75,
                "loyalty_points": 500,
                "loyalty_level": "gold",
                "esg_score": 85,
                "esg_level": "excellent",
                "account_age_days": 90,
                "is_new_user": False,
                "login_count": 45,
                "last_login": "2024-01-01T00:00:00Z",
                "average_purchase_value": 50.03,
                "favorite_categories": ["Alimentício", "Bebidas"],
                "monthly_purchases": 8,
                "monthly_amount": 400.25
            }
        }

class UserRoleChange(BaseModel):
    """Schema para alteração de role"""
    new_role: str = Field(..., description="Nova role do usuário")
    reason: Optional[str] = Field(None, description="Motivo da alteração")
    
    class Config:
        json_schema_extra = {
            "example": {
                "new_role": "manager",
                "reason": "Promoção para gerente de loja"
            }
        }

class UserSearchFilters(BaseModel):
    """Schema para filtros de busca de usuários"""
    search: Optional[str] = Field(None, description="Termo de busca")
    role: Optional[str] = Field(None, description="Filtrar por role")
    is_active: Optional[bool] = Field(None, description="Filtrar por status ativo")
    loyalty_level: Optional[str] = Field(None, description="Filtrar por nível de fidelidade")
    esg_level: Optional[str] = Field(None, description="Filtrar por nível ESG")
    created_after: Optional[datetime] = Field(None, description="Usuários criados após esta data")
    created_before: Optional[datetime] = Field(None, description="Usuários criados antes desta data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "search": "joão",
                "role": "user",
                "is_active": True,
                "loyalty_level": "gold",
                "esg_level": "good"
            }
        }

class UserBulkUpdate(BaseModel):
    """Schema para atualização em lote de usuários"""
    user_ids: List[UUID] = Field(..., description="IDs dos usuários para atualizar")
    updates: UserUpdate = Field(..., description="Campos para atualizar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_ids": [
                    "123e4567-e89b-12d3-a456-426614174000",
                    "123e4567-e89b-12d3-a456-426614174001"
                ],
                "updates": {
                    "role": "manager",
                    "email_notifications": True
                }
            }
        }

class UserExportRequest(BaseModel):
    """Schema para exportação de usuários"""
    format: str = Field("csv", description="Formato de exportação (csv, excel, json)")
    filters: Optional[UserSearchFilters] = Field(None, description="Filtros para exportação")
    fields: Optional[List[str]] = Field(None, description="Campos específicos para exportar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "format": "csv",
                "filters": {
                    "is_active": True,
                    "role": "user"
                },
                "fields": ["id", "email", "name", "role", "created_at"]
            }
        }
