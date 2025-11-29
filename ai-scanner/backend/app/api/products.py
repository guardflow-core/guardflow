"""
Products API Endpoints
API para gerenciamento de produtos e catálogo
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from app.database import get_db
from app.config import settings, AppMessages
from app.models.user import User
from app.models.product import Product
from app.models.store import Store
from app.schemas.product import (
    ProductResponse, ProductCreate, ProductUpdate, ProductListResponse,
    ProductSearchFilters, ProductCategoryResponse, ProductStatsResponse
)
from app.services.product_service import ProductService
from app.utils.security import get_current_user, require_permissions

# Logger
logger = logging.getLogger("guardflow.products")

# Router
router = APIRouter()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Services
product_service = ProductService()

@router.get("/", response_model=ProductListResponse)
@limiter.limit("60/minute")
async def list_products(
    request: Request,
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    search: Optional[str] = Query(None, description="Termo de busca"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    store_id: Optional[UUID] = Query(None, description="Filtrar por loja"),
    min_price: Optional[float] = Query(None, ge=0, description="Preço mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Preço máximo"),
    esg_score_min: Optional[int] = Query(None, ge=0, le=100, description="Score ESG mínimo"),
    is_organic: Optional[bool] = Query(None, description="Filtrar produtos orgânicos"),
    is_vegan: Optional[bool] = Query(None, description="Filtrar produtos veganos"),
    sort_by: Optional[str] = Query("name", description="Campo para ordenação"),
    sort_order: Optional[str] = Query("asc", description="Ordem (asc/desc)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Listar produtos com filtros avançados
    """
    try:
        logger.info(f"📦 Listando produtos - {current_user.email}")
        
        # Criar filtros
        filters = ProductSearchFilters(
            search=search,
            category=category,
            store_id=store_id,
            min_price=min_price,
            max_price=max_price,
            esg_score_min=esg_score_min,
            is_organic=is_organic,
            is_vegan=is_vegan,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Buscar produtos
        products, total = await product_service.list_products(
            db=db,
            skip=skip,
            limit=limit,
            filters=filters
        )
        
        return ProductListResponse(
            products=[ProductResponse.from_orm(product) for product in products],
            total=total,
            skip=skip,
            limit=limit,
            has_more=skip + limit < total
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao listar produtos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/{product_id}", response_model=ProductResponse)
@limiter.limit("120/minute")
async def get_product(
    request: Request,
    product_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obter produto por ID
    """
    try:
        logger.info(f"📦 Buscando produto: {product_id}")
        
        # Buscar produto
        product = await product_service.get_product_by_id(db=db, product_id=product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        return ProductResponse.from_orm(product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao obter produto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.post("/", response_model=ProductResponse)
@limiter.limit("20/minute")
async def create_product(
    request: Request,
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Criar novo produto
    """
    try:
        # Verificar permissões
        await require_permissions(current_user, ["admin", "manager"])
        
        logger.info(f"➕ Criando produto: {product_data.name}")
        
        # Verificar se loja existe
        if product_data.store_id:
            store = await product_service.get_store_by_id(db=db, store_id=product_data.store_id)
            if not store:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Loja não encontrada"
                )
        
        # Criar produto
        product = await product_service.create_product(
            db=db,
            product_data=product_data,
            created_by=current_user.id
        )
        
        logger.info(f"✅ Produto criado: {product.name}")
        
        return ProductResponse.from_orm(product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao criar produto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.put("/{product_id}", response_model=ProductResponse)
@limiter.limit("30/minute")
async def update_product(
    request: Request,
    product_id: UUID,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Atualizar produto
    """
    try:
        # Verificar permissões
        await require_permissions(current_user, ["admin", "manager"])
        
        logger.info(f"✏️ Atualizando produto: {product_id}")
        
        # Buscar produto
        product = await product_service.get_product_by_id(db=db, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        # Atualizar produto
        updated_product = await product_service.update_product(
            db=db,
            product=product,
            product_data=product_data,
            updated_by=current_user.id
        )
        
        logger.info(f"✅ Produto atualizado: {updated_product.name}")
        
        return ProductResponse.from_orm(updated_product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar produto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.delete("/{product_id}")
@limiter.limit("10/minute")
async def delete_product(
    request: Request,
    product_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Desativar produto (soft delete)
    """
    try:
        # Verificar permissões
        await require_permissions(current_user, ["admin", "manager"])
        
        logger.info(f"🗑️ Desativando produto: {product_id}")
        
        # Buscar produto
        product = await product_service.get_product_by_id(db=db, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        # Desativar produto
        await product_service.deactivate_product(
            db=db,
            product=product,
            deactivated_by=current_user.id
        )
        
        logger.info(f"✅ Produto desativado: {product.name}")
        
        return {
            "success": True,
            "message": "Produto desativado com sucesso",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao desativar produto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/categories/", response_model=List[ProductCategoryResponse])
@limiter.limit("60/minute")
async def get_categories(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obter categorias de produtos
    """
    try:
        logger.info(f"📂 Listando categorias - {current_user.email}")
        
        # Buscar categorias
        categories = await product_service.get_categories(db=db)
        
        return [ProductCategoryResponse.from_orm(category) for category in categories]
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar categorias: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/search/suggestions")
@limiter.limit("120/minute")
async def get_search_suggestions(
    request: Request,
    query: str = Query(..., min_length=2, description="Termo de busca"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de sugestões"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obter sugestões de busca
    """
    try:
        logger.info(f"🔍 Sugestões de busca: {query}")
        
        # Buscar sugestões
        suggestions = await product_service.get_search_suggestions(
            db=db,
            query=query,
            limit=limit
        )
        
        return {
            "success": True,
            "message": "Sugestões agilizadas! 🔍",
            "data": suggestions
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter sugestões: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/stats/", response_model=ProductStatsResponse)
@limiter.limit("30/minute")
async def get_product_stats(
    request: Request,
    store_id: Optional[UUID] = Query(None, description="Filtrar por loja"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obter estatísticas de produtos
    """
    try:
        # Verificar permissões
        await require_permissions(current_user, ["admin", "manager"])
        
        logger.info(f"📊 Estatísticas de produtos - {current_user.email}")
        
        # Obter estatísticas
        stats = await product_service.get_product_stats(
            db=db,
            store_id=store_id
        )
        
        return ProductStatsResponse.from_orm(stats)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.post("/{product_id}/scan")
@limiter.limit("60/minute")
async def scan_product(
    request: Request,
    product_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Registrar escaneamento de produto
    """
    try:
        logger.info(f"📱 Escaneando produto: {product_id}")
        
        # Buscar produto
        product = await product_service.get_product_by_id(db=db, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        # Registrar escaneamento
        await product_service.record_product_scan(
            db=db,
            product=product,
            user=current_user
        )
        
        logger.info(f"✅ Escaneamento registrado: {product.name}")
        
        return {
            "success": True,
            "message": "Produto agilizado! 📱",
            "data": {
                "product_id": str(product_id),
                "product_name": product.name,
                "scan_timestamp": datetime.utcnow().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao escanear produto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

@router.get("/barcode/{barcode}")
@limiter.limit("120/minute")
async def get_product_by_barcode(
    request: Request,
    barcode: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Buscar produto por código de barras
    """
    try:
        logger.info(f"🔍 Buscando produto por código: {barcode}")
        
        # Buscar produto
        product = await product_service.get_product_by_barcode(db=db, barcode=barcode)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        return ProductResponse.from_orm(product)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao buscar produto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=AppMessages.SERVER_ERROR
        )

# Endpoint de desenvolvimento (apenas debug)
if settings.DEBUG:
    @router.get("/debug/product-info/{product_id}")
    async def debug_product_info(
        product_id: UUID,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):
        """
        Debug: Informações detalhadas do produto (apenas desenvolvimento)
        """
        try:
            product = await product_service.get_product_by_id(db=db, product_id=product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Produto não encontrado"
                )
            
            return {
                "success": True,
                "message": "Informações do produto! 🔍",
                "data": {
                    "id": str(product.id),
                    "name": product.name,
                    "barcode": product.barcode,
                    "category": product.category,
                    "price": product.price,
                    "esg_score": product.esg_score,
                    "is_organic": product.is_organic,
                    "is_vegan": product.is_vegan,
                    "created_at": product.created_at.isoformat() if product.created_at else None,
                    "updated_at": product.updated_at.isoformat() if product.updated_at else None
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao obter informações: {str(e)}",
                "error": str(e)
            }
