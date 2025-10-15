from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager" 
    USER = "user"
    GUEST = "guest"

class UserBase(BaseModel):
    email: str = Field(..., description="Email do usuário")
    name: str = Field(..., description="Nome do usuário")
    role: UserRole = Field(default=UserRole.USER, description="Papel do usuário")
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Senha do usuário")

class UserResponse(UserBase):
    id: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(..., description="Nome do produto")
    price: float = Field(..., gt=0, description="Preço do produto")
    description: Optional[str] = Field(None, description="Descrição do produto")
    esg_score: Optional[float] = Field(None, ge=0, le=10, description="Score ESG do produto")

class ProductCreate(ProductBase):
    store_id: str = Field(..., description="ID da loja")

class ProductResponse(ProductBase):
    id: str
    store_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    product_id: str = Field(..., description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade")
    
class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    id: str
    product: ProductResponse
    total_price: float
    
    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0, description="Valor do pagamento")
    method: str = Field(..., description="Método de pagamento")
    
class PaymentCreate(PaymentBase):
    cart_id: str = Field(..., description="ID do carrinho")

class PaymentResponse(PaymentBase):
    id: str
    status: str
    transaction_id: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


