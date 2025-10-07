"""
Schemas de Produto para GuardFlow
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base para produto"""
    name: str = Field(..., description="Nome do produto")
    barcode: str = Field(..., description="Código de barras")
    price: float = Field(..., gt=0, description="Preço do produto")
    description: Optional[str] = Field(None, description="Descrição do produto")
    category: Optional[str] = Field(None, description="Categoria do produto")
    brand: Optional[str] = Field(None, description="Marca do produto")
    image_url: Optional[str] = Field(None, description="URL da imagem")
    
    # ESG
    esg_score: Optional[float] = Field(None, ge=0, le=100, description="Score ESG (0-100)")
    is_organic: bool = Field(False, description="Produto orgânico")
    is_local: bool = Field(False, description="Produto local")
    carbon_footprint: Optional[float] = Field(None, description="Pegada de carbono")
    recyclable_packaging: bool = Field(False, description="Embalagem reciclável")


class ProductScanRequest(BaseModel):
    """Request para scan de produto"""
    image_data: Optional[str] = Field(None, description="Imagem em base64")
    barcode: Optional[str] = Field(None, description="Código de barras")
    store_id: Optional[str] = Field(None, description="ID da loja")
    
    class Config:
        json_schema_extra = {
            "example": {
                "barcode": "7891234567890",
                "store_id": "store_123"
            }
        }


class ProductResponse(ProductBase):
    """Response de produto"""
    id: str
    store_id: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, description="Quantidade em estoque")
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    promotion_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "prod_123",
                "name": "Arroz Integral 1kg",
                "barcode": "7891234567890",
                "price": 12.99,
                "category": "Alimentos",
                "brand": "Marca X",
                "esg_score": 85.5,
                "is_organic": True,
                "is_local": True,
                "recyclable_packaging": True,
                "stock_quantity": 150,
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }


class ProductCreateRequest(ProductBase):
    """Request para criar produto"""
    store_id: str = Field(..., description="ID da loja")
    stock_quantity: Optional[int] = Field(100, description="Quantidade inicial")


class ProductUpdateRequest(BaseModel):
    """Request para atualizar produto"""
    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None
    stock_quantity: Optional[int] = None
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    promotion_text: Optional[str] = None
    
    # ESG
    esg_score: Optional[float] = Field(None, ge=0, le=100)
    is_organic: Optional[bool] = None
    is_local: Optional[bool] = None
    carbon_footprint: Optional[float] = None
    recyclable_packaging: Optional[bool] = None


class ProductSearchRequest(BaseModel):
    """Request para buscar produtos"""
    query: Optional[str] = Field(None, description="Termo de busca")
    category: Optional[str] = Field(None, description="Filtro por categoria")
    brand: Optional[str] = Field(None, description="Filtro por marca")
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    min_esg_score: Optional[float] = Field(None, ge=0, le=100)
    is_organic: Optional[bool] = None
    is_local: Optional[bool] = None
    store_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "arroz",
                "category": "Alimentos",
                "min_esg_score": 70,
                "is_organic": True
            }
        }
