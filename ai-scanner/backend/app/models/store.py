"""
Store Model - Modelo de supermercado/loja
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String
from app.database import DATABASE_URL

GUID = String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True)
from sqlalchemy.sql import func
import uuid
from typing import Dict, Any

from app.database import Base

class Store(Base):
    """
    Modelo de supermercado/loja parceira
    """
    __tablename__ = "stores"

    # Identificação
    id = Column(GUID, primary_key=True, default=uuid.uuid4, index=True)
    
    # Dados básicos
    name = Column(String(255), nullable=False, index=True)
    brand = Column(String(100), nullable=True)  # Ex: "Pão de Açúcar", "Extra"
    cnpj = Column(String(18), nullable=True, unique=True)
    
    # Endereço
    address = Column(Text, nullable=False)
    neighborhood = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(2), nullable=False, index=True)
    zipcode = Column(String(10), nullable=False)
    country = Column(String(2), default="BR")
    
    # Coordenadas geográficas
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Contato
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Configurações GuardFlow
    guardflow_enabled = Column(Boolean, default=True)
    contract_start_date = Column(DateTime(timezone=True), nullable=True)
    contract_end_date = Column(DateTime(timezone=True), nullable=True)
    
    # Configurações operacionais
    opening_hours = Column(JSON, nullable=True)  # {"monday": "08:00-22:00", ...}
    timezone = Column(String(50), default="America/Sao_Paulo")
    
    # Características da loja
    store_type = Column(String(50), default="supermarket")  # supermarket, hypermarket, convenience
    size_category = Column(String(20), default="medium")  # small, medium, large
    total_area_m2 = Column(Integer, nullable=True)
    
    # Recursos disponíveis
    has_parking = Column(Boolean, default=True)
    has_wifi = Column(Boolean, default=True)
    has_pharmacy = Column(Boolean, default=False)
    has_bakery = Column(Boolean, default=True)
    has_butchery = Column(Boolean, default=True)
    
    # Configurações GuardFlow específicas
    max_concurrent_users = Column(Integer, default=50)
    scanner_stations = Column(Integer, default=5)
    checkout_timeout_minutes = Column(Integer, default=30)
    
    # Preços e comissões
    monthly_fee = Column(String(20), default="0.00")
    transaction_fee_percent = Column(Float, default=2.5)
    setup_fee = Column(String(20), default="0.00")
    
    # Status e métricas
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    total_transactions = Column(Integer, default=0)
    total_revenue = Column(String(20), default="0.00")
    
    # Rating e feedback
    rating = Column(Float, default=5.0)
    total_reviews = Column(Integer, default=0)
    
    # Configurações ESG
    esg_score = Column(Integer, default=50)
    sustainability_features = Column(JSON, nullable=True)  # Lista de features sustentáveis
    
    # Integração com sistemas
    erp_system = Column(String(100), nullable=True)  # "SAP", "TOTVS", etc.
    pos_system = Column(String(100), nullable=True)   # Sistema de PDV
    integration_status = Column(String(20), default="pending")  # pending, active, error
    
    # Metadados
    logo_url = Column(Text, nullable=True)
    banner_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_sync = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Store {self.name} ({self.city}/{self.state})>"
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            "id": str(self.id),
            "name": self.name,
            "brand": self.brand,
            "address": self.address,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "store_type": self.store_type,
            "size_category": self.size_category,
            "rating": self.rating,
            "total_reviews": self.total_reviews,
            "esg_score": self.esg_score,
            "opening_hours": self.opening_hours,
            "has_parking": self.has_parking,
            "has_wifi": self.has_wifi,
            "has_pharmacy": self.has_pharmacy,
            "has_bakery": self.has_bakery,
            "has_butchery": self.has_butchery,
            "is_active": self.is_active,
            "guardflow_enabled": self.guardflow_enabled,
            "logo_url": self.logo_url,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def get_opening_hours_today(self) -> str:
        """Obter horário de funcionamento hoje"""
        if not self.opening_hours:
            return "Não informado"
        
        from datetime import datetime
        import calendar
        
        today = datetime.now().strftime("%A").lower()
        weekday_map = {
            "monday": "segunda",
            "tuesday": "terça", 
            "wednesday": "quarta",
            "thursday": "quinta",
            "friday": "sexta",
            "saturday": "sábado",
            "sunday": "domingo"
        }
        
        portuguese_day = weekday_map.get(today, today)
        return self.opening_hours.get(portuguese_day, "Fechado")
    
    def is_open_now(self) -> bool:
        """Verificar se a loja está aberta agora"""
        if not self.opening_hours:
            return True  # Assume aberto se não tiver horário
        
        from datetime import datetime
        import pytz
        
        # Converter para timezone da loja
        tz = pytz.timezone(self.timezone)
        now = datetime.now(tz)
        
        today = now.strftime("%A").lower()
        weekday_map = {
            "monday": "segunda",
            "tuesday": "terça",
            "wednesday": "quarta", 
            "thursday": "quinta",
            "friday": "sexta",
            "saturday": "sábado",
            "sunday": "domingo"
        }
        
        portuguese_day = weekday_map.get(today, today)
        hours = self.opening_hours.get(portuguese_day)
        
        if not hours or hours == "Fechado":
            return False
        
        # Parse horário (formato: "08:00-22:00")
        try:
            start_time, end_time = hours.split("-")
            start_hour, start_min = map(int, start_time.split(":"))
            end_hour, end_min = map(int, end_time.split(":"))
            
            current_time = now.hour * 60 + now.minute
            start_minutes = start_hour * 60 + start_min
            end_minutes = end_hour * 60 + end_min
            
            return start_minutes <= current_time <= end_minutes
            
        except:
            return True  # Assume aberto em caso de erro
    
    def calculate_distance_km(self, lat: float, lon: float) -> float:
        """Calcular distância em km usando fórmula de Haversine"""
        if not self.latitude or not self.longitude:
            return float('inf')
        
        import math
        
        # Raio da Terra em km
        R = 6371
        
        # Converter para radianos
        lat1_rad = math.radians(self.latitude)
        lon1_rad = math.radians(self.longitude)
        lat2_rad = math.radians(lat)
        lon2_rad = math.radians(lon)
        
        # Diferenças
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Fórmula de Haversine
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def add_transaction(self, amount: float):
        """Adicionar transação às estatísticas"""
        self.total_transactions += 1
        current_revenue = float(self.total_revenue)
        self.total_revenue = str(current_revenue + amount)
    
    def update_rating(self, new_rating: float):
        """Atualizar rating com nova avaliação"""
        current_total = self.rating * self.total_reviews
        self.total_reviews += 1
        self.rating = (current_total + new_rating) / self.total_reviews
    
    @property
    def full_address(self) -> str:
        """Endereço completo formatado"""
        parts = [self.address]
        if self.neighborhood:
            parts.append(self.neighborhood)
        parts.extend([self.city, self.state])
        if self.zipcode:
            parts.append(f"CEP {self.zipcode}")
        return ", ".join(parts)
    
    @property
    def size_description(self) -> str:
        """Descrição do tamanho da loja"""
        descriptions = {
            "small": "Pequeno porte",
            "medium": "Médio porte", 
            "large": "Grande porte"
        }
        return descriptions.get(self.size_category, "Não informado")
    
    @property
    def esg_level(self) -> str:
        """Nível ESG da loja"""
        if self.esg_score >= 80:
            return "Excelente"
        elif self.esg_score >= 60:
            return "Bom"
        elif self.esg_score >= 40:
            return "Regular"
        else:
            return "Iniciante"
