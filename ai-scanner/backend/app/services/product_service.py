"""
Product Service
Serviço para gerenciamento de produtos
"""
import logging
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc, asc
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.models.store import Store
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductSearchFilters

logger = logging.getLogger("guardflow.product_service")

class ProductService:
    """Serviço para gerenciamento de produtos"""
    
    async def list_products(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[ProductSearchFilters] = None
    ) -> Tuple[List[Product], int]:
        """
        Listar produtos com filtros
        """
        try:
            # Query base
            query = select(Product).where(Product.is_active == True)
            
            # Aplicar filtros
            if filters:
                if filters.search:
                    search_term = f"%{filters.search}%"
                    query = query.where(
                        or_(
                            Product.name.ilike(search_term),
                            Product.description.ilike(search_term),
                            Product.brand.ilike(search_term),
                            Product.barcode.ilike(search_term)
                        )
                    )
                
                if filters.category:
                    query = query.where(Product.category == filters.category)
                
                if filters.store_id:
                    query = query.where(Product.store_id == filters.store_id)
                
                if filters.min_price is not None:
                    query = query.where(Product.price >= filters.min_price)
                
                if filters.max_price is not None:
                    query = query.where(Product.price <= filters.max_price)
                
                if filters.esg_score_min is not None:
                    query = query.where(Product.esg_score >= filters.esg_score_min)
                
                if filters.is_organic is not None:
                    query = query.where(Product.is_organic == filters.is_organic)
                
                if filters.is_vegan is not None:
                    query = query.where(Product.is_vegan == filters.is_vegan)
                
                if filters.is_gluten_free is not None:
                    query = query.where(Product.is_gluten_free == filters.is_gluten_free)
                
                if filters.is_lactose_free is not None:
                    query = query.where(Product.is_lactose_free == filters.is_lactose_free)
                
                if filters.brand:
                    query = query.where(Product.brand.ilike(f"%{filters.brand}%"))
                
                # Ordenação
                if filters.sort_by:
                    if filters.sort_by == "name":
                        order_func = asc(Product.name) if filters.sort_order == "asc" else desc(Product.name)
                    elif filters.sort_by == "price":
                        order_func = asc(Product.price) if filters.sort_order == "asc" else desc(Product.price)
                    elif filters.sort_by == "esg_score":
                        order_func = asc(Product.esg_score) if filters.sort_order == "asc" else desc(Product.esg_score)
                    elif filters.sort_by == "created_at":
                        order_func = asc(Product.created_at) if filters.sort_order == "asc" else desc(Product.created_at)
                    else:
                        order_func = asc(Product.name)
                    
                    query = query.order_by(order_func)
            
            # Contar total
            count_query = select(func.count(Product.id)).where(Product.is_active == True)
            if filters and filters.search:
                search_term = f"%{filters.search}%"
                count_query = count_query.where(
                    or_(
                        Product.name.ilike(search_term),
                        Product.description.ilike(search_term),
                        Product.brand.ilike(search_term),
                        Product.barcode.ilike(search_term)
                    )
                )
            
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            # Aplicar paginação
            query = query.offset(skip).limit(limit)
            
            # Executar query
            result = await db.execute(query)
            products = result.scalars().all()
            
            return products, total
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar produtos: {str(e)}")
            raise
    
    async def get_product_by_id(
        self,
        db: AsyncSession,
        product_id: UUID
    ) -> Optional[Product]:
        """
        Buscar produto por ID
        """
        try:
            query = select(Product).where(
                and_(
                    Product.id == product_id,
                    Product.is_active == True
                )
            ).options(selectinload(Product.store))
            
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar produto: {str(e)}")
            raise
    
    async def get_product_by_barcode(
        self,
        db: AsyncSession,
        barcode: str
    ) -> Optional[Product]:
        """
        Buscar produto por código de barras
        """
        try:
            query = select(Product).where(
                and_(
                    Product.barcode == barcode,
                    Product.is_active == True
                )
            ).options(selectinload(Product.store))
            
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar produto por código: {str(e)}")
            raise
    
    async def create_product(
        self,
        db: AsyncSession,
        product_data: ProductCreate,
        created_by: UUID
    ) -> Product:
        """
        Criar novo produto
        """
        try:
            # Criar produto
            product = Product(
                name=product_data.name,
                description=product_data.description,
                barcode=product_data.barcode,
                category=product_data.category,
                price=product_data.price,
                unit=product_data.unit,
                weight=product_data.weight,
                volume=product_data.volume,
                brand=product_data.brand,
                manufacturer=product_data.manufacturer,
                esg_score=product_data.esg_score,
                is_organic=product_data.is_organic,
                is_vegan=product_data.is_vegan,
                is_gluten_free=product_data.is_gluten_free,
                is_lactose_free=product_data.is_lactose_free,
                sustainability_notes=product_data.sustainability_notes,
                calories_per_100g=product_data.calories_per_100g,
                protein_per_100g=product_data.protein_per_100g,
                carbs_per_100g=product_data.carbs_per_100g,
                fat_per_100g=product_data.fat_per_100g,
                image_url=product_data.image_url,
                image_urls=product_data.image_urls,
                store_id=product_data.store_id,
                created_by=created_by,
                created_at=datetime.utcnow()
            )
            
            db.add(product)
            await db.commit()
            await db.refresh(product)
            
            logger.info(f"✅ Produto criado: {product.name}")
            return product
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar produto: {str(e)}")
            await db.rollback()
            raise
    
    async def update_product(
        self,
        db: AsyncSession,
        product: Product,
        product_data: ProductUpdate,
        updated_by: UUID
    ) -> Product:
        """
        Atualizar produto
        """
        try:
            # Atualizar campos fornecidos
            update_data = product_data.dict(exclude_unset=True)
            
            for field, value in update_data.items():
                if hasattr(product, field):
                    setattr(product, field, value)
            
            product.updated_by = updated_by
            product.updated_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(product)
            
            logger.info(f"✅ Produto atualizado: {product.name}")
            return product
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar produto: {str(e)}")
            await db.rollback()
            raise
    
    async def deactivate_product(
        self,
        db: AsyncSession,
        product: Product,
        deactivated_by: UUID
    ) -> Product:
        """
        Desativar produto
        """
        try:
            product.is_active = False
            product.updated_by = deactivated_by
            product.updated_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(product)
            
            logger.info(f"✅ Produto desativado: {product.name}")
            return product
            
        except Exception as e:
            logger.error(f"❌ Erro ao desativar produto: {str(e)}")
            await db.rollback()
            raise
    
    async def get_categories(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Obter categorias de produtos
        """
        try:
            # Buscar categorias únicas
            query = select(
                Product.category,
                func.count(Product.id).label('product_count')
            ).where(
                Product.is_active == True
            ).group_by(Product.category).order_by(Product.category)
            
            result = await db.execute(query)
            categories = result.fetchall()
            
            return [
                {
                    "name": category[0],
                    "product_count": category[1]
                }
                for category in categories
            ]
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter categorias: {str(e)}")
            raise
    
    async def get_search_suggestions(
        self,
        db: AsyncSession,
        query: str,
        limit: int = 10
    ) -> List[str]:
        """
        Obter sugestões de busca
        """
        try:
            search_term = f"%{query}%"
            
            # Buscar sugestões por nome
            name_query = select(Product.name).where(
                and_(
                    Product.name.ilike(search_term),
                    Product.is_active == True
                )
            ).limit(limit)
            
            result = await db.execute(name_query)
            suggestions = [row[0] for row in result.fetchall()]
            
            return suggestions
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter sugestões: {str(e)}")
            raise
    
    async def get_product_stats(
        self,
        db: AsyncSession,
        store_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """
        Obter estatísticas de produtos
        """
        try:
            base_query = select(Product).where(Product.is_active == True)
            
            if store_id:
                base_query = base_query.where(Product.store_id == store_id)
            
            # Total de produtos
            total_query = select(func.count(Product.id)).where(Product.is_active == True)
            if store_id:
                total_query = total_query.where(Product.store_id == store_id)
            
            total_result = await db.execute(total_query)
            total_products = total_result.scalar()
            
            # Produtos ativos
            active_result = await db.execute(total_query)
            active_products = active_result.scalar()
            
            # Produtos inativos
            inactive_query = select(func.count(Product.id)).where(Product.is_active == False)
            if store_id:
                inactive_query = inactive_query.where(Product.store_id == store_id)
            
            inactive_result = await db.execute(inactive_query)
            inactive_products = inactive_result.scalar()
            
            # Produtos orgânicos
            organic_query = select(func.count(Product.id)).where(
                and_(Product.is_organic == True, Product.is_active == True)
            )
            if store_id:
                organic_query = organic_query.where(Product.store_id == store_id)
            
            organic_result = await db.execute(organic_query)
            organic_products = organic_result.scalar()
            
            # Produtos veganos
            vegan_query = select(func.count(Product.id)).where(
                and_(Product.is_vegan == True, Product.is_active == True)
            )
            if store_id:
                vegan_query = vegan_query.where(Product.store_id == store_id)
            
            vegan_result = await db.execute(vegan_query)
            vegan_products = vegan_result.scalar()
            
            # Score ESG médio
            esg_query = select(func.avg(Product.esg_score)).where(Product.is_active == True)
            if store_id:
                esg_query = esg_query.where(Product.store_id == store_id)
            
            esg_result = await db.execute(esg_query)
            average_esg_score = esg_result.scalar() or 0
            
            # Preço médio
            price_query = select(func.avg(Product.price)).where(Product.is_active == True)
            if store_id:
                price_query = price_query.where(Product.store_id == store_id)
            
            price_result = await db.execute(price_query)
            average_price = price_result.scalar() or 0
            
            return {
                "total_products": total_products,
                "active_products": active_products,
                "inactive_products": inactive_products,
                "organic_products": organic_products,
                "vegan_products": vegan_products,
                "average_esg_score": float(average_esg_score),
                "average_price": float(average_price)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas: {str(e)}")
            raise
    
    async def record_product_scan(
        self,
        db: AsyncSession,
        product: Product,
        user: User
    ) -> None:
        """
        Registrar escaneamento de produto
        """
        try:
            # Atualizar contador de escaneamentos
            product.scan_count += 1
            product.last_scan = datetime.utcnow()
            
            await db.commit()
            
            logger.info(f"✅ Escaneamento registrado: {product.name}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao registrar escaneamento: {str(e)}")
            await db.rollback()
            raise
    
    async def get_store_by_id(
        self,
        db: AsyncSession,
        store_id: UUID
    ) -> Optional[Store]:
        """
        Buscar loja por ID
        """
        try:
            query = select(Store).where(Store.id == store_id)
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar loja: {str(e)}")
            raise
