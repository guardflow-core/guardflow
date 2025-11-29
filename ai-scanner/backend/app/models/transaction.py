"""
Transaction Models - Modelos de transação e eventos
"""
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Float, Text, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.database import DATABASE_URL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from app.database import Base

class Transaction(Base):
    """
    Modelo de transação/pagamento
    """
    __tablename__ = "transactions"

    # Identificação
    id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Relacionamentos
    cart_id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), ForeignKey("carts.id"), nullable=False, index=True)
    user_id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    store_id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), ForeignKey("stores.id"), nullable=False, index=True)
    
    # Dados financeiros
    amount = Column(String(20), nullable=False)  # Valor total
    discount_amount = Column(String(20), default="0.00")
    tax_amount = Column(String(20), default="0.00")
    final_amount = Column(String(20), nullable=False)  # Valor final pago
    
    # Método de pagamento
    payment_method = Column(String(50), nullable=False, index=True)  # pix, credit_card, debit_card, guardpass_tokens
    
    # Integração com gateway de pagamento
    payment_id = Column(String(255), nullable=True, index=True)  # ID do Mercado Pago, etc.
    payment_gateway = Column(String(50), default="mercado_pago")
    
    # Status da transação
    status = Column(String(20), default="pending", index=True)  # pending, processing, completed, failed, cancelled, refunded
    
    # PIX específico
    pix_qr_code = Column(Text, nullable=True)
    pix_code = Column(Text, nullable=True)
    pix_expiration = Column(DateTime(timezone=True), nullable=True)
    
    # Dados do cartão (apenas últimos 4 dígitos)
    card_last_four = Column(String(4), nullable=True)
    card_brand = Column(String(20), nullable=True)  # visa, mastercard, etc.
    
    # Dados da transação
    transaction_data = Column(JSON, nullable=True)  # Dados completos da resposta do gateway
    
    # Informações de ESG
    esg_score = Column(Integer, default=50)
    carbon_footprint_kg = Column(Float, default=0.0)
    sustainability_impact = Column(JSON, nullable=True)
    
    # Tokens GuardPass (se aplicável)
    gst_tokens_earned = Column(Integer, default=0)
    gst_tokens_used = Column(Integer, default=0)
    
    # Informações de entrega/retirada
    delivery_method = Column(String(50), default="pickup")  # pickup, delivery
    delivery_address = Column(Text, nullable=True)
    delivery_fee = Column(String(20), default="0.00")
    
    # Metadados
    receipt_url = Column(Text, nullable=True)
    invoice_number = Column(String(100), nullable=True, unique=True)
    fiscal_note_key = Column(String(44), nullable=True)  # Chave da NFe
    
    # Informações do dispositivo/sessão
    device_info = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    refunded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos ORM
    cart = relationship("Cart", foreign_keys=[cart_id])
    user = relationship("User", foreign_keys=[user_id])
    store = relationship("Store", foreign_keys=[store_id])
    
    def __repr__(self):
        return f"<Transaction {self.id} - {self.status} - R$ {self.final_amount}>"
    
    def to_dict(self, include_sensitive: bool = False):
        """Converter para dicionário"""
        data = {
            "id": str(self.id),
            "cart_id": str(self.cart_id),
            "user_id": str(self.user_id),
            "store_id": str(self.store_id),
            "amount": self.amount,
            "discount_amount": self.discount_amount,
            "final_amount": self.final_amount,
            "payment_method": self.payment_method,
            "status": self.status,
            "esg_score": self.esg_score,
            "carbon_footprint_kg": self.carbon_footprint_kg,
            "gst_tokens_earned": self.gst_tokens_earned,
            "gst_tokens_used": self.gst_tokens_used,
            "delivery_method": self.delivery_method,
            "invoice_number": self.invoice_number,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None
        }
        
        if include_sensitive:
            data.update({
                "payment_id": self.payment_id,
                "pix_qr_code": self.pix_qr_code,
                "pix_code": self.pix_code,
                "card_last_four": self.card_last_four,
                "card_brand": self.card_brand,
                "transaction_data": self.transaction_data
            })
        
        return data
    
    def mark_as_paid(self, payment_data: Dict[str, Any] = None):
        """Marcar transação como paga"""
        self.status = "completed"
        self.paid_at = datetime.utcnow()
        
        if payment_data:
            self.transaction_data = payment_data
        
        # Calcular tokens GST (1 token para cada R$ 10 gastos)
        amount_float = self.get_final_amount_float()
        self.gst_tokens_earned = int(amount_float // 10)
        
        self.updated_at = datetime.utcnow()
    
    def mark_as_failed(self, error_message: str = None):
        """Marcar transação como falhou"""
        self.status = "failed"
        
        if error_message and self.transaction_data:
            self.transaction_data["error_message"] = error_message
        elif error_message:
            self.transaction_data = {"error_message": error_message}
        
        self.updated_at = datetime.utcnow()
    
    def cancel(self, reason: str = None):
        """Cancelar transação"""
        self.status = "cancelled"
        self.cancelled_at = datetime.utcnow()
        
        if reason and self.transaction_data:
            self.transaction_data["cancellation_reason"] = reason
        elif reason:
            self.transaction_data = {"cancellation_reason": reason}
        
        self.updated_at = datetime.utcnow()
    
    def refund(self, refund_amount: float = None, reason: str = None):
        """Processar reembolso"""
        self.status = "refunded"
        self.refunded_at = datetime.utcnow()
        
        refund_data = {
            "refund_amount": refund_amount or self.get_final_amount_float(),
            "refund_reason": reason,
            "refund_date": datetime.utcnow().isoformat()
        }
        
        if self.transaction_data:
            self.transaction_data["refund_data"] = refund_data
        else:
            self.transaction_data = {"refund_data": refund_data}
        
        self.updated_at = datetime.utcnow()
    
    def generate_invoice_number(self):
        """Gerar número da nota fiscal"""
        if not self.invoice_number:
            # Formato: GF + YYYYMMDD + sequencial de 6 dígitos
            date_part = datetime.now().strftime("%Y%m%d")
            # Em produção, implementar sequencial baseado no banco
            sequential = str(self.created_at.microsecond).zfill(6)[-6:]
            self.invoice_number = f"GF{date_part}{sequential}"
    
    def calculate_esg_impact(self):
        """Calcular impacto ESG da transação"""
        if not self.cart or not self.cart.items:
            return
        
        total_esg = 0
        total_carbon = 0.0
        item_count = 0
        
        for item in self.cart.items:
            if item.product:
                total_esg += item.product.esg_score * item.quantity
                if item.product.carbon_footprint_kg:
                    total_carbon += item.product.carbon_footprint_kg * item.quantity
                item_count += item.quantity
        
        if item_count > 0:
            self.esg_score = total_esg // item_count
            self.carbon_footprint_kg = total_carbon
            
            # Criar relatório de impacto
            self.sustainability_impact = {
                "total_items": item_count,
                "average_esg_score": self.esg_score,
                "total_carbon_footprint": total_carbon,
                "organic_items": sum(1 for item in self.cart.items if item.product and item.product.is_organic),
                "local_items": sum(1 for item in self.cart.items if item.product and item.product.is_local_product),
                "recyclable_packaging": sum(1 for item in self.cart.items if item.product and item.product.is_recyclable)
            }
    
    def get_amount_float(self) -> float:
        """Obter valor como float"""
        try:
            return float(self.amount)
        except (ValueError, TypeError):
            return 0.0
    
    def get_final_amount_float(self) -> float:
        """Obter valor final como float"""
        try:
            return float(self.final_amount)
        except (ValueError, TypeError):
            return 0.0
    
    def get_discount_amount_float(self) -> float:
        """Obter desconto como float"""
        try:
            return float(self.discount_amount)
        except (ValueError, TypeError):
            return 0.0
    
    @property
    def is_paid(self) -> bool:
        """Verificar se transação foi paga"""
        return self.status == "completed" and self.paid_at is not None
    
    @property
    def is_pending(self) -> bool:
        """Verificar se transação está pendente"""
        return self.status in ["pending", "processing"]
    
    @property
    def payment_method_display(self) -> str:
        """Nome amigável do método de pagamento"""
        methods = {
            "pix": "PIX",
            "credit_card": "Cartão de Crédito",
            "debit_card": "Cartão de Débito",
            "guardpass_tokens": "Tokens GuardPass"
        }
        return methods.get(self.payment_method, self.payment_method.title())
    
    @property
    def esg_level(self) -> str:
        """Nível ESG da transação"""
        if self.esg_score >= 80:
            return "Excelente"
        elif self.esg_score >= 60:
            return "Bom"
        elif self.esg_score >= 40:
            return "Regular"
        else:
            return "Iniciante"


class ScanEvent(Base):
    """
    Modelo para eventos de escaneamento (analytics)
    """
    __tablename__ = "scan_events"

    # Identificação
    id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Relacionamentos
    user_id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    store_id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), ForeignKey("stores.id"), nullable=True, index=True)
    product_id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), ForeignKey("products.id"), nullable=True, index=True)
    
    # Dados do escaneamento
    barcode_scanned = Column(String(50), nullable=True, index=True)
    confidence_score = Column(Float, nullable=True)
    scan_duration_ms = Column(Integer, nullable=True)  # Duração em millisegundos
    
    # Resultado do escaneamento
    successful = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    recognition_method = Column(String(50), nullable=True)  # barcode, ocr, image_recognition
    
    # Dados da imagem (se aplicável)
    image_width = Column(Integer, nullable=True)
    image_height = Column(Integer, nullable=True)
    image_size_bytes = Column(Integer, nullable=True)
    
    # Contexto do escaneamento
    scan_context = Column(String(50), nullable=True)  # shopping, inventory, price_check
    device_type = Column(String(50), nullable=True)   # mobile, tablet, scanner
    
    # Ação tomada após escaneamento
    action_taken = Column(String(50), nullable=True)  # added_to_cart, price_checked, ignored
    
    # Dados de localização (se disponível)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Metadados técnicos
    app_version = Column(String(20), nullable=True)
    os_version = Column(String(50), nullable=True)
    device_model = Column(String(100), nullable=True)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relacionamentos ORM
    user = relationship("User", foreign_keys=[user_id])
    store = relationship("Store", foreign_keys=[store_id])
    product = relationship("Product", foreign_keys=[product_id])
    
    def __repr__(self):
        return f"<ScanEvent {self.barcode_scanned} - {self.successful} - {self.confidence_score}>"
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "store_id": str(self.store_id) if self.store_id else None,
            "product_id": str(self.product_id) if self.product_id else None,
            "barcode_scanned": self.barcode_scanned,
            "confidence_score": self.confidence_score,
            "scan_duration_ms": self.scan_duration_ms,
            "successful": self.successful,
            "error_message": self.error_message,
            "recognition_method": self.recognition_method,
            "action_taken": self.action_taken,
            "device_type": self.device_type,
            "app_version": self.app_version,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def create_scan_event(
        cls,
        barcode: str = None,
        user_id: str = None,
        store_id: str = None,
        product_id: str = None,
        confidence: float = None,
        duration_ms: int = None,
        successful: bool = True,
        error_message: str = None,
        recognition_method: str = "barcode",
        action_taken: str = None,
        device_type: str = "mobile",
        app_version: str = None
    ):
        """Factory method para criar evento de escaneamento"""
        return cls(
            barcode_scanned=barcode,
            user_id=user_id,
            store_id=store_id,
            product_id=product_id,
            confidence_score=confidence,
            scan_duration_ms=duration_ms,
            successful=successful,
            error_message=error_message,
            recognition_method=recognition_method,
            action_taken=action_taken,
            device_type=device_type,
            app_version=app_version
        )
    
    @property
    def confidence_level(self) -> str:
        """Nível de confiança do reconhecimento"""
        if not self.confidence_score:
            return "Desconhecido"
        
        if self.confidence_score >= 0.9:
            return "Muito Alto"
        elif self.confidence_score >= 0.7:
            return "Alto"
        elif self.confidence_score >= 0.5:
            return "Médio"
        else:
            return "Baixo"
    
    @property
    def scan_duration_seconds(self) -> Optional[float]:
        """Duração do escaneamento em segundos"""
        if self.scan_duration_ms:
            return self.scan_duration_ms / 1000.0
        return None
