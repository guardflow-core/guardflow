"""
Schemas de Carrinho para GuardFlow
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CartItemBase(BaseModel):
    """Base para item do carrinho"""
    product_id: str = Field(..., description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade")
    price: float = Field(..., gt=0, description="Preço unitário")


class AddItemRequest(CartItemBase):
    """Request para adicionar item ao carrinho"""
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "prod_123",
                "quantity": 2,
                "price": 12.99
            }
        }


class UpdateItemRequest(BaseModel):
    """Request para atualizar item do carrinho"""
    quantity: int = Field(..., gt=0, description="Nova quantidade")
    
    class Config:
        json_schema_extra = {
            "example": {
                "quantity": 3
            }
        }


class CartItemResponse(CartItemBase):
    """Response de item do carrinho"""
    id: str
    product_name: str
    product_image: Optional[str] = None
    subtotal: float = Field(..., description="Subtotal do item")
    esg_score: Optional[float] = Field(None, description="Score ESG do produto")
    discount_amount: Optional[float] = Field(0, description="Desconto aplicado")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "item_123",
                "product_id": "prod_123",
                "product_name": "Arroz Integral 1kg",
                "quantity": 2,
                "price": 12.99,
                "subtotal": 25.98,
                "esg_score": 85.5,
                "discount_amount": 0
            }
        }


class CartResponse(BaseModel):
    """Response do carrinho completo"""
    id: str
    user_id: str
    items: List[CartItemResponse] = []
    items_count: int = Field(..., description="Total de itens")
    subtotal: float = Field(..., description="Subtotal sem descontos")
    discount_total: float = Field(0, description="Total de descontos")
    total: float = Field(..., description="Total final")
    average_esg_score: Optional[float] = Field(None, description="Score ESG médio")
    gst_tokens_earned: Optional[float] = Field(None, description="GST tokens ganhos")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "cart_123",
                "user_id": "user_123",
                "items": [],
                "items_count": 5,
                "subtotal": 150.00,
                "discount_total": 10.00,
                "total": 140.00,
                "average_esg_score": 82.3,
                "gst_tokens_earned": 14.0,
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:30:00"
            }
        }


class CheckoutRequest(BaseModel):
    """Request para checkout"""
    payment_method: str = Field(..., description="Método de pagamento (pix, credit_card, guardpass)")
    store_id: str = Field(..., description="ID da loja")
    use_loyalty_points: bool = Field(False, description="Usar pontos de fidelidade")
    loyalty_points_amount: Optional[float] = Field(None, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "payment_method": "pix",
                "store_id": "store_123",
                "use_loyalty_points": False
            }
        }


class CheckoutResponse(BaseModel):
    """Response do checkout"""
    transaction_id: str
    status: str = Field(..., description="Status da transação")
    payment_url: Optional[str] = Field(None, description="URL para pagamento (PIX)")
    qr_code: Optional[str] = Field(None, description="QR Code PIX")
    total_paid: float
    loyalty_points_earned: float
    gst_tokens_earned: float
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "trans_123",
                "status": "pending_payment",
                "payment_url": "https://pix.guardflow.com/...",
                "qr_code": "00020126...",
                "total_paid": 140.00,
                "loyalty_points_earned": 140,
                "gst_tokens_earned": 14.0,
                "message": "Checkout realizado! Aguardando pagamento."
            }
        }
