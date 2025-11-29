"""
Store API Endpoints
API para gerenciamento de supermercados
DIA 1 MVP - CRUD básico funcional
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from datetime import datetime
from typing import Optional, List
import math

from app.database import get_db
from app.config import settings, AppMessages
from app.models.user import User
from app.models.store import Store
from app.models.product import Product
from app.utils.security import get_current_user

# Logger
logger = logging.getLogger("guardflow.store")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

@router.get("/")
async def list_stores(
    city: Optional[str] = None,
    state: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: Optional[float] = 10.0,
    limit: int = Query(20, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Listar supermercados
    Suporte a filtros por localização
    """
    try:
        from sqlalchemy import select, and_, or_
        
        query = select(Store).where(Store.is_active == True)
        
        # Filtros de localização
        if city:
            query = query.where(Store.city.ilike(f"%{city}%"))
        
        if state:
            query = query.where(Store.state.ilike(f"%{state}%"))
        
        # Filtro por coordenadas (simplificado para MVP)
        if lat and lon:
            # Em produção, usar função de distância do PostGIS
            lat_range = radius_km / 111.0  # Aproximação: 1 grau ≈ 111km
            lon_range = radius_km / (111.0 * math.cos(math.radians(lat)))
            
            query = query.where(
                and_(
                    Store.latitude.between(lat - lat_range, lat + lat_range),
                    Store.longitude.between(lon - lon_range, lon + lon_range)
                )
            )
        
        query = query.limit(limit).offset(offset)
        
        result = await db.execute(query)
        stores = result.scalars().all()
        
        # Calcular distância se coordenadas fornecidas
        stores_data = []
        for store in stores:
            store_dict = store.to_dict()
            
            if lat and lon and store.latitude and store.longitude:
                distance = store.calculate_distance_km(lat, lon)
                store_dict["distance_km"] = round(distance, 2)
            
            stores_data.append(store_dict)
        
        # Ordenar por distância se aplicável
        if lat and lon:
            stores_data.sort(key=lambda x: x.get("distance_km", float('inf')))
        
        logger.info(f"🏪 {len(stores)} supermercados encontrados")
        
        return {
            "success": True,
            "message": f"Agilizou! {len(stores)} supermercados encontrados! 🏪",
            "data": {
                "stores": stores_data,
                "total": len(stores),
                "limit": limit,
                "offset": offset,
                "filters": {
                    "city": city,
                    "state": state,
                    "radius_km": radius_km if lat and lon else None
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar supermercados: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar supermercados"
        )

@router.get("/{store_id}")
async def get_store(
    store_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Obter detalhes de um supermercado
    """
    try:
        from sqlalchemy import select
        
        result = await db.execute(
            select(Store).where(
                Store.id == store_id,
                Store.is_active == True
            )
        )
        store = result.scalar_one_or_none()
        
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supermercado não encontrado! 🏪"
            )
        
        # Dados adicionais
        store_data = store.to_dict()
        store_data["opening_hours_today"] = store.get_opening_hours_today()
        store_data["is_open_now"] = store.is_open_now()
        store_data["full_address"] = store.full_address
        store_data["size_description"] = store.size_description
        store_data["esg_level"] = store.esg_level
        
        logger.info(f"🏪 Supermercado consultado: {store.name}")
        
        return {
            "success": True,
            "message": f"Supermercado agilizado! {store.name} 🏪",
            "data": store_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao buscar supermercado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar supermercado"
        )

@router.post("/{store_id}/checkin")
@limiter.limit("10/minute")
async def checkin_store(
    request: Request,
    store_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Fazer check-in em um supermercado
    """
    try:
        from sqlalchemy import select
        
        result = await db.execute(
            select(Store).where(
                Store.id == store_id,
                Store.is_active == True
            )
        )
        store = result.scalar_one_or_none()
        
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supermercado não encontrado! 🏪"
            )
        
        # Verificar se está aberto
        if not store.is_open_now():
            return {
                "success": True,
                "message": f"Check-in realizado, mas {store.name} está fechado no momento 🕐",
                "data": {
                    "store_id": store_id,
                    "store_name": store.name,
                    "is_open": False,
                    "opening_hours_today": store.get_opening_hours_today(),
                    "checkin_time": datetime.utcnow().isoformat()
                },
                "warning": "Supermercado fechado"
            }
        
        logger.info(f"📍 Check-in: {current_user.email} em {store.name}")
        
        return {
            "success": True,
            "message": f"Check-in agilizado em {store.name}! Boas compras! 🛒",
            "data": {
                "store_id": store_id,
                "store_name": store.name,
                "is_open": True,
                "opening_hours_today": store.get_opening_hours_today(),
                "checkin_time": datetime.utcnow().isoformat(),
                "user_loyalty_points": current_user.loyalty_points
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no check-in: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao fazer check-in"
        )

@router.get("/{store_id}/products")
async def get_store_products(
    store_id: str,
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Listar produtos de um supermercado
    """
    try:
        from sqlalchemy import select, and_, or_
        
        # Verificar se supermercado existe
        store_result = await db.execute(
            select(Store).where(
                Store.id == store_id,
                Store.is_active == True
            )
        )
        store = store_result.scalar_one_or_none()
        
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supermercado não encontrado! 🏪"
            )
        
        # Buscar produtos (MVP: todos os produtos, em produção seria por loja)
        query = select(Product).where(
            and_(
                Product.is_active == True,
                Product.is_available == True
            )
        )
        
        # Filtros
        if category:
            query = query.where(Product.category.ilike(f"%{category}%"))
        
        if search:
            query = query.where(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.brand.ilike(f"%{search}%"),
                    Product.barcode.ilike(f"%{search}%")
                )
            )
        
        query = query.limit(limit).offset(offset)
        
        result = await db.execute(query)
        products = result.scalars().all()
        
        products_data = [product.to_dict() for product in products]
        
        logger.info(f"🛒 {len(products)} produtos encontrados em {store.name}")
        
        return {
            "success": True,
            "message": f"Produtos agilizados! {len(products)} itens de {store.name} 🛒",
            "data": {
                "store": {
                    "id": store_id,
                    "name": store.name,
                    "is_open": store.is_open_now()
                },
                "products": products_data,
                "total": len(products),
                "limit": limit,
                "offset": offset,
                "filters": {
                    "category": category,
                    "search": search
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao buscar produtos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar produtos do supermercado"
        )

@router.get("/{store_id}/stats")
async def get_store_stats(
    store_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Estatísticas do supermercado
    """
    try:
        from sqlalchemy import select, func
        from app.models.transaction import Transaction
        
        # Verificar se supermercado existe
        store_result = await db.execute(
            select(Store).where(
                Store.id == store_id,
                Store.is_active == True
            )
        )
        store = store_result.scalar_one_or_none()
        
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supermercado não encontrado! 🏪"
            )
        
        # Estatísticas básicas
        stats = {
            "store_info": {
                "name": store.name,
                "rating": store.rating,
                "total_reviews": store.total_reviews,
                "esg_score": store.esg_score,
                "esg_level": store.esg_level
            },
            "transactions": {
                "total": store.total_transactions,
                "total_revenue": store.total_revenue
            },
            "operational": {
                "is_open_now": store.is_open_now(),
                "opening_hours_today": store.get_opening_hours_today(),
                "guardflow_enabled": store.guardflow_enabled,
                "max_concurrent_users": store.max_concurrent_users
            }
        }
        
        logger.info(f"📊 Estatísticas consultadas: {store.name}")
        
        return {
            "success": True,
            "message": f"Estatísticas agilizadas de {store.name}! 📊",
            "data": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao buscar estatísticas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar estatísticas do supermercado"
        )

# Endpoints de desenvolvimento
if settings.DEBUG:
    @router.post("/populate-stores")
    async def populate_mock_stores(db: AsyncSession = Depends(get_db)):
        """
        Popular banco com supermercados mock para demonstração
        """
        try:
            mock_stores = [
                {
                    "name": "Supermercado Zona Sul",
                    "brand": "Zona Sul",
                    "address": "Rua das Laranjeiras, 123",
                    "neighborhood": "Laranjeiras",
                    "city": "Rio de Janeiro",
                    "state": "RJ",
                    "zipcode": "22240-001",
                    "latitude": -22.9068,
                    "longitude": -43.1729,
                    "phone": "(21) 3333-4444",
                    "opening_hours": {
                        "segunda": "07:00-22:00",
                        "terça": "07:00-22:00",
                        "quarta": "07:00-22:00",
                        "quinta": "07:00-22:00",
                        "sexta": "07:00-23:00",
                        "sábado": "07:00-23:00",
                        "domingo": "08:00-20:00"
                    }
                },
                {
                    "name": "Angeloni Centro",
                    "brand": "Angeloni",
                    "address": "Av. Mauro Ramos, 456",
                    "neighborhood": "Centro",
                    "city": "Florianópolis",
                    "state": "SC",
                    "zipcode": "88020-300",
                    "latitude": -27.5954,
                    "longitude": -48.5480,
                    "phone": "(48) 3333-5555",
                    "opening_hours": {
                        "segunda": "08:00-22:00",
                        "terça": "08:00-22:00",
                        "quarta": "08:00-22:00",
                        "quinta": "08:00-22:00",
                        "sexta": "08:00-22:00",
                        "sábado": "08:00-22:00",
                        "domingo": "09:00-20:00"
                    }
                },
                {
                    "name": "Condor Vila Madalena",
                    "brand": "Condor",
                    "address": "Rua Harmonia, 789",
                    "neighborhood": "Vila Madalena",
                    "city": "São Paulo",
                    "state": "SP",
                    "zipcode": "05435-000",
                    "latitude": -23.5505,
                    "longitude": -46.6333,
                    "phone": "(11) 3333-6666",
                    "opening_hours": {
                        "segunda": "06:00-23:00",
                        "terça": "06:00-23:00",
                        "quarta": "06:00-23:00",
                        "quinta": "06:00-23:00",
                        "sexta": "06:00-24:00",
                        "sábado": "06:00-24:00",
                        "domingo": "07:00-22:00"
                    }
                }
            ]
            
            created_count = 0
            for mock_data in mock_stores:
                # Verificar se já existe
                from sqlalchemy import select
                result = await db.execute(
                    select(Store).where(Store.name == mock_data["name"])
                )
                existing = result.scalar_one_or_none()
                
                if not existing:
                    store = Store(
                        name=mock_data["name"],
                        brand=mock_data["brand"],
                        address=mock_data["address"],
                        neighborhood=mock_data["neighborhood"],
                        city=mock_data["city"],
                        state=mock_data["state"],
                        zipcode=mock_data["zipcode"],
                        latitude=mock_data["latitude"],
                        longitude=mock_data["longitude"],
                        phone=mock_data["phone"],
                        opening_hours=mock_data["opening_hours"],
                        is_active=True,
                        guardflow_enabled=True,
                        store_type="supermarket",
                        size_category="medium",
                        rating=4.5,
                        esg_score=75,
                        has_parking=True,
                        has_wifi=True,
                        has_bakery=True
                    )
                    
                    db.add(store)
                    created_count += 1
            
            await db.commit()
            
            return {
                "success": True,
                "message": f"Agilizou! {created_count} supermercados criados para demonstração! 🏪",
                "data": {
                    "created_stores": created_count,
                    "total_stores": len(mock_stores)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao popular supermercados: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar supermercados mock"
            )
