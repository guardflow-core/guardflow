"""
Schemas de Loja para GuardFlow
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, time
from pydantic import BaseModel, Field


class StoreBase(BaseModel):
    """Base para loja"""
    name: str = Field(..., description="Nome da loja")
    cnpj: str = Field(..., description="CNPJ da loja")
    address: str = Field(..., description="Endereço completo")
    city: str = Field(..., description="Cidade")
    state: str = Field(..., description="Estado (UF)")
    zip_code: str = Field(..., description="CEP")
    phone: str = Field(..., description="Telefone")
    email: Optional[str] = Field(None, description="Email de contato")
    
    # Coordenadas
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    
    # Configurações
    accepts_guardflow: bool = Field(True, description="Aceita GuardFlow")
    has_smart_carts: bool = Field(False, description="Possui carrinhos inteligentes")
    self_checkout_enabled: bool = Field(True, description="Self-checkout habilitado")
    
    # ESG
    esg_certified: bool = Field(False, description="Certificação ESG")
    local_products_percentage: Optional[float] = Field(None, ge=0, le=100)
    renewable_energy: bool = Field(False, description="Usa energia renovável")


class StoreResponse(StoreBase):
    """Response de loja"""
    id: str
    is_active: bool = True
    rating: Optional[float] = Field(None, ge=0, le=5)
    total_reviews: int = 0
    
    # Horários
    opening_time: Optional[str] = Field(None, description="Horário de abertura")
    closing_time: Optional[str] = Field(None, description="Horário de fechamento")
    is_24h: bool = Field(False, description="Funciona 24h")
    
    # Estatísticas
    avg_queue_time: Optional[float] = Field(None, description="Tempo médio de fila (minutos)")
    current_queue_size: Optional[int] = Field(None, description="Tamanho atual da fila")
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "store_123",
                "name": "Supermercado Exemplo",
                "cnpj": "12.345.678/0001-90",
                "address": "Rua Exemplo, 123",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234-567",
                "phone": "(11) 98765-4321",
                "latitude": -23.550520,
                "longitude": -46.633308,
                "accepts_guardflow": True,
                "has_smart_carts": True,
                "self_checkout_enabled": True,
                "esg_certified": True,
                "local_products_percentage": 40,
                "renewable_energy": True,
                "is_active": True,
                "rating": 4.5,
                "total_reviews": 250,
                "opening_time": "07:00",
                "closing_time": "22:00",
                "avg_queue_time": 5.5,
                "current_queue_size": 3,
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }


class StoreCreateRequest(StoreBase):
    """Request para criar loja"""
    manager_id: Optional[str] = Field(None, description="ID do gerente")


class StoreUpdateRequest(BaseModel):
    """Request para atualizar loja"""
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    accepts_guardflow: Optional[bool] = None
    has_smart_carts: Optional[bool] = None
    self_checkout_enabled: Optional[bool] = None
    
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    is_24h: Optional[bool] = None
    
    esg_certified: Optional[bool] = None
    local_products_percentage: Optional[float] = Field(None, ge=0, le=100)
    renewable_energy: Optional[bool] = None


class StoreSearchRequest(BaseModel):
    """Request para buscar lojas"""
    query: Optional[str] = Field(None, description="Termo de busca")
    city: Optional[str] = Field(None, description="Filtrar por cidade")
    state: Optional[str] = Field(None, description="Filtrar por estado")
    
    # Geolocalização
    latitude: Optional[float] = Field(None, description="Latitude para busca por proximidade")
    longitude: Optional[float] = Field(None, description="Longitude para busca por proximidade")
    radius_km: Optional[float] = Field(5, gt=0, le=50, description="Raio de busca em km")
    
    # Filtros
    only_guardflow: bool = Field(False, description="Apenas lojas com GuardFlow")
    only_smart_carts: bool = Field(False, description="Apenas com carrinhos inteligentes")
    only_esg: bool = Field(False, description="Apenas certificadas ESG")
    is_open_now: bool = Field(False, description="Apenas lojas abertas agora")
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": -23.550520,
                "longitude": -46.633308,
                "radius_km": 5,
                "only_guardflow": True
            }
        }


class StoreListResponse(BaseModel):
    """Response de lista de lojas"""
    stores: List[StoreResponse]
    total_count: int
    nearby_count: Optional[int] = Field(None, description="Quantidade de lojas próximas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "stores": [],
                "total_count": 10,
                "nearby_count": 3
            }
        }


class QueueStatusResponse(BaseModel):
    """Response de status da fila"""
    store_id: str
    current_size: int = Field(..., description="Tamanho atual da fila")
    estimated_wait_time: float = Field(..., description="Tempo estimado de espera (minutos)")
    trend: str = Field(..., description="Tendência (increasing, stable, decreasing)")
    last_updated: datetime
    
    # Previsão AI
    predicted_size_30min: Optional[int] = Field(None, description="Previsão para 30 min")
    predicted_size_60min: Optional[int] = Field(None, description="Previsão para 60 min")
    best_time_to_shop: Optional[str] = Field(None, description="Melhor horário para compras")
    
    class Config:
        json_schema_extra = {
            "example": {
                "store_id": "store_123",
                "current_size": 5,
                "estimated_wait_time": 7.5,
                "trend": "decreasing",
                "last_updated": "2024-01-01T10:30:00",
                "predicted_size_30min": 3,
                "predicted_size_60min": 2,
                "best_time_to_shop": "11:00-12:00"
            }
        }
