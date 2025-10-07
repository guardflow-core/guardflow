"""
User Model - Modelo de usuário integrado com GuardPass
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String
from app.database import DATABASE_URL

# Tipo UUID compatível com SQLite
GUID = String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True)
from sqlalchemy.sql import func
import uuid
from datetime import datetime

from app.database import Base

class User(Base):
    """
    Modelo de usuário integrado com GuardPass
    """
    __tablename__ = "users"

    # Identificação
    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    guardpass_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Dados pessoais
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    
    # Avatar/foto
    avatar_url = Column(Text, nullable=True)
    
    # Preferências
    preferred_language = Column(String(5), default="pt-BR")
    preferred_currency = Column(String(3), default="BRL")
    
    # Configurações de notificação
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)
    
    # ESG Score (integração GuardPass)
    esg_score = Column(Integer, default=50)
    esg_last_updated = Column(DateTime(timezone=True), nullable=True)
    
    # Gamificação
    total_purchases = Column(Integer, default=0)
    total_amount_spent = Column(String(20), default="0.00")  # Stored as string to avoid precision issues
    loyalty_points = Column(Integer, default=0)
    
    # Status da conta
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    
    # Dados de acesso
    last_login = Column(DateTime(timezone=True), nullable=True)
    login_count = Column(Integer, default=0)
    
    # Localização (para recomendações)
    last_known_city = Column(String(100), nullable=True)
    last_known_state = Column(String(2), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Metadados
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    def __repr__(self):
        return f"<User {self.name} ({self.email})>"
    
    def to_dict(self):
        """Converter para dicionário (sem dados sensíveis)"""
        return {
            "id": str(self.id),
            "guardpass_id": self.guardpass_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "avatar_url": self.avatar_url,
            "preferred_language": self.preferred_language,
            "esg_score": self.esg_score,
            "total_purchases": self.total_purchases,
            "loyalty_points": self.loyalty_points,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_premium": self.is_premium,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def update_login_info(self, ip_address: str = None, user_agent: str = None):
        """Atualizar informações de login"""
        self.last_login = datetime.utcnow()
        self.login_count += 1
        if ip_address:
            self.ip_address = ip_address
        if user_agent:
            self.user_agent = user_agent
    
    def add_loyalty_points(self, points: int):
        """Adicionar pontos de fidelidade"""
        self.loyalty_points += points
    
    def update_esg_score(self, new_score: int):
        """Atualizar ESG score"""
        self.esg_score = new_score
        self.esg_last_updated = datetime.utcnow()
    
    def increment_purchases(self, amount: float):
        """Incrementar estatísticas de compras"""
        self.total_purchases += 1
        current_amount = float(self.total_amount_spent)
        self.total_amount_spent = str(current_amount + amount)
    
    @property
    def display_name(self) -> str:
        """Nome para exibição"""
        return self.name or self.email.split("@")[0]
    
    @property
    def is_new_user(self) -> bool:
        """Verificar se é usuário novo (menos de 7 dias)"""
        if not self.created_at:
            return True
        
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        return self.created_at > week_ago
    
    @property
    def esg_level(self) -> str:
        """Nível ESG baseado no score"""
        if self.esg_score >= 80:
            return "Excelente"
        elif self.esg_score >= 60:
            return "Bom" 
        elif self.esg_score >= 40:
            return "Regular"
        else:
            return "Iniciante"
    
    @property
    def loyalty_level(self) -> str:
        """Nível de fidelidade baseado nos pontos"""
        if self.loyalty_points >= 10000:
            return "Diamante"
        elif self.loyalty_points >= 5000:
            return "Ouro"
        elif self.loyalty_points >= 1000:
            return "Prata"
        else:
            return "Bronze"



