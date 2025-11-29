"""
Product Model - Modelo de produto
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, Float, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String
from app.database import DATABASE_URL

GUID = String(36) if DATABASE_URL.startswith("sqlite") else PG_UUID(as_uuid=True)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from typing import Dict, List, Optional

from app.database import Base

class Product(Base):
    """
    Modelo de produto do supermercado
    """
    __tablename__ = "products"

    # Identificação
    # Em SQLite armazenamos UUID como string para evitar erros de bind
    id = Column(GUID, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    # Códigos de identificação
    barcode = Column(String(50), unique=True, nullable=False, index=True)
    sku = Column(String(100), nullable=True, index=True)
    gtin = Column(String(14), nullable=True)  # Global Trade Item Number
    
    # Dados básicos
    name = Column(String(255), nullable=False, index=True)
    brand = Column(String(100), nullable=True, index=True)
    manufacturer = Column(String(100), nullable=True)
    
    # Categorização
    category = Column(String(100), nullable=True, index=True)
    subcategory = Column(String(100), nullable=True)
    department = Column(String(50), nullable=True)
    
    # Descrição e especificações
    description = Column(Text, nullable=True)
    ingredients = Column(Text, nullable=True)
    nutritional_info = Column(JSON, nullable=True)
    
    # Preços
    price = Column(String(20), default="0.00")  # Preço atual
    original_price = Column(String(20), nullable=True)  # Preço original (para promoções)
    cost_price = Column(String(20), nullable=True)  # Preço de custo
    
    # Características físicas
    weight_grams = Column(Integer, nullable=True)
    volume_ml = Column(Integer, nullable=True)
    dimensions = Column(JSON, nullable=True)  # {"length": 10, "width": 5, "height": 15}
    
    # Embalagem
    packaging_type = Column(String(50), nullable=True)  # "lata", "garrafa", "caixa", etc.
    packaging_material = Column(String(50), nullable=True)  # "plástico", "vidro", "papel"
    is_recyclable = Column(Boolean, default=True)
    
    # Status e disponibilidade
    is_active = Column(Boolean, default=True)
    is_available = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=10)
    
    # Imagens
    image_url = Column(Text, nullable=True)
    thumbnail_url = Column(Text, nullable=True)
    additional_images = Column(JSON, nullable=True)  # Lista de URLs
    
    # ESG e Sustentabilidade
    esg_score = Column(Integer, default=50)
    carbon_footprint_kg = Column(Float, nullable=True)
    is_organic = Column(Boolean, default=False)
    is_fair_trade = Column(Boolean, default=False)
    is_local_product = Column(Boolean, default=False)
    sustainability_certifications = Column(JSON, nullable=True)  # Lista de certificações
    
    # Informações nutricionais e de saúde
    calories_per_100g = Column(Integer, nullable=True)
    is_gluten_free = Column(Boolean, default=False)
    is_lactose_free = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_vegetarian = Column(Boolean, default=False)
    allergens = Column(JSON, nullable=True)  # Lista de alérgenos
    
    # Datas importantes
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    manufacture_date = Column(DateTime(timezone=True), nullable=True)
    
    # Métricas de popularidade
    scan_count = Column(Integer, default=0)
    purchase_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    
    # Configurações de reconhecimento
    recognition_confidence = Column(Float, default=0.0)  # Última confiança de reconhecimento
    recognition_keywords = Column(JSON, nullable=True)  # Palavras-chave para reconhecimento
    
    # Promoções e ofertas
    is_on_sale = Column(Boolean, default=False)
    sale_start_date = Column(DateTime(timezone=True), nullable=True)
    sale_end_date = Column(DateTime(timezone=True), nullable=True)
    discount_percent = Column(Float, default=0.0)
    
    # Integração com fornecedores
    supplier_id = Column(String(100), nullable=True)
    supplier_product_code = Column(String(100), nullable=True)
    
    # Metadados
    tags = Column(JSON, nullable=True)  # Tags para busca e categorização
    search_keywords = Column(Text, nullable=True)  # Palavras-chave para busca
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_scanned = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Product {self.name} ({self.barcode})>"
    
    def to_dict(self, include_detailed: bool = False):
        """Converter para dicionário"""
        base_data = {
            "id": str(self.id),
            "barcode": self.barcode,
            "name": self.name,
            "brand": self.brand,
            "category": self.category,
            "price": self.price,
            "original_price": self.original_price,
            "image_url": self.image_url,
            "thumbnail_url": self.thumbnail_url,
            "is_available": self.is_available,
            "is_on_sale": self.is_on_sale,
            "discount_percent": self.discount_percent,
            "esg_score": self.esg_score,
            "rating": self.rating,
            "review_count": self.review_count,
            "is_organic": self.is_organic,
            "is_vegan": self.is_vegan,
            "is_gluten_free": self.is_gluten_free,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
        
        if include_detailed:
            base_data.update({
                "sku": self.sku,
                "description": self.description,
                "ingredients": self.ingredients,
                "nutritional_info": self.nutritional_info,
                "weight_grams": self.weight_grams,
                "volume_ml": self.volume_ml,
                "packaging_type": self.packaging_type,
                "carbon_footprint_kg": self.carbon_footprint_kg,
                "calories_per_100g": self.calories_per_100g,
                "allergens": self.allergens,
                "sustainability_certifications": self.sustainability_certifications,
                "additional_images": self.additional_images,
                "tags": self.tags,
                "scan_count": self.scan_count,
                "purchase_count": self.purchase_count
            })
        
        return base_data
    
    def increment_scan_count(self):
        """Incrementar contador de escaneamentos"""
        from datetime import datetime
        self.scan_count += 1
        self.last_scanned = datetime.utcnow()
    
    def increment_purchase_count(self):
        """Incrementar contador de compras"""
        self.purchase_count += 1
    
    def update_rating(self, new_rating: float):
        """Atualizar rating com nova avaliação"""
        if self.review_count == 0:
            self.rating = new_rating
        else:
            current_total = self.rating * self.review_count
            self.rating = (current_total + new_rating) / (self.review_count + 1)
        
        self.review_count += 1
    
    def apply_discount(self, discount_percent: float, start_date=None, end_date=None):
        """Aplicar desconto ao produto"""
        from datetime import datetime, timedelta
        
        if not self.original_price:
            self.original_price = self.price
        
        current_price = float(self.price)
        discounted_price = current_price * (1 - discount_percent / 100)
        
        self.price = str(round(discounted_price, 2))
        self.discount_percent = discount_percent
        self.is_on_sale = True
        
        if start_date:
            self.sale_start_date = start_date
        else:
            self.sale_start_date = datetime.utcnow()
        
        if end_date:
            self.sale_end_date = end_date
        else:
            # Default: promoção por 7 dias
            self.sale_end_date = datetime.utcnow() + timedelta(days=7)
    
    def remove_discount(self):
        """Remover desconto do produto"""
        if self.original_price:
            self.price = self.original_price
            self.original_price = None
        
        self.discount_percent = 0.0
        self.is_on_sale = False
        self.sale_start_date = None
        self.sale_end_date = None
    
    def calculate_esg_score(self):
        """Calcular ESG score baseado nas características do produto"""
        score = 50  # Score base
        
        # Fatores positivos
        if self.is_organic:
            score += 15
        if self.is_local_product:
            score += 10
        if self.is_fair_trade:
            score += 10
        if self.is_recyclable:
            score += 5
        if self.carbon_footprint_kg and self.carbon_footprint_kg < 1.0:
            score += 10
        
        # Certificações sustentáveis
        if self.sustainability_certifications:
            score += len(self.sustainability_certifications) * 5
        
        # Limitar entre 0 e 100
        self.esg_score = max(0, min(100, score))
        return self.esg_score
    
    def get_price_float(self) -> float:
        """Obter preço como float"""
        try:
            return float(self.price)
        except (ValueError, TypeError):
            return 0.0
    
    def get_original_price_float(self) -> Optional[float]:
        """Obter preço original como float"""
        if not self.original_price:
            return None
        try:
            return float(self.original_price)
        except (ValueError, TypeError):
            return None
    
    def get_savings_amount(self) -> float:
        """Calcular valor economizado"""
        if not self.is_on_sale or not self.original_price:
            return 0.0
        
        original = self.get_original_price_float()
        current = self.get_price_float()
        
        if original and current:
            return original - current
        return 0.0
    
    @property
    def display_name(self) -> str:
        """Nome para exibição com marca"""
        if self.brand:
            return f"{self.brand} {self.name}"
        return self.name
    
    @property
    def is_expired(self) -> bool:
        """Verificar se produto está vencido"""
        if not self.expiry_date:
            return False
        
        from datetime import datetime
        return datetime.utcnow() > self.expiry_date
    
    @property
    def is_low_stock(self) -> bool:
        """Verificar se estoque está baixo"""
        return self.stock_quantity <= self.min_stock_level
    
    @property
    def esg_level(self) -> str:
        """Nível ESG do produto"""
        if self.esg_score >= 80:
            return "Excelente"
        elif self.esg_score >= 60:
            return "Bom"
        elif self.esg_score >= 40:
            return "Regular"
        else:
            return "Iniciante"
    
    @property
    def sustainability_badges(self) -> List[str]:
        """Lista de badges de sustentabilidade"""
        badges = []
        
        if self.is_organic:
            badges.append("Orgânico")
        if self.is_local_product:
            badges.append("Produto Local")
        if self.is_fair_trade:
            badges.append("Comércio Justo")
        if self.is_vegan:
            badges.append("Vegano")
        if self.is_gluten_free:
            badges.append("Sem Glúten")
        if self.is_recyclable:
            badges.append("Reciclável")
        
        return badges
