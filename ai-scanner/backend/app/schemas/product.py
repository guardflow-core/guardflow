"""
Product Schemas
Schemas para API de produtos
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal

class ProductBase(BaseModel):
    """Schema base para produto"""
    name: str = Field(..., min_length=1, max_length=255, description="Nome do produto")
    description: Optional[str] = Field(None, max_length=1000, description="Descrição do produto")
    barcode: Optional[str] = Field(None, max_length=50, description="Código de barras")
    category: str = Field(..., description="Categoria do produto")
    price: Decimal = Field(..., ge=0, description="Preço do produto")
    unit: str = Field("unidade", description="Unidade de medida")
    weight: Optional[float] = Field(None, ge=0, description="Peso em gramas")
    volume: Optional[float] = Field(None, ge=0, description="Volume em ml")
    brand: Optional[str] = Field(None, max_length=100, description="Marca do produto")
    manufacturer: Optional[str] = Field(None, max_length=100, description="Fabricante")
    
    # Atributos ESG
    esg_score: int = Field(50, ge=0, le=100, description="Score ESG (0-100)")
    is_organic: bool = Field(False, description="Produto orgânico")
    is_vegan: bool = Field(False, description="Produto vegano")
    is_gluten_free: bool = Field(False, description="Produto sem glúten")
    is_lactose_free: bool = Field(False, description="Produto sem lactose")
    sustainability_notes: Optional[str] = Field(None, max_length=500, description="Notas de sustentabilidade")
    
    # Informações nutricionais
    calories_per_100g: Optional[float] = Field(None, ge=0, description="Calorias por 100g")
    protein_per_100g: Optional[float] = Field(None, ge=0, description="Proteína por 100g")
    carbs_per_100g: Optional[float] = Field(None, ge=0, description="Carboidratos por 100g")
    fat_per_100g: Optional[float] = Field(None, ge=0, description="Gordura por 100g")
    
    # Imagens
    image_url: Optional[str] = Field(None, description="URL da imagem principal")
    image_urls: Optional[List[str]] = Field(None, description="URLs das imagens adicionais")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Arroz Integral Orgânico",
                "description": "Arroz integral orgânico de alta qualidade",
                "barcode": "7891234567890",
                "category": "Alimentício",
                "price": 12.50,
                "unit": "kg",
                "weight": 1000.0,
                "brand": "Fazenda Orgânica",
                "manufacturer": "Fazenda Orgânica Ltda",
                "esg_score": 85,
                "is_organic": True,
                "is_vegan": True,
                "is_gluten_free": True,
                "sustainability_notes": "Cultivado sem agrotóxicos",
                "calories_per_100g": 350.0,
                "protein_per_100g": 8.0,
                "carbs_per_100g": 75.0,
                "fat_per_100g": 2.0,
                "image_url": "https://example.com/arroz.jpg"
            }
        }

class ProductCreate(ProductBase):
    """Schema para criação de produto"""
    store_id: Optional[UUID] = Field(None, description="ID da loja")
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v

class ProductUpdate(BaseModel):
    """Schema para atualização de produto"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    barcode: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    unit: Optional[str] = None
    weight: Optional[float] = Field(None, ge=0)
    volume: Optional[float] = Field(None, ge=0)
    brand: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=100)
    
    # Atributos ESG
    esg_score: Optional[int] = Field(None, ge=0, le=100)
    is_organic: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_gluten_free: Optional[bool] = None
    is_lactose_free: Optional[bool] = None
    sustainability_notes: Optional[str] = Field(None, max_length=500)
    
    # Informações nutricionais
    calories_per_100g: Optional[float] = Field(None, ge=0)
    protein_per_100g: Optional[float] = Field(None, ge=0)
    carbs_per_100g: Optional[float] = Field(None, ge=0)
    fat_per_100g: Optional[float] = Field(None, ge=0)
    
    # Imagens
    image_url: Optional[str] = None
    image_urls: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Arroz Integral Orgânico Premium",
                "price": 15.00,
                "esg_score": 90,
                "sustainability_notes": "Cultivado com práticas sustentáveis"
            }
        }

class ProductResponse(ProductBase):
    """Schema de resposta para produto"""
    id: UUID
    store_id: Optional[UUID] = None
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    
    # Estatísticas
    scan_count: int = 0
    purchase_count: int = 0
    last_scan: Optional[datetime] = None
    last_purchase: Optional[datetime] = None
    
    # Informações da loja
    store_name: Optional[str] = None
    store_address: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Arroz Integral Orgânico",
                "description": "Arroz integral orgânico de alta qualidade",
                "barcode": "7891234567890",
                "category": "Alimentício",
                "price": 12.50,
                "unit": "kg",
                "weight": 1000.0,
                "brand": "Fazenda Orgânica",
                "esg_score": 85,
                "is_organic": True,
                "is_vegan": True,
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "scan_count": 25,
                "purchase_count": 10,
                "store_name": "Supermercado Verde"
            }
        }

class ProductListResponse(BaseModel):
    """Schema de resposta para lista de produtos"""
    products: List[ProductResponse]
    total: int
    skip: int
    limit: int
    has_more: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "products": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Arroz Integral Orgânico",
                        "category": "Alimentício",
                        "price": 12.50,
                        "esg_score": 85,
                        "is_organic": True
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 100,
                "has_more": False
            }
        }

class ProductSearchFilters(BaseModel):
    """Schema para filtros de busca de produtos"""
    search: Optional[str] = Field(None, description="Termo de busca")
    category: Optional[str] = Field(None, description="Categoria")
    store_id: Optional[UUID] = Field(None, description="ID da loja")
    min_price: Optional[float] = Field(None, ge=0, description="Preço mínimo")
    max_price: Optional[float] = Field(None, ge=0, description="Preço máximo")
    esg_score_min: Optional[int] = Field(None, ge=0, le=100, description="Score ESG mínimo")
    is_organic: Optional[bool] = Field(None, description="Produtos orgânicos")
    is_vegan: Optional[bool] = Field(None, description="Produtos veganos")
    is_gluten_free: Optional[bool] = Field(None, description="Produtos sem glúten")
    is_lactose_free: Optional[bool] = Field(None, description="Produtos sem lactose")
    brand: Optional[str] = Field(None, description="Marca")
    sort_by: Optional[str] = Field("name", description="Campo para ordenação")
    sort_order: Optional[str] = Field("asc", description="Ordem (asc/desc)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "search": "arroz",
                "category": "Alimentício",
                "min_price": 10.0,
                "max_price": 20.0,
                "esg_score_min": 70,
                "is_organic": True,
                "sort_by": "price",
                "sort_order": "asc"
            }
        }

class ProductCategoryResponse(BaseModel):
    """Schema de resposta para categoria de produto"""
    id: UUID
    name: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
    is_active: bool = True
    product_count: int = 0
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Alimentício",
                "description": "Produtos alimentícios",
                "product_count": 150
            }
        }

class ProductStatsResponse(BaseModel):
    """Schema de resposta para estatísticas de produtos"""
    total_products: int
    active_products: int
    inactive_products: int
    organic_products: int
    vegan_products: int
    gluten_free_products: int
    lactose_free_products: int
    average_esg_score: float
    average_price: float
    categories_count: int
    brands_count: int
    top_categories: List[Dict[str, Any]]
    top_brands: List[Dict[str, Any]]
    esg_distribution: Dict[str, int]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_products": 1000,
                "active_products": 950,
                "inactive_products": 50,
                "organic_products": 200,
                "vegan_products": 150,
                "gluten_free_products": 100,
                "lactose_free_products": 80,
                "average_esg_score": 65.5,
                "average_price": 15.75,
                "categories_count": 15,
                "brands_count": 50,
                "top_categories": [
                    {"name": "Alimentício", "count": 300},
                    {"name": "Bebidas", "count": 200}
                ],
                "top_brands": [
                    {"name": "Marca A", "count": 50},
                    {"name": "Marca B", "count": 45}
                ],
                "esg_distribution": {
                    "excellent": 100,
                    "good": 200,
                    "neutral": 300,
                    "poor": 50
                }
            }
        }

class ProductBulkUpdate(BaseModel):
    """Schema para atualização em lote de produtos"""
    product_ids: List[UUID] = Field(..., description="IDs dos produtos para atualizar")
    updates: ProductUpdate = Field(..., description="Campos para atualizar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_ids": [
                    "123e4567-e89b-12d3-a456-426614174000",
                    "123e4567-e89b-12d3-a456-426614174001"
                ],
                "updates": {
                    "esg_score": 80,
                    "is_organic": True
                }
            }
        }

class ProductImportRequest(BaseModel):
    """Schema para importação de produtos"""
    format: str = Field("csv", description="Formato de importação (csv, excel, json)")
    data: List[Dict[str, Any]] = Field(..., description="Dados dos produtos")
    store_id: Optional[UUID] = Field(None, description="ID da loja")
    
    class Config:
        json_schema_extra = {
            "example": {
                "format": "csv",
                "store_id": "123e4567-e89b-12d3-a456-426614174000",
                "data": [
                    {
                        "name": "Produto 1",
                        "barcode": "7891234567890",
                        "category": "Alimentício",
                        "price": 10.50
                    }
                ]
            }
        }