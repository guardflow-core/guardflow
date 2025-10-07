"""
Schemas de Pagamento para GuardFlow
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class PaymentMethod(str, Enum):
    """Métodos de pagamento suportados"""
    PIX = "pix"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    GUARDPASS = "guardpass"
    GST_TOKEN = "gst_token"


class PaymentStatus(str, Enum):
    """Status de pagamento"""
    PENDING = "pending"
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentRequest(BaseModel):
    """Request para processar pagamento"""
    amount: float = Field(..., gt=0, description="Valor total")
    method: PaymentMethod = Field(..., description="Método de pagamento")
    cart_id: str = Field(..., description="ID do carrinho")
    store_id: str = Field(..., description="ID da loja")
    
    # Dados específicos por método
    card_token: Optional[str] = Field(None, description="Token do cartão (para cartões)")
    guardpass_token: Optional[str] = Field(None, description="Token GuardPass")
    gst_amount: Optional[float] = Field(None, description="Quantidade de GST tokens")
    
    # Descontos e cupons
    discount_code: Optional[str] = Field(None, description="Código de desconto")
    loyalty_points_used: Optional[float] = Field(None, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "amount": 150.00,
                "method": "pix",
                "cart_id": "cart_123",
                "store_id": "store_123"
            }
        }


class PaymentResponse(BaseModel):
    """Response de pagamento"""
    id: str
    transaction_id: str
    status: PaymentStatus
    amount: float
    method: PaymentMethod
    
    # PIX específico
    pix_qr_code: Optional[str] = Field(None, description="QR Code PIX")
    pix_copy_paste: Optional[str] = Field(None, description="PIX copia e cola")
    pix_expiration: Optional[datetime] = Field(None, description="Expiração do PIX")
    
    # Cartão específico
    card_last_digits: Optional[str] = Field(None, description="Últimos 4 dígitos")
    card_brand: Optional[str] = Field(None, description="Bandeira do cartão")
    installments: Optional[int] = Field(None, description="Parcelas")
    
    # Recompensas
    loyalty_points_earned: float = Field(0, description="Pontos ganhos")
    gst_tokens_earned: float = Field(0, description="GST tokens ganhos")
    cashback_amount: Optional[float] = Field(None, description="Valor de cashback")
    
    # Timestamps
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "pay_123",
                "transaction_id": "trans_123",
                "status": "approved",
                "amount": 150.00,
                "method": "pix",
                "pix_qr_code": "00020126...",
                "loyalty_points_earned": 150,
                "gst_tokens_earned": 15.0,
                "created_at": "2024-01-01T10:00:00"
            }
        }


class PIXResponse(BaseModel):
    """Response específico para pagamento PIX"""
    qr_code: str = Field(..., description="QR Code para pagamento")
    qr_code_base64: str = Field(..., description="QR Code em base64")
    copy_paste: str = Field(..., description="Código PIX copia e cola")
    expiration: datetime = Field(..., description="Expiração do PIX")
    amount: float = Field(..., description="Valor")
    
    class Config:
        json_schema_extra = {
            "example": {
                "qr_code": "00020126580014br.gov.bcb.pix...",
                "qr_code_base64": "data:image/png;base64,...",
                "copy_paste": "00020126580014br.gov.bcb.pix...",
                "expiration": "2024-01-01T11:00:00",
                "amount": 150.00
            }
        }


class RefundRequest(BaseModel):
    """Request para reembolso"""
    transaction_id: str = Field(..., description="ID da transação")
    amount: Optional[float] = Field(None, gt=0, description="Valor parcial (se não informado, total)")
    reason: str = Field(..., description="Motivo do reembolso")
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "trans_123",
                "reason": "Produto com defeito"
            }
        }


class RefundResponse(BaseModel):
    """Response de reembolso"""
    id: str
    original_transaction_id: str
    status: str
    amount: float
    reason: str
    processed_at: Optional[datetime]
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "refund_123",
                "original_transaction_id": "trans_123",
                "status": "approved",
                "amount": 150.00,
                "reason": "Produto com defeito",
                "processed_at": "2024-01-01T12:00:00"
            }
        }


class TransactionHistoryResponse(BaseModel):
    """Response de histórico de transações"""
    transactions: List[PaymentResponse]
    total_count: int
    total_amount: float
    period_start: datetime
    period_end: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "transactions": [],
                "total_count": 10,
                "total_amount": 1500.00,
                "period_start": "2024-01-01T00:00:00",
                "period_end": "2024-01-31T23:59:59"
            }
        }
