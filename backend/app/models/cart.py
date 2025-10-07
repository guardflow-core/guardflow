"""
Cart Models - Modelos de carrinho de compras
"""
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.database import DATABASE_URL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from typing import List, Dict, Any
from datetime import datetime, timedelta

from app.database import Base

class Cart(Base):
    """
    Modelo de carrinho de compras
    """
    __tablename__ = "carts"

    # Identificação
    id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Relacionamentos
    user_id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    store_id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), ForeignKey("stores.id"), nullable=False, index=True)
    
    # Status do carrinho
    status = Column(String(20), default="active", index=True)  # active, checkout, completed, abandoned
    
    # Totais
    total_items = Column(Integer, default=0)
    total_amount = Column(String(20), default="0.00")
    discount_amount = Column(String(20), default="0.00")
    tax_amount = Column(String(20), default="0.00")
    final_amount = Column(String(20), default="0.00")
    
    # ESG Score do carrinho
    esg_score = Column(Integer, default=50)
    carbon_footprint_kg = Column(Float, default=0.0)
    
    # Configurações
    checkout_timeout_minutes = Column(Integer, default=30)
    
    # Metadados de sessão
    session_id = Column(String(255), nullable=True, index=True)
    device_info = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    checkout_started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos ORM
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    user = relationship("User", foreign_keys=[user_id])
    store = relationship("Store", foreign_keys=[store_id])
    
    def __repr__(self):
        return f"<Cart {self.id} - {self.status} - {self.total_items} items>"
    
    def to_dict(self, include_items: bool = True):
        """Converter para dicionário"""
        data = {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "store_id": str(self.store_id),
            "status": self.status,
            "total_items": self.total_items,
            "total_amount": self.total_amount,
            "discount_amount": self.discount_amount,
            "final_amount": self.final_amount,
            "esg_score": self.esg_score,
            "carbon_footprint_kg": self.carbon_footprint_kg,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }
        
        if include_items and self.items:
            data["items"] = [item.to_dict() for item in self.items]
        
        return data
    
    def add_item(self, product_id: str, quantity: int = 1, unit_price: float = 0.0):
        """Adicionar item ao carrinho"""
        # Verificar se item já existe
        existing_item = None
        for item in self.items:
            if str(item.product_id) == product_id:
                existing_item = item
                break
        
        if existing_item:
            # Atualizar quantidade
            existing_item.quantity += quantity
            existing_item.total_price = str(existing_item.quantity * existing_item.get_unit_price_float())
        else:
            # Criar novo item
            new_item = CartItem(
                cart_id=self.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=str(unit_price),
                total_price=str(quantity * unit_price)
            )
            self.items.append(new_item)
        
        # Recalcular totais
        self.recalculate_totals()
        self.updated_at = datetime.utcnow()
    
    def remove_item(self, product_id: str, quantity: int = None):
        """Remover item do carrinho"""
        item_to_remove = None
        for item in self.items:
            if str(item.product_id) == product_id:
                item_to_remove = item
                break
        
        if item_to_remove:
            if quantity is None or quantity >= item_to_remove.quantity:
                # Remover item completamente
                self.items.remove(item_to_remove)
            else:
                # Reduzir quantidade
                item_to_remove.quantity -= quantity
                item_to_remove.total_price = str(
                    item_to_remove.quantity * item_to_remove.get_unit_price_float()
                )
            
            # Recalcular totais
            self.recalculate_totals()
            self.updated_at = datetime.utcnow()
            return True
        
        return False
    
    def clear(self):
        """Limpar carrinho"""
        self.items.clear()
        self.recalculate_totals()
        self.updated_at = datetime.utcnow()
    
    def recalculate_totals(self):
        """Recalcular totais do carrinho"""
        self.total_items = len(self.items)
        total = 0.0
        total_carbon = 0.0
        total_esg = 0
        
        for item in self.items:
            total += item.get_total_price_float()
            # Aqui você pode adicionar lógica para calcular carbono e ESG
            # baseado nos produtos
        
        self.total_amount = str(round(total, 2))
        
        # Calcular desconto (implementar lógica de desconto aqui)
        discount = 0.0
        self.discount_amount = str(round(discount, 2))
        
        # Calcular valor final
        final = total - discount
        self.final_amount = str(round(final, 2))
        
        # Atualizar ESG score médio
        if self.items:
            self.esg_score = total_esg // len(self.items) if total_esg > 0 else 50
        
        self.carbon_footprint_kg = total_carbon
    
    def start_checkout(self):
        """Iniciar processo de checkout"""
        self.status = "checkout"
        self.checkout_started_at = datetime.utcnow()
        
        # Definir expiração do checkout
        self.expires_at = datetime.utcnow() + timedelta(minutes=self.checkout_timeout_minutes)
        self.updated_at = datetime.utcnow()
    
    def complete_checkout(self):
        """Completar checkout"""
        self.status = "completed"
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def abandon(self):
        """Marcar carrinho como abandonado"""
        self.status = "abandoned"
        self.updated_at = datetime.utcnow()
    
    def is_expired(self) -> bool:
        """Verificar se carrinho está expirado"""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    def get_total_amount_float(self) -> float:
        """Obter valor total como float"""
        try:
            return float(self.total_amount)
        except (ValueError, TypeError):
            return 0.0
    
    def get_final_amount_float(self) -> float:
        """Obter valor final como float"""
        try:
            return float(self.final_amount)
        except (ValueError, TypeError):
            return 0.0
    
    @property
    def is_empty(self) -> bool:
        """Verificar se carrinho está vazio"""
        return self.total_items == 0
    
    @property
    def can_checkout(self) -> bool:
        """Verificar se pode fazer checkout"""
        return (
            not self.is_empty and 
            self.status == "active" and 
            not self.is_expired()
        )
    
    @property
    def esg_level(self) -> str:
        """Nível ESG do carrinho"""
        if self.esg_score >= 80:
            return "Excelente"
        elif self.esg_score >= 60:
            return "Bom"
        elif self.esg_score >= 40:
            return "Regular"
        else:
            return "Iniciante"


class CartItem(Base):
    """
    Modelo de item do carrinho
    """
    __tablename__ = "cart_items"

    # Identificação
    id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Relacionamentos
    cart_id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), ForeignKey("carts.id"), nullable=False, index=True)
    product_id = Column(String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, index=True)
    
    # Dados do item
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(String(20), nullable=False)
    total_price = Column(String(20), nullable=False)
    
    # Preço no momento da adição (para histórico)
    price_at_addition = Column(String(20), nullable=True)
    
    # Metadados
    added_via = Column(String(50), default="scanner")  # scanner, search, recommendation
    scan_confidence = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relacionamentos ORM
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", foreign_keys=[product_id])
    
    def __repr__(self):
        return f"<CartItem {self.product_id} x{self.quantity} = {self.total_price}>"
    
    def to_dict(self, include_product: bool = True):
        """Converter para dicionário"""
        data = {
            "id": str(self.id),
            "cart_id": str(self.cart_id),
            "product_id": str(self.product_id),
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "added_via": self.added_via,
            "scan_confidence": self.scan_confidence,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_product and self.product:
            data["product"] = self.product.to_dict()
        
        return data
    
    def update_quantity(self, new_quantity: int):
        """Atualizar quantidade do item"""
        if new_quantity <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        self.quantity = new_quantity
        self.total_price = str(new_quantity * self.get_unit_price_float())
        self.updated_at = datetime.utcnow()
    
    def get_unit_price_float(self) -> float:
        """Obter preço unitário como float"""
        try:
            return float(self.unit_price)
        except (ValueError, TypeError):
            return 0.0
    
    def get_total_price_float(self) -> float:
        """Obter preço total como float"""
        try:
            return float(self.total_price)
        except (ValueError, TypeError):
            return 0.0
    
    def calculate_savings(self) -> float:
        """Calcular economia se produto estiver em promoção"""
        if not self.product or not self.product.is_on_sale:
            return 0.0
        
        savings_per_unit = self.product.get_savings_amount()
        return savings_per_unit * self.quantity
    
    @property
    def is_on_sale(self) -> bool:
        """Verificar se produto está em promoção"""
        return self.product and self.product.is_on_sale
    
    @property
    def subtotal_with_discount(self) -> float:
        """Subtotal considerando desconto"""
        total = self.get_total_price_float()
        savings = self.calculate_savings()
        return total - savings
