# -*- coding: utf-8 -*-
"""
GuardFlow - Monetization Models
Modelos para tokenização ESG e monetização governamental
"""

from sqlalchemy import Column, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base

class InvoiceConversion(Base):
    """Modelo para conversão de NFe em tokens ESG"""
    __tablename__ = "invoice_conversions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(String(100), nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    nfe_xml = Column(Text, nullable=False)
    esg_score = Column(Float, nullable=False, default=0.0)
    token_amount = Column(Float, nullable=False, default=0.0)
    conversion_rate = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="pending")
    blockchain_tx_hash = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = relationship("User", back_populates="invoice_conversions")

class ESGAsset(Base):
    """Modelo para ativos ESG tokenizados"""
    __tablename__ = "esg_assets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_name = Column(String(200), nullable=False)
    asset_type = Column(String(50), nullable=False)  # environmental, social, governance
    token_symbol = Column(String(10), nullable=False)
    total_supply = Column(Float, nullable=False, default=0.0)
    current_price = Column(Float, nullable=False, default=0.0)
    market_cap = Column(Float, nullable=False, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MonetizationTransaction(Base):
    """Modelo para transações de monetização"""
    __tablename__ = "monetization_transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    transaction_type = Column(String(50), nullable=False)  # esg_conversion, government_credit, nft_mint
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="BRL")
    status = Column(String(50), nullable=False, default="pending")
    blockchain_tx_hash = Column(String(100), nullable=True)
    transaction_metadata = Column(Text, nullable=True)  # JSON com dados adicionais
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = relationship("User", back_populates="monetization_transactions")

class GovernmentCredit(Base):
    """Modelo para créditos governamentais"""
    __tablename__ = "government_credits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    credit_type = Column(String(50), nullable=False)  # ICMS, IPI, PIS_COFINS, LEI_DO_BEM
    invoice_id = Column(String(100), nullable=False)
    credit_amount = Column(Float, nullable=False)
    tax_rate = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = relationship("User", back_populates="government_credits")

class ESGToken(Base):
    """Modelo para tokens ESG"""
    __tablename__ = "esg_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_name = Column(String(100), nullable=False)
    token_symbol = Column(String(10), nullable=False, unique=True)
    token_type = Column(String(50), nullable=False)  # GST, ECT, AET, ECS, CCR, ECR, EST, EGM
    total_supply = Column(Float, nullable=False, default=0.0)
    circulating_supply = Column(Float, nullable=False, default=0.0)
    current_price = Column(Float, nullable=False, default=0.0)
    market_cap = Column(Float, nullable=False, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
